### Minikube development

- minikube start

Kubernetes environment build docker images

- `eval $(minikube docker-env)`
- `docker build --platform linux/amd64 -t model-server -f Dockerfile.model-server  .`
- `docker build --platform linux/amd64 -t web-server -f Dockerfile.web-server  .`
- `eval $(minikube docker-env -u)`

Ensure that in `kubectl get pod` all `three` pods are in running state

- `minikube service model-server-service`
- `minikube service web-server-service`

**Debugging pods or server**

- kubectl logs <`pod name`>

**Testing**

- `curl -X POST <http://127.0.0.1:43139/classify-imagenet> -H "Content-Type: multipart/form-data" -F "image=@dog.jpg"`

```
{"golden_retriever":0.40282928943634033,"Brittany_spaniel":0.2731628119945526,"vizsla, Hungarian_pointer":0.03351568430662155,"Sussex_spaniel":0.017249081283807755,"Chesapeake_Bay_retriever":0.011031302623450756}
```

**Ingress Services**

- `minikube addons enable ingress`
- `minikube tunnel`

In `/etc/hosts` add

```

127.0.0.1       fastapi.locahost        localhost

```

- Also do in  `C:\Windows\System32\drivers\etc\hosts` if you are in windows and using wsl. if not u can reach through curl in wsl but not in browser.