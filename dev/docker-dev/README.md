### Docker testing of model-server and web-server(fastapi)

**Build**

- `docker build -t model-server -f Dockerfile.model-server .`
- `docker build -t web-server -f Dockerfile.web-server .`

**Start Servers**

Model server

- `docker run -it -v /home/ajith/mlops/course/emlo_play/emlo4-s14/dev-place/src/model-server:/opt/src -p8000:8000 model-server bash`
- `python server.py`

Web server

- `docker run -it -v /home/ajith/mlops/course/emlo_play/emlo4-s14/dev-place/src/web-server:/opt/src -p9000:9000 web-server bash`
- `python server.py`

**Testing both services**

Note: remember @ before the filepath

- `curl -X POST http://localhost:8000/infer -H "Content-Type: multipart/form-data" -F "image=@dog.jpg"`

- `curl -X POST http://localhost:9000/classify-imagenet -H "Content-Type: multipart/form-data" -F "image=@dog.jpg"`

- After testing this you can proceed with `minikube`