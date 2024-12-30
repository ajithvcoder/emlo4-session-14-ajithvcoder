import urllib
import io
import os
import zlib
import json
import socket
import logging
import requests

import redis.asyncio as redis
import torch
import timm
import numpy as np

from PIL import Image
from fastapi import FastAPI, File, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from typing import Dict, Annotated

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - ModelServer - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

app = FastAPI(title="Mamba Model Server")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Update environment variables
MODEL_NAME = os.environ.get("MODEL_NAME", "mambaout_femto.in1k")
REDIS_HOST = os.environ.get("REDIS_HOST", "localhost")
REDIS_PORT = os.environ.get("REDIS_PORT", "6379")
REDIS_PASSWORD = os.environ.get("REDIS_PASSWORD", "")
HOSTNAME = socket.gethostname()

@app.on_event("startup")
async def initialize():
    global model, device, transform, categories, redis_pool

    logger.info(f"Initializing model server on host {HOSTNAME}")

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    logger.info(f"Using device: {device}")

    logger.info(f"Loading model: {MODEL_NAME}")
    model = timm.create_model(MODEL_NAME, pretrained=True)
    model = model.to(device)
    model.eval()
    logger.info(f"Model loaded successfully")

    # Get model specific transforms
    logger.info("Setting up model transforms")
    data_config = timm.data.resolve_model_data_config(model)
    transform = timm.data.create_transform(**data_config, is_training=False)

    # Load ImageNet labels
    logger.info("Loading ImageNet categories")
    url = "https://storage.googleapis.com/bit_models/ilsvrc2012_wordnet_lemmas.txt"
    categories = requests.get(url).text.strip().split("\n")
    # print(categories)
    logger.info(f"Loaded {len(categories)} categories")

    # Redis setup
    logger.info(f"Creating Redis connection pool: host={REDIS_HOST}, port={REDIS_PORT}")
    redis_pool = redis.ConnectionPool(
        host=REDIS_HOST,
        port=REDIS_PORT,
        password=REDIS_PASSWORD,
        db=0,
        decode_responses=True,
    )
    logger.info("Model server initialization complete")

@app.on_event("shutdown")
async def shutdown():
    """Cleanup connection pool on shutdown"""
    logger.info("Shutting down model server")
    await redis_pool.aclose()
    logger.info("Cleanup complete")

def get_redis():
    return redis.Redis(connection_pool=redis_pool)

def predict(inp_img: Image) -> Dict[str, float]:
    logger.debug("Starting prediction")
    img = inp_img.convert("RGB")
    img_tensor = transform(img).unsqueeze(0).to(device)

    # inference
    with torch.no_grad():
        logger.debug("Running inference")
        out = model(img_tensor)
        probabilities = torch.nn.functional.softmax(out[0], dim=0)

        # Get top predictions
        top_prob, top_catid = torch.topk(probabilities, 5)
        confidences = {
            categories[idx.item()]: float(prob)
            for prob, idx in zip(top_prob, top_catid)
        }

    logger.debug(f"Prediction complete. Top class: {list(confidences.keys())[0]}")
    return confidences

async def write_to_cache(file: bytes, result: Dict[str, float]) -> None:
    cache = get_redis()
    hash = str(zlib.adler32(file))
    logger.debug(f"Writing prediction to cache with hash: {hash}")
    await cache.set(hash, json.dumps(result))
    logger.debug("Cache write complete")

@app.post("/infer")
async def infer(image: Annotated[bytes, File()]):
    
    logger.info("Received inference request")
    img: Image.Image = Image.open(io.BytesIO(image))

    logger.debug("Running prediction")
    predictions = predict(img)

    logger.debug("Writing results to cache")
    await write_to_cache(image, predictions)

    logger.info("Inference complete")
    return predictions

@app.get("/health")
async def health_check():
    try:
        redis_client = get_redis()
        redis_connected = await redis_client.ping()
    except Exception as e:
        logger.error(f"Redis health check failed: {str(e)}")
        redis_connected = False

    return {
        "status": "healthy",
        "hostname": HOSTNAME,
        "model": MODEL_NAME,
        "device": str(device) if "device" in globals() else None,
        "redis": {
            "host": REDIS_HOST,
            "port": REDIS_PORT,
            "connected": redis_connected,
        },
    }

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=80)
