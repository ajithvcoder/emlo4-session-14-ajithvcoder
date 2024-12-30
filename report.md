### Report for Assignment

- Output of the following in a .md file in your repository

- `kubectl describe <your_deployment>`
- `kubectl describe <your_pod>`
- `kubectl describe <your_ingress>`
- `kubectl top pod`
- `kubectl top node`
- `kubectl get all -A -o yaml`

#### Describe Deployment

- `kubectl describe deployment.apps/model-server -n prod`

**Model-server**

  ```
  Name:                   model-server
  Namespace:              prod
  CreationTimestamp:      Mon, 30 Dec 2024 11:19:59 +0000
  Labels:                 app.kubernetes.io/managed-by=Helm
                          app.kubernetes.io/name=model-server
                          app.kubernetes.io/part-of=fastapi-app
  Annotations:            deployment.kubernetes.io/revision: 1
                          meta.helm.sh/release-name: fastapi-release-prod
                          meta.helm.sh/release-namespace: production
  Selector:               app.kubernetes.io/name=model-server
  Replicas:               2 desired | 2 updated | 2 total | 2 available | 0 unavailable
  StrategyType:           RollingUpdate
  MinReadySeconds:        0
  RollingUpdateStrategy:  25% max unavailable, 25% max surge
  Pod Template:
    Labels:  app.kubernetes.io/name=model-server
    Containers:
    model-server:
      Image:      model-server:latest
      Port:       80/TCP
      Host Port:  0/TCP
      Limits:
        cpu:     1
        memory:  2Gi
      Environment:
        REDIS_HOST:      <set to the key 'hostname' of config map 'redis-config-v1'>           Optional: false
        REDIS_PORT:      <set to the key 'port' of config map 'redis-config-v1'>               Optional: false
        REDIS_PASSWORD:  <set to the key 'db_password' in secret 'redis-secret-v1'>            Optional: false
        MODEL_NAME:      <set to the key 'model_name' of config map 'model-server-config-v1'>  Optional: false
      Mounts:            <none>
    Volumes:             <none>
    Node-Selectors:      <none>
    Tolerations:         <none>
  Conditions:
    Type           Status  Reason
    ----           ------  ------
    Available      True    MinimumReplicasAvailable
    Progressing    True    NewReplicaSetAvailable
  OldReplicaSets:  <none>
  NewReplicaSet:   model-server-664885b79f (2/2 replicas created)
  Events:
    Type    Reason             Age   From                   Message
    ----    ------             ----  ----                   -------
    Normal  ScalingReplicaSet  23m   deployment-controller  Scaled up replica set model-server-664885b79f to 2
  ```

**Redis**

- `kubectl describe deployment.apps/redis -n prod`

  ```
  Name:                   redis
  Namespace:              prod
  CreationTimestamp:      Mon, 30 Dec 2024 11:19:59 +0000
  Labels:                 app.kubernetes.io/managed-by=Helm
                          app.kubernetes.io/name=redis
                          app.kubernetes.io/part-of=fastapi-app
  Annotations:            deployment.kubernetes.io/revision: 1
                          meta.helm.sh/release-name: fastapi-release-prod
                          meta.helm.sh/release-namespace: production
  Selector:               app.kubernetes.io/name=redis,role=master
  Replicas:               1 desired | 1 updated | 1 total | 1 available | 0 unavailable
  StrategyType:           RollingUpdate
  MinReadySeconds:        0
  RollingUpdateStrategy:  25% max unavailable, 25% max surge
  Pod Template:
    Labels:  app.kubernetes.io/name=redis
            role=master
    Containers:
    redis:
      Image:      redis:7.4.1
      Port:       6379/TCP
      Host Port:  0/TCP
      Command:
        redis-server
      Args:
        --requirepass
        $(REDIS_PASSWORD)
      Limits:
        cpu:     200m
        memory:  200Mi
      Environment:
        REDIS_PASSWORD:  <set to the key 'db_password' in secret 'redis-secret-v1'>  Optional: false
      Mounts:
        /data from redis-storage (rw)
    Volumes:
    redis-storage:
      Type:          PersistentVolumeClaim (a reference to a PersistentVolumeClaim in the same namespace)
      ClaimName:     redis-pvc
      ReadOnly:      false
    Node-Selectors:  <none>
    Tolerations:     <none>
  Conditions:
    Type           Status  Reason
    ----           ------  ------
    Available      True    MinimumReplicasAvailable
    Progressing    True    NewReplicaSetAvailable
  OldReplicaSets:  <none>
  NewReplicaSet:   redis-69cf9b5676 (1/1 replicas created)
  Events:
    Type    Reason             Age   From                   Message
    ----    ------             ----  ----                   -------
    Normal  ScalingReplicaSet  24m   deployment-controller  Scaled up replica set redis-69cf9b5676 to 1
  ```

**Web-server**

- `kubectl describe deployment.apps/web-server    -n prod`

  ```
  Name:                   web-server
  Namespace:              prod
  CreationTimestamp:      Mon, 30 Dec 2024 11:19:59 +0000
  Labels:                 app.kubernetes.io/managed-by=Helm
                          app.kubernetes.io/name=web-server
                          app.kubernetes.io/part-of=fastapi-app
  Annotations:            deployment.kubernetes.io/revision: 1
                          meta.helm.sh/release-name: fastapi-release-prod
                          meta.helm.sh/release-namespace: production
  Selector:               app.kubernetes.io/name=web-server
  Replicas:               2 desired | 2 updated | 2 total | 2 available | 0 unavailable
  StrategyType:           RollingUpdate
  MinReadySeconds:        0
  RollingUpdateStrategy:  25% max unavailable, 25% max surge
  Pod Template:
    Labels:  app.kubernetes.io/name=web-server
    Containers:
    web-server:
      Image:      web-server:latest
      Port:       80/TCP
      Host Port:  0/TCP
      Environment:
        REDIS_HOST:        <set to the key 'hostname' of config map 'redis-config-v1'>                 Optional: false
        REDIS_PORT:        <set to the key 'port' of config map 'redis-config-v1'>                     Optional: false
        REDIS_PASSWORD:    <set to the key 'db_password' in secret 'redis-secret-v1'>                  Optional: false
        MODEL_SERVER_URL:  <set to the key 'model_server_url' of config map 'model-server-config-v1'>  Optional: false
      Mounts:              <none>
    Volumes:               <none>
    Node-Selectors:        <none>
    Tolerations:           <none>
  Conditions:
    Type           Status  Reason
    ----           ------  ------
    Available      True    MinimumReplicasAvailable
    Progressing    True    NewReplicaSetAvailable
  OldReplicaSets:  <none>
  NewReplicaSet:   web-server-5c89b7fd87 (2/2 replicas created)
  Events:
    Type    Reason             Age   From                   Message
    ----    ------             ----  ----                   -------
    Normal  ScalingReplicaSet  24m   deployment-controller  Scaled up replica set web-server-5c89b7fd87 to 2
  ```

#### Describe Pod

**model-server pod**

- `kubectl describe pod/model-server-664885b79f-g7q85    -n prod`

  ```
  Name:             model-server-664885b79f-g7q85
  Namespace:        prod
  Priority:         0
  Service Account:  default
  Node:             minikube/192.168.49.2
  Start Time:       Mon, 30 Dec 2024 11:20:00 +0000
  Labels:           app.kubernetes.io/name=model-server
                    pod-template-hash=664885b79f
  Annotations:      <none>
  Status:           Running
  IP:               10.244.0.25
  IPs:
    IP:           10.244.0.25
  Controlled By:  ReplicaSet/model-server-664885b79f
  Containers:
    model-server:
      Container ID:   docker://a434b50d85b13874aad3f7f0d3d0ced24ff5aa0cbe3a655f139029654bcb34bc
      Image:          model-server:latest
      Image ID:       docker://sha256:7b09b0acbbfa7baf666665468a5dbd930895258597ffcfa0e83ab22e09f3f57d
      Port:           80/TCP
      Host Port:      0/TCP
      State:          Running
        Started:      Mon, 30 Dec 2024 11:20:02 +0000
      Ready:          True
      Restart Count:  0
      Limits:
        cpu:     1
        memory:  2Gi
      Requests:
        cpu:     1
        memory:  2Gi
      Environment:
        REDIS_HOST:      <set to the key 'hostname' of config map 'redis-config-v1'>           Optional: false
        REDIS_PORT:      <set to the key 'port' of config map 'redis-config-v1'>               Optional: false
        REDIS_PASSWORD:  <set to the key 'db_password' in secret 'redis-secret-v1'>            Optional: false
        MODEL_NAME:      <set to the key 'model_name' of config map 'model-server-config-v1'>  Optional: false
      Mounts:
        /var/run/secrets/kubernetes.io/serviceaccount from kube-api-access-k9xzz (ro)
  Conditions:
    Type                        Status
    PodReadyToStartContainers   True 
    Initialized                 True 
    Ready                       True 
    ContainersReady             True 
    PodScheduled                True 
  Volumes:
    kube-api-access-k9xzz:
      Type:                    Projected (a volume that contains injected data from multiple sources)
      TokenExpirationSeconds:  3607
      ConfigMapName:           kube-root-ca.crt
      ConfigMapOptional:       <nil>
      DownwardAPI:             true
  QoS Class:                   Guaranteed
  Node-Selectors:              <none>
  Tolerations:                 node.kubernetes.io/not-ready:NoExecute op=Exists for 300s
                              node.kubernetes.io/unreachable:NoExecute op=Exists for 300s
  Events:
    Type    Reason     Age   From               Message
    ----    ------     ----  ----               -------
    Normal  Scheduled  25m   default-scheduler  Successfully assigned prod/model-server-664885b79f-g7q85 to minikube
    Normal  Pulled     25m   kubelet            Container image "model-server:latest" already present on machine
    Normal  Created    25m   kubelet            Created container model-server
    Normal  Started    25m   kubelet            Started container model-server
  ```

**Redis-pod**

- `kubectl describe pod/redis-69cf9b5676-ksgqb  -n prod`

  ```
  Name:             redis-69cf9b5676-ksgqb
  Namespace:        prod
  Priority:         0
  Service Account:  default
  Node:             minikube/192.168.49.2
  Start Time:       Mon, 30 Dec 2024 11:20:00 +0000
  Labels:           app.kubernetes.io/name=redis
                    pod-template-hash=69cf9b5676
                    role=master
  Annotations:      <none>
  Status:           Running
  IP:               10.244.0.24
  IPs:
    IP:           10.244.0.24
  Controlled By:  ReplicaSet/redis-69cf9b5676
  Containers:
    redis:
      Container ID:  docker://56f47c7cada60042797f82e86db5013538e6fda674ff77897ed9130071f0b60a
      Image:         redis:7.4.1
      Image ID:      docker-pullable://redis@sha256:bb142a9c18ac18a16713c1491d779697b4e107c22a97266616099d288237ef47
      Port:          6379/TCP
      Host Port:     0/TCP
      Command:
        redis-server
      Args:
        --requirepass
        $(REDIS_PASSWORD)
      State:          Running
        Started:      Mon, 30 Dec 2024 11:20:02 +0000
      Ready:          True
      Restart Count:  0
      Limits:
        cpu:     200m
        memory:  200Mi
      Requests:
        cpu:     200m
        memory:  200Mi
      Environment:
        REDIS_PASSWORD:  <set to the key 'db_password' in secret 'redis-secret-v1'>  Optional: false
      Mounts:
        /data from redis-storage (rw)
        /var/run/secrets/kubernetes.io/serviceaccount from kube-api-access-54b62 (ro)
  Conditions:
    Type                        Status
    PodReadyToStartContainers   True 
    Initialized                 True 
    Ready                       True 
    ContainersReady             True 
    PodScheduled                True 
  Volumes:
    redis-storage:
      Type:       PersistentVolumeClaim (a reference to a PersistentVolumeClaim in the same namespace)
      ClaimName:  redis-pvc
      ReadOnly:   false
    kube-api-access-54b62:
      Type:                    Projected (a volume that contains injected data from multiple sources)
      TokenExpirationSeconds:  3607
      ConfigMapName:           kube-root-ca.crt
      ConfigMapOptional:       <nil>
      DownwardAPI:             true
  QoS Class:                   Guaranteed
  Node-Selectors:              <none>
  Tolerations:                 node.kubernetes.io/not-ready:NoExecute op=Exists for 300s
                              node.kubernetes.io/unreachable:NoExecute op=Exists for 300s
  Events:
    Type    Reason     Age   From               Message
    ----    ------     ----  ----               -------
    Normal  Scheduled  26m   default-scheduler  Successfully assigned prod/redis-69cf9b5676-ksgqb to minikube
    Normal  Pulled     26m   kubelet            Container image "redis:7.4.1" already present on machine
    Normal  Created    26m   kubelet            Created container redis
    Normal  Started    26m   kubelet            Started container redis
  ```

**Web-Server**

- `kubectl describe pod/web-server-5c89b7fd87-vh7kk -n prod`

  ```
  Name:             web-server-5c89b7fd87-vh7kk
  Namespace:        prod
  Priority:         0
  Service Account:  default
  Node:             minikube/192.168.49.2
  Start Time:       Mon, 30 Dec 2024 11:20:00 +0000
  Labels:           app.kubernetes.io/name=web-server
                    pod-template-hash=5c89b7fd87
  Annotations:      <none>
  Status:           Running
  IP:               10.244.0.23
  IPs:
    IP:           10.244.0.23
  Controlled By:  ReplicaSet/web-server-5c89b7fd87
  Containers:
    web-server:
      Container ID:   docker://e932dc2cd156ebefe65109d79aeb481115a8d8c8c60f892ff3f1e5769cd81c39
      Image:          web-server:latest
      Image ID:       docker://sha256:c7cc6d48367bb4147ac5ac200583fe06a6d1bcefd02377f384a8965ec6ec9899
      Port:           80/TCP
      Host Port:      0/TCP
      State:          Running
        Started:      Mon, 30 Dec 2024 11:20:02 +0000
      Ready:          True
      Restart Count:  0
      Environment:
        REDIS_HOST:        <set to the key 'hostname' of config map 'redis-config-v1'>                 Optional: false
        REDIS_PORT:        <set to the key 'port' of config map 'redis-config-v1'>                     Optional: false
        REDIS_PASSWORD:    <set to the key 'db_password' in secret 'redis-secret-v1'>                  Optional: false
        MODEL_SERVER_URL:  <set to the key 'model_server_url' of config map 'model-server-config-v1'>  Optional: false
      Mounts:
        /var/run/secrets/kubernetes.io/serviceaccount from kube-api-access-c8rtm (ro)
  Conditions:
    Type                        Status
    PodReadyToStartContainers   True 
    Initialized                 True 
    Ready                       True 
    ContainersReady             True 
    PodScheduled                True 
  Volumes:
    kube-api-access-c8rtm:
      Type:                    Projected (a volume that contains injected data from multiple sources)
      TokenExpirationSeconds:  3607
      ConfigMapName:           kube-root-ca.crt
      ConfigMapOptional:       <nil>
      DownwardAPI:             true
  QoS Class:                   BestEffort
  Node-Selectors:              <none>
  Tolerations:                 node.kubernetes.io/not-ready:NoExecute op=Exists for 300s
                              node.kubernetes.io/unreachable:NoExecute op=Exists for 300s
  Events:
    Type    Reason     Age   From               Message
    ----    ------     ----  ----               -------
    Normal  Scheduled  26m   default-scheduler  Successfully assigned prod/web-server-5c89b7fd87-vh7kk to minikube
    Normal  Pulled     26m   kubelet            Container image "web-server:latest" already present on machine
    Normal  Created    26m   kubelet            Created container web-server
    Normal  Started    26m   kubelet            Started container web-server
  ```

**Describe Ingress**

- `kubectl get ingress -n prod`

  ```
  NAME                 CLASS    HOSTS          ADDRESS        PORTS   AGE
  web-server-ingress   <none>   fastapi.prod   192.168.49.2   80      27m
  ```

- `kubectl describe ingress -n prod`

  ```
  Name:             web-server-ingress
  Labels:           app.kubernetes.io/managed-by=Helm
                    app.kubernetes.io/name=web-server
                    app.kubernetes.io/part-of=fastapi-app
  Namespace:        prod
  Address:          192.168.49.2
  Ingress Class:    <none>
  Default backend:  <default>
  Rules:
    Host          Path  Backends
    ----          ----  --------
    fastapi.prod  
                  /   web-server-service:80 (10.244.0.23:80,10.244.0.26:80)
  Annotations:    meta.helm.sh/release-name: fastapi-release-prod
                  meta.helm.sh/release-namespace: production
  Events:
    Type    Reason  Age                From                      Message
    ----    ------  ----               ----                      -------
    Normal  Sync    22m (x2 over 23m)  nginx-ingress-controller  Scheduled for sync
  ```

#### Top Node

- `kubectl top node  -n prod `

  ```
  NAME       CPU(cores)   CPU%   MEMORY(bytes)   MEMORY%   
  minikube   239m         0%     1956Mi          25%       
  ```

#### Top Pod

- `kubectl top pod -n prod`

  ```
  NAME                            CPU(cores)   MEMORY(bytes)   
  model-server-664885b79f-g7q85   2m           141Mi           
  model-server-664885b79f-qc4ck   3m           142Mi           
  redis-69cf9b5676-ksgqb          5m           11Mi            
  web-server-5c89b7fd87-5c928     3m           49Mi            
  web-server-5c89b7fd87-vh7kk     3m           51Mi            
  ```

#### Get all info

- `kubectl get all -A -o yaml`

  ```
  apiVersion: v1
  items:
  - apiVersion: v1
    kind: Pod
    metadata:
      creationTimestamp: "2024-12-30T11:24:37Z"
      generateName: ingress-nginx-admission-create-
      labels:
        app.kubernetes.io/component: admission-webhook
        app.kubernetes.io/instance: ingress-nginx
        app.kubernetes.io/name: ingress-nginx
        batch.kubernetes.io/controller-uid: 4656eb27-4c5b-4f8a-8a24-dd97448d8f05
        batch.kubernetes.io/job-name: ingress-nginx-admission-create
        controller-uid: 4656eb27-4c5b-4f8a-8a24-dd97448d8f05
        job-name: ingress-nginx-admission-create
      name: ingress-nginx-admission-create-w4gsb
      namespace: ingress-nginx
      ownerReferences:
      - apiVersion: batch/v1
        blockOwnerDeletion: true
        controller: true
        kind: Job
        name: ingress-nginx-admission-create
        uid: 4656eb27-4c5b-4f8a-8a24-dd97448d8f05
      resourceVersion: "6173"
      uid: de42f17a-5ec1-4129-acb9-eec5dac774ab
    spec:
      containers:
      - args:
        - create
        - --host=ingress-nginx-controller-admission,ingress-nginx-controller-admission.$(POD_NAMESPACE).svc
        - --namespace=$(POD_NAMESPACE)
        - --secret-name=ingress-nginx-admission
        env:
        - name: POD_NAMESPACE
          valueFrom:
            fieldRef:
              apiVersion: v1
              fieldPath: metadata.namespace
        image: registry.k8s.io/ingress-nginx/kube-webhook-certgen:v1.4.3@sha256:a320a50cc91bd15fd2d6fa6de58bd98c1bd64b9a6f926ce23a600d87043455a3
        imagePullPolicy: IfNotPresent
        name: create
        resources: {}
        securityContext:
          allowPrivilegeEscalation: false
        terminationMessagePath: /dev/termination-log
        terminationMessagePolicy: File
        volumeMounts:
        - mountPath: /var/run/secrets/kubernetes.io/serviceaccount
          name: kube-api-access-g9n7h
          readOnly: true
      dnsPolicy: ClusterFirst
      enableServiceLinks: true
      nodeName: minikube
      nodeSelector:
        kubernetes.io/os: linux
        minikube.k8s.io/primary: "true"
      preemptionPolicy: PreemptLowerPriority
      priority: 0
      restartPolicy: OnFailure
      schedulerName: default-scheduler
      securityContext:
        runAsNonRoot: true
        runAsUser: 2000
      serviceAccount: ingress-nginx-admission
      serviceAccountName: ingress-nginx-admission
      terminationGracePeriodSeconds: 30
      tolerations:
      - effect: NoExecute
        key: node.kubernetes.io/not-ready
        operator: Exists
        tolerationSeconds: 300
      - effect: NoExecute
        key: node.kubernetes.io/unreachable
        operator: Exists
        tolerationSeconds: 300
      volumes:
      - name: kube-api-access-g9n7h
        projected:
          defaultMode: 420
          sources:
          - serviceAccountToken:
              expirationSeconds: 3607
              path: token
          - configMap:
              items:
              - key: ca.crt
                path: ca.crt
              name: kube-root-ca.crt
          - downwardAPI:
              items:
              - fieldRef:
                  apiVersion: v1
                  fieldPath: metadata.namespace
                path: namespace
    status:
      conditions:
      - lastProbeTime: null
        lastTransitionTime: "2024-12-30T11:24:54Z"
        status: "False"
        type: PodReadyToStartContainers
      - lastProbeTime: null
        lastTransitionTime: "2024-12-30T11:24:37Z"
        reason: PodCompleted
        status: "True"
        type: Initialized
      - lastProbeTime: null
        lastTransitionTime: "2024-12-30T11:24:37Z"
        reason: PodCompleted
        status: "False"
        type: Ready
      - lastProbeTime: null
        lastTransitionTime: "2024-12-30T11:24:37Z"
        reason: PodCompleted
        status: "False"
        type: ContainersReady
      - lastProbeTime: null
        lastTransitionTime: "2024-12-30T11:24:37Z"
        status: "True"
        type: PodScheduled
      containerStatuses:
      - containerID: docker://80669d858cd1edd5a573030b25bc84c38a1fe2822d8d3205c2fb597a62c5822f
        image: registry.k8s.io/ingress-nginx/kube-webhook-certgen@sha256:a320a50cc91bd15fd2d6fa6de58bd98c1bd64b9a6f926ce23a600d87043455a3
        imageID: docker-pullable://registry.k8s.io/ingress-nginx/kube-webhook-certgen@sha256:a320a50cc91bd15fd2d6fa6de58bd98c1bd64b9a6f926ce23a600d87043455a3
        lastState: {}
        name: create
        ready: false
        restartCount: 0
        started: false
        state:
          terminated:
            containerID: docker://80669d858cd1edd5a573030b25bc84c38a1fe2822d8d3205c2fb597a62c5822f
            exitCode: 0
            finishedAt: "2024-12-30T11:24:52Z"
            reason: Completed
            startedAt: "2024-12-30T11:24:52Z"
        volumeMounts:
        - mountPath: /var/run/secrets/kubernetes.io/serviceaccount
          name: kube-api-access-g9n7h
          readOnly: true
          recursiveReadOnly: Disabled
      hostIP: 192.168.49.2
      hostIPs:
      - ip: 192.168.49.2
      phase: Succeeded
      podIP: 10.244.0.28
      podIPs:
      - ip: 10.244.0.28
      qosClass: BestEffort
      startTime: "2024-12-30T11:24:37Z"
  - apiVersion: v1
    kind: Pod
    metadata:
      creationTimestamp: "2024-12-30T11:24:37Z"
      generateName: ingress-nginx-admission-patch-
      labels:
        app.kubernetes.io/component: admission-webhook
        app.kubernetes.io/instance: ingress-nginx
        app.kubernetes.io/name: ingress-nginx
        batch.kubernetes.io/controller-uid: 251e2330-8e81-4f38-83ac-3fba38d28aa4
        batch.kubernetes.io/job-name: ingress-nginx-admission-patch
        controller-uid: 251e2330-8e81-4f38-83ac-3fba38d28aa4
        job-name: ingress-nginx-admission-patch
      name: ingress-nginx-admission-patch-hzp5l
      namespace: ingress-nginx
      ownerReferences:
      - apiVersion: batch/v1
        blockOwnerDeletion: true
        controller: true
        kind: Job
        name: ingress-nginx-admission-patch
        uid: 251e2330-8e81-4f38-83ac-3fba38d28aa4
      resourceVersion: "6179"
      uid: b302c90c-4d4a-4306-b1c7-1ed1f42b347e
    spec:
      containers:
      - args:
        - patch
        - --webhook-name=ingress-nginx-admission
        - --namespace=$(POD_NAMESPACE)
        - --patch-mutating=false
        - --secret-name=ingress-nginx-admission
        - --patch-failure-policy=Fail
        env:
        - name: POD_NAMESPACE
          valueFrom:
            fieldRef:
              apiVersion: v1
              fieldPath: metadata.namespace
        image: registry.k8s.io/ingress-nginx/kube-webhook-certgen:v1.4.3@sha256:a320a50cc91bd15fd2d6fa6de58bd98c1bd64b9a6f926ce23a600d87043455a3
        imagePullPolicy: IfNotPresent
        name: patch
        resources: {}
        securityContext:
          allowPrivilegeEscalation: false
        terminationMessagePath: /dev/termination-log
        terminationMessagePolicy: File
        volumeMounts:
        - mountPath: /var/run/secrets/kubernetes.io/serviceaccount
          name: kube-api-access-rsfjj
          readOnly: true
      dnsPolicy: ClusterFirst
      enableServiceLinks: true
      nodeName: minikube
      nodeSelector:
        kubernetes.io/os: linux
        minikube.k8s.io/primary: "true"
      preemptionPolicy: PreemptLowerPriority
      priority: 0
      restartPolicy: OnFailure
      schedulerName: default-scheduler
      securityContext:
        runAsNonRoot: true
        runAsUser: 2000
      serviceAccount: ingress-nginx-admission
      serviceAccountName: ingress-nginx-admission
      terminationGracePeriodSeconds: 30
      tolerations:
      - effect: NoExecute
        key: node.kubernetes.io/not-ready
        operator: Exists
        tolerationSeconds: 300
      - effect: NoExecute
        key: node.kubernetes.io/unreachable
        operator: Exists
        tolerationSeconds: 300
      volumes:
      - name: kube-api-access-rsfjj
        projected:
          defaultMode: 420
          sources:
          - serviceAccountToken:
              expirationSeconds: 3607
              path: token
          - configMap:
              items:
              - key: ca.crt
                path: ca.crt
              name: kube-root-ca.crt
          - downwardAPI:
              items:
              - fieldRef:
                  apiVersion: v1
                  fieldPath: metadata.namespace
                path: namespace
    status:
      conditions:
      - lastProbeTime: null
        lastTransitionTime: "2024-12-30T11:24:55Z"
        status: "False"
        type: PodReadyToStartContainers
      - lastProbeTime: null
        lastTransitionTime: "2024-12-30T11:24:37Z"
        reason: PodCompleted
        status: "True"
        type: Initialized
      - lastProbeTime: null
        lastTransitionTime: "2024-12-30T11:24:37Z"
        reason: PodCompleted
        status: "False"
        type: Ready
      - lastProbeTime: null
        lastTransitionTime: "2024-12-30T11:24:37Z"
        reason: PodCompleted
        status: "False"
        type: ContainersReady
      - lastProbeTime: null
        lastTransitionTime: "2024-12-30T11:24:37Z"
        status: "True"
        type: PodScheduled
      containerStatuses:
      - containerID: docker://0473cb759bc684178f4577833c7b81f15858061c3000e24ce870b7222e43ef45
        image: registry.k8s.io/ingress-nginx/kube-webhook-certgen@sha256:a320a50cc91bd15fd2d6fa6de58bd98c1bd64b9a6f926ce23a600d87043455a3
        imageID: docker-pullable://registry.k8s.io/ingress-nginx/kube-webhook-certgen@sha256:a320a50cc91bd15fd2d6fa6de58bd98c1bd64b9a6f926ce23a600d87043455a3
        lastState: {}
        name: patch
        ready: false
        restartCount: 0
        started: false
        state:
          terminated:
            containerID: docker://0473cb759bc684178f4577833c7b81f15858061c3000e24ce870b7222e43ef45
            exitCode: 0
            finishedAt: "2024-12-30T11:24:52Z"
            reason: Completed
            startedAt: "2024-12-30T11:24:52Z"
        volumeMounts:
        - mountPath: /var/run/secrets/kubernetes.io/serviceaccount
          name: kube-api-access-rsfjj
          readOnly: true
          recursiveReadOnly: Disabled
      hostIP: 192.168.49.2
      hostIPs:
      - ip: 192.168.49.2
      phase: Succeeded
      podIP: 10.244.0.29
      podIPs:
      - ip: 10.244.0.29
      qosClass: BestEffort
      startTime: "2024-12-30T11:24:37Z"
  - apiVersion: v1
    kind: Pod
    metadata:
      creationTimestamp: "2024-12-30T11:24:37Z"
      generateName: ingress-nginx-controller-bc57996ff-
      labels:
        app.kubernetes.io/component: controller
        app.kubernetes.io/instance: ingress-nginx
        app.kubernetes.io/name: ingress-nginx
        gcp-auth-skip-secret: "true"
        pod-template-hash: bc57996ff
      name: ingress-nginx-controller-bc57996ff-grt58
      namespace: ingress-nginx
      ownerReferences:
      - apiVersion: apps/v1
        blockOwnerDeletion: true
        controller: true
        kind: ReplicaSet
        name: ingress-nginx-controller-bc57996ff
        uid: 5fcd67e7-65b4-408f-b284-c6b214d36e05
      resourceVersion: "6295"
      uid: e2664f58-62e5-44cd-a2ad-6474cb62554a
    spec:
      containers:
      - args:
        - /nginx-ingress-controller
        - --election-id=ingress-nginx-leader
        - --controller-class=k8s.io/ingress-nginx
        - --watch-ingress-without-class=true
        - --configmap=$(POD_NAMESPACE)/ingress-nginx-controller
        - --tcp-services-configmap=$(POD_NAMESPACE)/tcp-services
        - --udp-services-configmap=$(POD_NAMESPACE)/udp-services
        - --validating-webhook=:8443
        - --validating-webhook-certificate=/usr/local/certificates/cert
        - --validating-webhook-key=/usr/local/certificates/key
        env:
        - name: POD_NAME
          valueFrom:
            fieldRef:
              apiVersion: v1
              fieldPath: metadata.name
        - name: POD_NAMESPACE
          valueFrom:
            fieldRef:
              apiVersion: v1
              fieldPath: metadata.namespace
        - name: LD_PRELOAD
          value: /usr/local/lib/libmimalloc.so
        image: registry.k8s.io/ingress-nginx/controller:v1.11.2@sha256:d5f8217feeac4887cb1ed21f27c2674e58be06bd8f5184cacea2a69abaf78dce
        imagePullPolicy: IfNotPresent
        lifecycle:
          preStop:
            exec:
              command:
              - /wait-shutdown
        livenessProbe:
          failureThreshold: 5
          httpGet:
            path: /healthz
            port: 10254
            scheme: HTTP
          initialDelaySeconds: 10
          periodSeconds: 10
          successThreshold: 1
          timeoutSeconds: 1
        name: controller
        ports:
        - containerPort: 80
          hostPort: 80
          name: http
          protocol: TCP
        - containerPort: 443
          hostPort: 443
          name: https
          protocol: TCP
        - containerPort: 8443
          name: webhook
          protocol: TCP
        readinessProbe:
          failureThreshold: 3
          httpGet:
            path: /healthz
            port: 10254
            scheme: HTTP
          initialDelaySeconds: 10
          periodSeconds: 10
          successThreshold: 1
          timeoutSeconds: 1
        resources:
          requests:
            cpu: 100m
            memory: 90Mi
        securityContext:
          allowPrivilegeEscalation: true
          capabilities:
            add:
            - NET_BIND_SERVICE
            drop:
            - ALL
          runAsUser: 101
        terminationMessagePath: /dev/termination-log
        terminationMessagePolicy: File
        volumeMounts:
        - mountPath: /usr/local/certificates/
          name: webhook-cert
          readOnly: true
        - mountPath: /var/run/secrets/kubernetes.io/serviceaccount
          name: kube-api-access-kcqf2
          readOnly: true
      dnsPolicy: ClusterFirst
      enableServiceLinks: true
      nodeName: minikube
      nodeSelector:
        kubernetes.io/os: linux
        minikube.k8s.io/primary: "true"
      preemptionPolicy: PreemptLowerPriority
      priority: 0
      restartPolicy: Always
      schedulerName: default-scheduler
      securityContext: {}
      serviceAccount: ingress-nginx
      serviceAccountName: ingress-nginx
      terminationGracePeriodSeconds: 0
      tolerations:
      - effect: NoSchedule
        key: node-role.kubernetes.io/master
        operator: Equal
      - effect: NoExecute
        key: node.kubernetes.io/not-ready
        operator: Exists
        tolerationSeconds: 300
      - effect: NoExecute
        key: node.kubernetes.io/unreachable
        operator: Exists
        tolerationSeconds: 300
      volumes:
      - name: webhook-cert
        secret:
          defaultMode: 420
          secretName: ingress-nginx-admission
      - name: kube-api-access-kcqf2
        projected:
          defaultMode: 420
          sources:
          - serviceAccountToken:
              expirationSeconds: 3607
              path: token
          - configMap:
              items:
              - key: ca.crt
                path: ca.crt
              name: kube-root-ca.crt
          - downwardAPI:
              items:
              - fieldRef:
                  apiVersion: v1
                  fieldPath: metadata.namespace
                path: namespace
    status:
      conditions:
      - lastProbeTime: null
        lastTransitionTime: "2024-12-30T11:25:34Z"
        status: "True"
        type: PodReadyToStartContainers
      - lastProbeTime: null
        lastTransitionTime: "2024-12-30T11:24:37Z"
        status: "True"
        type: Initialized
      - lastProbeTime: null
        lastTransitionTime: "2024-12-30T11:25:45Z"
        status: "True"
        type: Ready
      - lastProbeTime: null
        lastTransitionTime: "2024-12-30T11:25:45Z"
        status: "True"
        type: ContainersReady
      - lastProbeTime: null
        lastTransitionTime: "2024-12-30T11:24:37Z"
        status: "True"
        type: PodScheduled
      containerStatuses:
      - containerID: docker://af53c55411918ce495e10848c8044dc75375df0ee464cefe7c7dbe844f95f07b
        image: registry.k8s.io/ingress-nginx/controller@sha256:d5f8217feeac4887cb1ed21f27c2674e58be06bd8f5184cacea2a69abaf78dce
        imageID: docker-pullable://registry.k8s.io/ingress-nginx/controller@sha256:d5f8217feeac4887cb1ed21f27c2674e58be06bd8f5184cacea2a69abaf78dce
        lastState: {}
        name: controller
        ready: true
        restartCount: 0
        started: true
        state:
          running:
            startedAt: "2024-12-30T11:25:33Z"
        volumeMounts:
        - mountPath: /usr/local/certificates/
          name: webhook-cert
          readOnly: true
          recursiveReadOnly: Disabled
        - mountPath: /var/run/secrets/kubernetes.io/serviceaccount
          name: kube-api-access-kcqf2
          readOnly: true
          recursiveReadOnly: Disabled
      hostIP: 192.168.49.2
      hostIPs:
      - ip: 192.168.49.2
      phase: Running
      podIP: 10.244.0.30
      podIPs:
      - ip: 10.244.0.30
      qosClass: Burstable
      startTime: "2024-12-30T11:24:37Z"
  - apiVersion: v1
    kind: Pod
    metadata:
      creationTimestamp: "2024-12-30T09:46:24Z"
      generateName: coredns-6f6b679f8f-
      labels:
        k8s-app: kube-dns
        pod-template-hash: 6f6b679f8f
      name: coredns-6f6b679f8f-vzg2s
      namespace: kube-system
      ownerReferences:
      - apiVersion: apps/v1
        blockOwnerDeletion: true
        controller: true
        kind: ReplicaSet
        name: coredns-6f6b679f8f
        uid: 0fc88bea-a82e-40e1-bf89-235b47d32db4
      resourceVersion: "5473"
      uid: da2dba22-554a-4d20-ae68-61a1d2e9bc73
    spec:
      affinity:
        podAntiAffinity:
          preferredDuringSchedulingIgnoredDuringExecution:
          - podAffinityTerm:
              labelSelector:
                matchExpressions:
                - key: k8s-app
                  operator: In
                  values:
                  - kube-dns
              topologyKey: kubernetes.io/hostname
            weight: 100
      containers:
      - args:
        - -conf
        - /etc/coredns/Corefile
        image: registry.k8s.io/coredns/coredns:v1.11.1
        imagePullPolicy: IfNotPresent
        livenessProbe:
          failureThreshold: 5
          httpGet:
            path: /health
            port: 8080
            scheme: HTTP
          initialDelaySeconds: 60
          periodSeconds: 10
          successThreshold: 1
          timeoutSeconds: 5
        name: coredns
        ports:
        - containerPort: 53
          name: dns
          protocol: UDP
        - containerPort: 53
          name: dns-tcp
          protocol: TCP
        - containerPort: 9153
          name: metrics
          protocol: TCP
        readinessProbe:
          failureThreshold: 3
          httpGet:
            path: /ready
            port: 8181
            scheme: HTTP
          periodSeconds: 10
          successThreshold: 1
          timeoutSeconds: 1
        resources:
          limits:
            memory: 170Mi
          requests:
            cpu: 100m
            memory: 70Mi
        securityContext:
          allowPrivilegeEscalation: false
          capabilities:
            add:
            - NET_BIND_SERVICE
            drop:
            - ALL
          readOnlyRootFilesystem: true
        terminationMessagePath: /dev/termination-log
        terminationMessagePolicy: File
        volumeMounts:
        - mountPath: /etc/coredns
          name: config-volume
          readOnly: true
        - mountPath: /var/run/secrets/kubernetes.io/serviceaccount
          name: kube-api-access-cx9gs
          readOnly: true
      dnsPolicy: Default
      enableServiceLinks: true
      nodeName: minikube
      nodeSelector:
        kubernetes.io/os: linux
      preemptionPolicy: PreemptLowerPriority
      priority: 2000000000
      priorityClassName: system-cluster-critical
      restartPolicy: Always
      schedulerName: default-scheduler
      securityContext: {}
      serviceAccount: coredns
      serviceAccountName: coredns
      terminationGracePeriodSeconds: 30
      tolerations:
      - key: CriticalAddonsOnly
        operator: Exists
      - effect: NoSchedule
        key: node-role.kubernetes.io/control-plane
      - effect: NoExecute
        key: node.kubernetes.io/not-ready
        operator: Exists
        tolerationSeconds: 300
      - effect: NoExecute
        key: node.kubernetes.io/unreachable
        operator: Exists
        tolerationSeconds: 300
      volumes:
      - configMap:
          defaultMode: 420
          items:
          - key: Corefile
            path: Corefile
          name: coredns
        name: config-volume
      - name: kube-api-access-cx9gs
        projected:
          defaultMode: 420
          sources:
          - serviceAccountToken:
              expirationSeconds: 3607
              path: token
          - configMap:
              items:
              - key: ca.crt
                path: ca.crt
              name: kube-root-ca.crt
          - downwardAPI:
              items:
              - fieldRef:
                  apiVersion: v1
                  fieldPath: metadata.namespace
                path: namespace
    status:
      conditions:
      - lastProbeTime: null
        lastTransitionTime: "2024-12-30T11:15:07Z"
        status: "True"
        type: PodReadyToStartContainers
      - lastProbeTime: null
        lastTransitionTime: "2024-12-30T09:46:24Z"
        status: "True"
        type: Initialized
      - lastProbeTime: null
        lastTransitionTime: "2024-12-30T11:15:43Z"
        status: "True"
        type: Ready
      - lastProbeTime: null
        lastTransitionTime: "2024-12-30T11:15:43Z"
        status: "True"
        type: ContainersReady
      - lastProbeTime: null
        lastTransitionTime: "2024-12-30T09:46:24Z"
        status: "True"
        type: PodScheduled
      containerStatuses:
      - containerID: docker://2aa535a26083202447eb92d1179c3d9bc4076adbab5f4f6800318c1952ef1925
        image: registry.k8s.io/coredns/coredns:v1.11.1
        imageID: docker-pullable://registry.k8s.io/coredns/coredns@sha256:1eeb4c7316bacb1d4c8ead65571cd92dd21e27359f0d4917f1a5822a73b75db1
        lastState:
          terminated:
            containerID: docker://0602339cf7caf336b54f7d8eb864b04aad2b0e383ca0b143c9762dd6e754d3c4
            exitCode: 0
            finishedAt: "2024-12-30T11:14:48Z"
            reason: Completed
            startedAt: "2024-12-30T09:46:26Z"
        name: coredns
        ready: true
        restartCount: 1
        started: true
        state:
          running:
            startedAt: "2024-12-30T11:15:03Z"
        volumeMounts:
        - mountPath: /etc/coredns
          name: config-volume
          readOnly: true
          recursiveReadOnly: Disabled
        - mountPath: /var/run/secrets/kubernetes.io/serviceaccount
          name: kube-api-access-cx9gs
          readOnly: true
          recursiveReadOnly: Disabled
      hostIP: 192.168.49.2
      hostIPs:
      - ip: 192.168.49.2
      phase: Running
      podIP: 10.244.0.19
      podIPs:
      - ip: 10.244.0.19
      qosClass: Burstable
      startTime: "2024-12-30T09:46:24Z"
  - apiVersion: v1
    kind: Pod
    metadata:
      annotations:
        kubeadm.kubernetes.io/etcd.advertise-client-urls: https://192.168.49.2:2379
        kubernetes.io/config.hash: a5363f4f31e043bdae3c93aca4991903
        kubernetes.io/config.mirror: a5363f4f31e043bdae3c93aca4991903
        kubernetes.io/config.seen: "2024-12-30T09:46:19.596805504Z"
        kubernetes.io/config.source: file
      creationTimestamp: "2024-12-30T09:46:19Z"
      labels:
        component: etcd
        tier: control-plane
      name: etcd-minikube
      namespace: kube-system
      ownerReferences:
      - apiVersion: v1
        controller: true
        kind: Node
        name: minikube
        uid: 441abd8e-19ba-4c09-b5a9-7c27af9db6c0
      resourceVersion: "5350"
      uid: 8109526b-1f7c-4bde-bedf-701f1bad9484
    spec:
      containers:
      - command:
        - etcd
        - --advertise-client-urls=https://192.168.49.2:2379
        - --cert-file=/var/lib/minikube/certs/etcd/server.crt
        - --client-cert-auth=true
        - --data-dir=/var/lib/minikube/etcd
        - --experimental-initial-corrupt-check=true
        - --experimental-watch-progress-notify-interval=5s
        - --initial-advertise-peer-urls=https://192.168.49.2:2380
        - --initial-cluster=minikube=https://192.168.49.2:2380
        - --key-file=/var/lib/minikube/certs/etcd/server.key
        - --listen-client-urls=https://127.0.0.1:2379,https://192.168.49.2:2379
        - --listen-metrics-urls=http://127.0.0.1:2381
        - --listen-peer-urls=https://192.168.49.2:2380
        - --name=minikube
        - --peer-cert-file=/var/lib/minikube/certs/etcd/peer.crt
        - --peer-client-cert-auth=true
        - --peer-key-file=/var/lib/minikube/certs/etcd/peer.key
        - --peer-trusted-ca-file=/var/lib/minikube/certs/etcd/ca.crt
        - --proxy-refresh-interval=70000
        - --snapshot-count=10000
        - --trusted-ca-file=/var/lib/minikube/certs/etcd/ca.crt
        image: registry.k8s.io/etcd:3.5.15-0
        imagePullPolicy: IfNotPresent
        livenessProbe:
          failureThreshold: 8
          httpGet:
            host: 127.0.0.1
            path: /livez
            port: 2381
            scheme: HTTP
          initialDelaySeconds: 10
          periodSeconds: 10
          successThreshold: 1
          timeoutSeconds: 15
        name: etcd
        readinessProbe:
          failureThreshold: 3
          httpGet:
            host: 127.0.0.1
            path: /readyz
            port: 2381
            scheme: HTTP
          periodSeconds: 1
          successThreshold: 1
          timeoutSeconds: 15
        resources:
          requests:
            cpu: 100m
            memory: 100Mi
        startupProbe:
          failureThreshold: 24
          httpGet:
            host: 127.0.0.1
            path: /readyz
            port: 2381
            scheme: HTTP
          initialDelaySeconds: 10
          periodSeconds: 10
          successThreshold: 1
          timeoutSeconds: 15
        terminationMessagePath: /dev/termination-log
        terminationMessagePolicy: File
        volumeMounts:
        - mountPath: /var/lib/minikube/etcd
          name: etcd-data
        - mountPath: /var/lib/minikube/certs/etcd
          name: etcd-certs
      dnsPolicy: ClusterFirst
      enableServiceLinks: true
      hostNetwork: true
      nodeName: minikube
      preemptionPolicy: PreemptLowerPriority
      priority: 2000001000
      priorityClassName: system-node-critical
      restartPolicy: Always
      schedulerName: default-scheduler
      securityContext:
        seccompProfile:
          type: RuntimeDefault
      terminationGracePeriodSeconds: 30
      tolerations:
      - effect: NoExecute
        operator: Exists
      volumes:
      - hostPath:
          path: /var/lib/minikube/certs/etcd
          type: DirectoryOrCreate
        name: etcd-certs
      - hostPath:
          path: /var/lib/minikube/etcd
          type: DirectoryOrCreate
        name: etcd-data
    status:
      conditions:
      - lastProbeTime: null
        lastTransitionTime: "2024-12-30T11:15:07Z"
        status: "True"
        type: PodReadyToStartContainers
      - lastProbeTime: null
        lastTransitionTime: "2024-12-30T09:46:19Z"
        status: "True"
        type: Initialized
      - lastProbeTime: null
        lastTransitionTime: "2024-12-30T11:15:18Z"
        status: "True"
        type: Ready
      - lastProbeTime: null
        lastTransitionTime: "2024-12-30T11:15:18Z"
        status: "True"
        type: ContainersReady
      - lastProbeTime: null
        lastTransitionTime: "2024-12-30T09:46:19Z"
        status: "True"
        type: PodScheduled
      containerStatuses:
      - containerID: docker://b489c901f43414e2ab3999495d6bb569a76c3d7b1bab9b2855e6cb185fe668a1
        image: registry.k8s.io/etcd:3.5.15-0
        imageID: docker-pullable://registry.k8s.io/etcd@sha256:a6dc63e6e8cfa0307d7851762fa6b629afb18f28d8aa3fab5a6e91b4af60026a
        lastState:
          terminated:
            containerID: docker://cc98027ab220a6fd1d83fa5445cea64f96def693bd8fc099e92813fc1712b3e5
            exitCode: 0
            finishedAt: "2024-12-30T11:14:44Z"
            reason: Completed
            startedAt: "2024-12-30T09:46:13Z"
        name: etcd
        ready: true
        restartCount: 1
        started: true
        state:
          running:
            startedAt: "2024-12-30T11:15:00Z"
      hostIP: 192.168.49.2
      hostIPs:
      - ip: 192.168.49.2
      phase: Running
      podIP: 192.168.49.2
      podIPs:
      - ip: 192.168.49.2
      qosClass: Burstable
      startTime: "2024-12-30T09:46:19Z"
  - apiVersion: v1
    kind: Pod
    metadata:
      annotations:
        kubeadm.kubernetes.io/kube-apiserver.advertise-address.endpoint: 192.168.49.2:8443
        kubernetes.io/config.hash: 9e315b3a91fa9f6f7463439d9dac1a56
        kubernetes.io/config.mirror: 9e315b3a91fa9f6f7463439d9dac1a56
        kubernetes.io/config.seen: "2024-12-30T09:46:12.634020784Z"
        kubernetes.io/config.source: file
      creationTimestamp: "2024-12-30T09:46:18Z"
      labels:
        component: kube-apiserver
        tier: control-plane
      name: kube-apiserver-minikube
      namespace: kube-system
      ownerReferences:
      - apiVersion: v1
        controller: true
        kind: Node
        name: minikube
        uid: 441abd8e-19ba-4c09-b5a9-7c27af9db6c0
      resourceVersion: "5482"
      uid: 528ccfea-0d37-45ef-9504-01ab32610936
    spec:
      containers:
      - command:
        - kube-apiserver
        - --advertise-address=192.168.49.2
        - --allow-privileged=true
        - --authorization-mode=Node,RBAC
        - --client-ca-file=/var/lib/minikube/certs/ca.crt
        - --enable-admission-plugins=NamespaceLifecycle,LimitRanger,ServiceAccount,DefaultStorageClass,DefaultTolerationSeconds,NodeRestriction,MutatingAdmissionWebhook,ValidatingAdmissionWebhook,ResourceQuota
        - --enable-bootstrap-token-auth=true
        - --etcd-cafile=/var/lib/minikube/certs/etcd/ca.crt
        - --etcd-certfile=/var/lib/minikube/certs/apiserver-etcd-client.crt
        - --etcd-keyfile=/var/lib/minikube/certs/apiserver-etcd-client.key
        - --etcd-servers=https://127.0.0.1:2379
        - --kubelet-client-certificate=/var/lib/minikube/certs/apiserver-kubelet-client.crt
        - --kubelet-client-key=/var/lib/minikube/certs/apiserver-kubelet-client.key
        - --kubelet-preferred-address-types=InternalIP,ExternalIP,Hostname
        - --proxy-client-cert-file=/var/lib/minikube/certs/front-proxy-client.crt
        - --proxy-client-key-file=/var/lib/minikube/certs/front-proxy-client.key
        - --requestheader-allowed-names=front-proxy-client
        - --requestheader-client-ca-file=/var/lib/minikube/certs/front-proxy-ca.crt
        - --requestheader-extra-headers-prefix=X-Remote-Extra-
        - --requestheader-group-headers=X-Remote-Group
        - --requestheader-username-headers=X-Remote-User
        - --secure-port=8443
        - --service-account-issuer=https://kubernetes.default.svc.cluster.local
        - --service-account-key-file=/var/lib/minikube/certs/sa.pub
        - --service-account-signing-key-file=/var/lib/minikube/certs/sa.key
        - --service-cluster-ip-range=10.96.0.0/12
        - --tls-cert-file=/var/lib/minikube/certs/apiserver.crt
        - --tls-private-key-file=/var/lib/minikube/certs/apiserver.key
        image: registry.k8s.io/kube-apiserver:v1.31.0
        imagePullPolicy: IfNotPresent
        livenessProbe:
          failureThreshold: 8
          httpGet:
            host: 192.168.49.2
            path: /livez
            port: 8443
            scheme: HTTPS
          initialDelaySeconds: 10
          periodSeconds: 10
          successThreshold: 1
          timeoutSeconds: 15
        name: kube-apiserver
        readinessProbe:
          failureThreshold: 3
          httpGet:
            host: 192.168.49.2
            path: /readyz
            port: 8443
            scheme: HTTPS
          periodSeconds: 1
          successThreshold: 1
          timeoutSeconds: 15
        resources:
          requests:
            cpu: 250m
        startupProbe:
          failureThreshold: 24
          httpGet:
            host: 192.168.49.2
            path: /livez
            port: 8443
            scheme: HTTPS
          initialDelaySeconds: 10
          periodSeconds: 10
          successThreshold: 1
          timeoutSeconds: 15
        terminationMessagePath: /dev/termination-log
        terminationMessagePolicy: File
        volumeMounts:
        - mountPath: /etc/ssl/certs
          name: ca-certs
          readOnly: true
        - mountPath: /etc/ca-certificates
          name: etc-ca-certificates
          readOnly: true
        - mountPath: /var/lib/minikube/certs
          name: k8s-certs
          readOnly: true
        - mountPath: /usr/local/share/ca-certificates
          name: usr-local-share-ca-certificates
          readOnly: true
        - mountPath: /usr/share/ca-certificates
          name: usr-share-ca-certificates
          readOnly: true
      dnsPolicy: ClusterFirst
      enableServiceLinks: true
      hostNetwork: true
      nodeName: minikube
      preemptionPolicy: PreemptLowerPriority
      priority: 2000001000
      priorityClassName: system-node-critical
      restartPolicy: Always
      schedulerName: default-scheduler
      securityContext:
        seccompProfile:
          type: RuntimeDefault
      terminationGracePeriodSeconds: 30
      tolerations:
      - effect: NoExecute
        operator: Exists
      volumes:
      - hostPath:
          path: /etc/ssl/certs
          type: DirectoryOrCreate
        name: ca-certs
      - hostPath:
          path: /etc/ca-certificates
          type: DirectoryOrCreate
        name: etc-ca-certificates
      - hostPath:
          path: /var/lib/minikube/certs
          type: DirectoryOrCreate
        name: k8s-certs
      - hostPath:
          path: /usr/local/share/ca-certificates
          type: DirectoryOrCreate
        name: usr-local-share-ca-certificates
      - hostPath:
          path: /usr/share/ca-certificates
          type: DirectoryOrCreate
        name: usr-share-ca-certificates
    status:
      conditions:
      - lastProbeTime: null
        lastTransitionTime: "2024-12-30T11:15:03Z"
        status: "True"
        type: PodReadyToStartContainers
      - lastProbeTime: null
        lastTransitionTime: "2024-12-30T09:46:19Z"
        status: "True"
        type: Initialized
      - lastProbeTime: null
        lastTransitionTime: "2024-12-30T11:15:50Z"
        status: "True"
        type: Ready
      - lastProbeTime: null
        lastTransitionTime: "2024-12-30T11:15:50Z"
        status: "True"
        type: ContainersReady
      - lastProbeTime: null
        lastTransitionTime: "2024-12-30T09:46:19Z"
        status: "True"
        type: PodScheduled
      containerStatuses:
      - containerID: docker://161b2b81dfc91a6612b563e300e0c97885b996060be5763fa021045d7a706e0c
        image: registry.k8s.io/kube-apiserver:v1.31.0
        imageID: docker-pullable://registry.k8s.io/kube-apiserver@sha256:470179274deb9dc3a81df55cfc24823ce153147d4ebf2ed649a4f271f51eaddf
        lastState:
          terminated:
            containerID: docker://2c8a6868eea611f3033dd6050340eab6191b1186695d7ad320e226c88944e74c
            exitCode: 137
            finishedAt: "2024-12-30T11:14:51Z"
            reason: Error
            startedAt: "2024-12-30T09:46:13Z"
        name: kube-apiserver
        ready: true
        restartCount: 1
        started: true
        state:
          running:
            startedAt: "2024-12-30T11:15:00Z"
      hostIP: 192.168.49.2
      hostIPs:
      - ip: 192.168.49.2
      phase: Running
      podIP: 192.168.49.2
      podIPs:
      - ip: 192.168.49.2
      qosClass: Burstable
      startTime: "2024-12-30T09:46:19Z"
  - apiVersion: v1
    kind: Pod
    metadata:
      annotations:
        kubernetes.io/config.hash: 40f5f661ab65f2e4bfe41ac2993c01de
        kubernetes.io/config.mirror: 40f5f661ab65f2e4bfe41ac2993c01de
        kubernetes.io/config.seen: "2024-12-30T09:46:12.634016982Z"
        kubernetes.io/config.source: file
      creationTimestamp: "2024-12-30T09:46:18Z"
      labels:
        component: kube-controller-manager
        tier: control-plane
      name: kube-controller-manager-minikube
      namespace: kube-system
      ownerReferences:
      - apiVersion: v1
        controller: true
        kind: Node
        name: minikube
        uid: 441abd8e-19ba-4c09-b5a9-7c27af9db6c0
      resourceVersion: "5384"
      uid: f178c1d7-8e69-47fc-9898-62f38b26e159
    spec:
      containers:
      - command:
        - kube-controller-manager
        - --allocate-node-cidrs=true
        - --authentication-kubeconfig=/etc/kubernetes/controller-manager.conf
        - --authorization-kubeconfig=/etc/kubernetes/controller-manager.conf
        - --bind-address=127.0.0.1
        - --client-ca-file=/var/lib/minikube/certs/ca.crt
        - --cluster-cidr=10.244.0.0/16
        - --cluster-name=mk
        - --cluster-signing-cert-file=/var/lib/minikube/certs/ca.crt
        - --cluster-signing-key-file=/var/lib/minikube/certs/ca.key
        - --controllers=*,bootstrapsigner,tokencleaner
        - --kubeconfig=/etc/kubernetes/controller-manager.conf
        - --leader-elect=false
        - --requestheader-client-ca-file=/var/lib/minikube/certs/front-proxy-ca.crt
        - --root-ca-file=/var/lib/minikube/certs/ca.crt
        - --service-account-private-key-file=/var/lib/minikube/certs/sa.key
        - --service-cluster-ip-range=10.96.0.0/12
        - --use-service-account-credentials=true
        image: registry.k8s.io/kube-controller-manager:v1.31.0
        imagePullPolicy: IfNotPresent
        livenessProbe:
          failureThreshold: 8
          httpGet:
            host: 127.0.0.1
            path: /healthz
            port: 10257
            scheme: HTTPS
          initialDelaySeconds: 10
          periodSeconds: 10
          successThreshold: 1
          timeoutSeconds: 15
        name: kube-controller-manager
        resources:
          requests:
            cpu: 200m
        startupProbe:
          failureThreshold: 24
          httpGet:
            host: 127.0.0.1
            path: /healthz
            port: 10257
            scheme: HTTPS
          initialDelaySeconds: 10
          periodSeconds: 10
          successThreshold: 1
          timeoutSeconds: 15
        terminationMessagePath: /dev/termination-log
        terminationMessagePolicy: File
        volumeMounts:
        - mountPath: /etc/ssl/certs
          name: ca-certs
          readOnly: true
        - mountPath: /etc/ca-certificates
          name: etc-ca-certificates
          readOnly: true
        - mountPath: /usr/libexec/kubernetes/kubelet-plugins/volume/exec
          name: flexvolume-dir
        - mountPath: /var/lib/minikube/certs
          name: k8s-certs
          readOnly: true
        - mountPath: /etc/kubernetes/controller-manager.conf
          name: kubeconfig
          readOnly: true
        - mountPath: /usr/local/share/ca-certificates
          name: usr-local-share-ca-certificates
          readOnly: true
        - mountPath: /usr/share/ca-certificates
          name: usr-share-ca-certificates
          readOnly: true
      dnsPolicy: ClusterFirst
      enableServiceLinks: true
      hostNetwork: true
      nodeName: minikube
      preemptionPolicy: PreemptLowerPriority
      priority: 2000001000
      priorityClassName: system-node-critical
      restartPolicy: Always
      schedulerName: default-scheduler
      securityContext:
        seccompProfile:
          type: RuntimeDefault
      terminationGracePeriodSeconds: 30
      tolerations:
      - effect: NoExecute
        operator: Exists
      volumes:
      - hostPath:
          path: /etc/ssl/certs
          type: DirectoryOrCreate
        name: ca-certs
      - hostPath:
          path: /etc/ca-certificates
          type: DirectoryOrCreate
        name: etc-ca-certificates
      - hostPath:
          path: /usr/libexec/kubernetes/kubelet-plugins/volume/exec
          type: DirectoryOrCreate
        name: flexvolume-dir
      - hostPath:
          path: /var/lib/minikube/certs
          type: DirectoryOrCreate
        name: k8s-certs
      - hostPath:
          path: /etc/kubernetes/controller-manager.conf
          type: FileOrCreate
        name: kubeconfig
      - hostPath:
          path: /usr/local/share/ca-certificates
          type: DirectoryOrCreate
        name: usr-local-share-ca-certificates
      - hostPath:
          path: /usr/share/ca-certificates
          type: DirectoryOrCreate
        name: usr-share-ca-certificates
    status:
      conditions:
      - lastProbeTime: null
        lastTransitionTime: "2024-12-30T11:15:04Z"
        status: "True"
        type: PodReadyToStartContainers
      - lastProbeTime: null
        lastTransitionTime: "2024-12-30T09:46:19Z"
        status: "True"
        type: Initialized
      - lastProbeTime: null
        lastTransitionTime: "2024-12-30T11:15:24Z"
        status: "True"
        type: Ready
      - lastProbeTime: null
        lastTransitionTime: "2024-12-30T11:15:24Z"
        status: "True"
        type: ContainersReady
      - lastProbeTime: null
        lastTransitionTime: "2024-12-30T09:46:19Z"
        status: "True"
        type: PodScheduled
      containerStatuses:
      - containerID: docker://df6eb4dc38cf4a7c65d59738fa60d9b31d802a7936db7ca5572b50d98111dc38
        image: registry.k8s.io/kube-controller-manager:v1.31.0
        imageID: docker-pullable://registry.k8s.io/kube-controller-manager@sha256:f6f3c33dda209e8434b83dacf5244c03b59b0018d93325ff21296a142b68497d
        lastState:
          terminated:
            containerID: docker://3d544ceae582cf6acdd061ba479cc06170bdf2a52608e1127bff80fe9b6d2471
            exitCode: 2
            finishedAt: "2024-12-30T11:14:44Z"
            reason: Error
            startedAt: "2024-12-30T09:46:13Z"
        name: kube-controller-manager
        ready: true
        restartCount: 1
        started: true
        state:
          running:
            startedAt: "2024-12-30T11:14:59Z"
      hostIP: 192.168.49.2
      hostIPs:
      - ip: 192.168.49.2
      phase: Running
      podIP: 192.168.49.2
      podIPs:
      - ip: 192.168.49.2
      qosClass: Burstable
      startTime: "2024-12-30T09:46:19Z"
  - apiVersion: v1
    kind: Pod
    metadata:
      creationTimestamp: "2024-12-30T09:46:24Z"
      generateName: kube-proxy-
      labels:
        controller-revision-hash: 5976bc5f75
        k8s-app: kube-proxy
        pod-template-generation: "1"
      name: kube-proxy-gcdrz
      namespace: kube-system
      ownerReferences:
      - apiVersion: apps/v1
        blockOwnerDeletion: true
        controller: true
        kind: DaemonSet
        name: kube-proxy
        uid: 46b4a363-ef53-42bf-85be-c7329f1ae879
      resourceVersion: "5371"
      uid: 92b4ee28-607b-4112-a0dc-c094248bb753
    spec:
      affinity:
        nodeAffinity:
          requiredDuringSchedulingIgnoredDuringExecution:
            nodeSelectorTerms:
            - matchFields:
              - key: metadata.name
                operator: In
                values:
                - minikube
      containers:
      - command:
        - /usr/local/bin/kube-proxy
        - --config=/var/lib/kube-proxy/config.conf
        - --hostname-override=$(NODE_NAME)
        env:
        - name: NODE_NAME
          valueFrom:
            fieldRef:
              apiVersion: v1
              fieldPath: spec.nodeName
        image: registry.k8s.io/kube-proxy:v1.31.0
        imagePullPolicy: IfNotPresent
        name: kube-proxy
        resources: {}
        securityContext:
          privileged: true
        terminationMessagePath: /dev/termination-log
        terminationMessagePolicy: File
        volumeMounts:
        - mountPath: /var/lib/kube-proxy
          name: kube-proxy
        - mountPath: /run/xtables.lock
          name: xtables-lock
        - mountPath: /lib/modules
          name: lib-modules
          readOnly: true
        - mountPath: /var/run/secrets/kubernetes.io/serviceaccount
          name: kube-api-access-q2ddk
          readOnly: true
      dnsPolicy: ClusterFirst
      enableServiceLinks: true
      hostNetwork: true
      nodeName: minikube
      nodeSelector:
        kubernetes.io/os: linux
      preemptionPolicy: PreemptLowerPriority
      priority: 2000001000
      priorityClassName: system-node-critical
      restartPolicy: Always
      schedulerName: default-scheduler
      securityContext: {}
      serviceAccount: kube-proxy
      serviceAccountName: kube-proxy
      terminationGracePeriodSeconds: 30
      tolerations:
      - operator: Exists
      - effect: NoExecute
        key: node.kubernetes.io/not-ready
        operator: Exists
      - effect: NoExecute
        key: node.kubernetes.io/unreachable
        operator: Exists
      - effect: NoSchedule
        key: node.kubernetes.io/disk-pressure
        operator: Exists
      - effect: NoSchedule
        key: node.kubernetes.io/memory-pressure
        operator: Exists
      - effect: NoSchedule
        key: node.kubernetes.io/pid-pressure
        operator: Exists
      - effect: NoSchedule
        key: node.kubernetes.io/unschedulable
        operator: Exists
      - effect: NoSchedule
        key: node.kubernetes.io/network-unavailable
        operator: Exists
      volumes:
      - configMap:
          defaultMode: 420
          name: kube-proxy
        name: kube-proxy
      - hostPath:
          path: /run/xtables.lock
          type: FileOrCreate
        name: xtables-lock
      - hostPath:
          path: /lib/modules
          type: ""
        name: lib-modules
      - name: kube-api-access-q2ddk
        projected:
          defaultMode: 420
          sources:
          - serviceAccountToken:
              expirationSeconds: 3607
              path: token
          - configMap:
              items:
              - key: ca.crt
                path: ca.crt
              name: kube-root-ca.crt
          - downwardAPI:
              items:
              - fieldRef:
                  apiVersion: v1
                  fieldPath: metadata.namespace
                path: namespace
    status:
      conditions:
      - lastProbeTime: null
        lastTransitionTime: "2024-12-30T11:15:04Z"
        status: "True"
        type: PodReadyToStartContainers
      - lastProbeTime: null
        lastTransitionTime: "2024-12-30T09:46:24Z"
        status: "True"
        type: Initialized
      - lastProbeTime: null
        lastTransitionTime: "2024-12-30T11:15:04Z"
        status: "True"
        type: Ready
      - lastProbeTime: null
        lastTransitionTime: "2024-12-30T11:15:04Z"
        status: "True"
        type: ContainersReady
      - lastProbeTime: null
        lastTransitionTime: "2024-12-30T09:46:24Z"
        status: "True"
        type: PodScheduled
      containerStatuses:
      - containerID: docker://5becf807f6b88dd1c02c46e507d65b46a052b75a14fd570fad16f10ffe1e931b
        image: registry.k8s.io/kube-proxy:v1.31.0
        imageID: docker-pullable://registry.k8s.io/kube-proxy@sha256:c727efb1c6f15a68060bf7f207f5c7a765355b7e3340c513e582ec819c5cd2fe
        lastState:
          terminated:
            containerID: docker://66d74560fc50524dd7e4f6ab821c1151cffd5ec25bb3b8a6b0338c84e1542921
            exitCode: 2
            finishedAt: "2024-12-30T11:14:43Z"
            reason: Error
            startedAt: "2024-12-30T09:46:26Z"
        name: kube-proxy
        ready: true
        restartCount: 1
        started: true
        state:
          running:
            startedAt: "2024-12-30T11:15:00Z"
        volumeMounts:
        - mountPath: /var/lib/kube-proxy
          name: kube-proxy
        - mountPath: /run/xtables.lock
          name: xtables-lock
        - mountPath: /lib/modules
          name: lib-modules
          readOnly: true
          recursiveReadOnly: Disabled
        - mountPath: /var/run/secrets/kubernetes.io/serviceaccount
          name: kube-api-access-q2ddk
          readOnly: true
          recursiveReadOnly: Disabled
      hostIP: 192.168.49.2
      hostIPs:
      - ip: 192.168.49.2
      phase: Running
      podIP: 192.168.49.2
      podIPs:
      - ip: 192.168.49.2
      qosClass: BestEffort
      startTime: "2024-12-30T09:46:24Z"
  - apiVersion: v1
    kind: Pod
    metadata:
      annotations:
        kubernetes.io/config.hash: e039200acb850c82bb901653cc38ff6e
        kubernetes.io/config.mirror: e039200acb850c82bb901653cc38ff6e
        kubernetes.io/config.seen: "2024-12-30T09:46:19.596804243Z"
        kubernetes.io/config.source: file
      creationTimestamp: "2024-12-30T09:46:19Z"
      labels:
        component: kube-scheduler
        tier: control-plane
      name: kube-scheduler-minikube
      namespace: kube-system
      ownerReferences:
      - apiVersion: v1
        controller: true
        kind: Node
        name: minikube
        uid: 441abd8e-19ba-4c09-b5a9-7c27af9db6c0
      resourceVersion: "5382"
      uid: aa91dd14-09c2-4f3d-96dc-8159abd5f315
    spec:
      containers:
      - command:
        - kube-scheduler
        - --authentication-kubeconfig=/etc/kubernetes/scheduler.conf
        - --authorization-kubeconfig=/etc/kubernetes/scheduler.conf
        - --bind-address=127.0.0.1
        - --kubeconfig=/etc/kubernetes/scheduler.conf
        - --leader-elect=false
        image: registry.k8s.io/kube-scheduler:v1.31.0
        imagePullPolicy: IfNotPresent
        livenessProbe:
          failureThreshold: 8
          httpGet:
            host: 127.0.0.1
            path: /healthz
            port: 10259
            scheme: HTTPS
          initialDelaySeconds: 10
          periodSeconds: 10
          successThreshold: 1
          timeoutSeconds: 15
        name: kube-scheduler
        resources:
          requests:
            cpu: 100m
        startupProbe:
          failureThreshold: 24
          httpGet:
            host: 127.0.0.1
            path: /healthz
            port: 10259
            scheme: HTTPS
          initialDelaySeconds: 10
          periodSeconds: 10
          successThreshold: 1
          timeoutSeconds: 15
        terminationMessagePath: /dev/termination-log
        terminationMessagePolicy: File
        volumeMounts:
        - mountPath: /etc/kubernetes/scheduler.conf
          name: kubeconfig
          readOnly: true
      dnsPolicy: ClusterFirst
      enableServiceLinks: true
      hostNetwork: true
      nodeName: minikube
      preemptionPolicy: PreemptLowerPriority
      priority: 2000001000
      priorityClassName: system-node-critical
      restartPolicy: Always
      schedulerName: default-scheduler
      securityContext:
        seccompProfile:
          type: RuntimeDefault
      terminationGracePeriodSeconds: 30
      tolerations:
      - effect: NoExecute
        operator: Exists
      volumes:
      - hostPath:
          path: /etc/kubernetes/scheduler.conf
          type: FileOrCreate
        name: kubeconfig
    status:
      conditions:
      - lastProbeTime: null
        lastTransitionTime: "2024-12-30T11:15:07Z"
        status: "True"
        type: PodReadyToStartContainers
      - lastProbeTime: null
        lastTransitionTime: "2024-12-30T09:46:19Z"
        status: "True"
        type: Initialized
      - lastProbeTime: null
        lastTransitionTime: "2024-12-30T11:15:36Z"
        status: "True"
        type: Ready
      - lastProbeTime: null
        lastTransitionTime: "2024-12-30T11:15:36Z"
        status: "True"
        type: ContainersReady
      - lastProbeTime: null
        lastTransitionTime: "2024-12-30T09:46:19Z"
        status: "True"
        type: PodScheduled
      containerStatuses:
      - containerID: docker://1d3b500373c0e6282b0dc0283165955d6c40f97b089b3a15069d60fed096f730
        image: registry.k8s.io/kube-scheduler:v1.31.0
        imageID: docker-pullable://registry.k8s.io/kube-scheduler@sha256:96ddae9c9b2e79342e0551e2d2ec422c0c02629a74d928924aaa069706619808
        lastState:
          terminated:
            containerID: docker://80973d66aa31e446b09aa3f4fc237a5eef8e31961592b21f689973cb6cf00851
            exitCode: 1
            finishedAt: "2024-12-30T11:14:44Z"
            reason: Error
            startedAt: "2024-12-30T09:46:13Z"
        name: kube-scheduler
        ready: true
        restartCount: 1
        started: true
        state:
          running:
            startedAt: "2024-12-30T11:15:01Z"
      hostIP: 192.168.49.2
      hostIPs:
      - ip: 192.168.49.2
      phase: Running
      podIP: 192.168.49.2
      podIPs:
      - ip: 192.168.49.2
      qosClass: Burstable
      startTime: "2024-12-30T09:46:19Z"
  - apiVersion: v1
    kind: Pod
    metadata:
      creationTimestamp: "2024-12-30T11:25:47Z"
      generateName: metrics-server-84c5f94fbc-
      labels:
        k8s-app: metrics-server
        pod-template-hash: 84c5f94fbc
      name: metrics-server-84c5f94fbc-g8wg9
      namespace: kube-system
      ownerReferences:
      - apiVersion: apps/v1
        blockOwnerDeletion: true
        controller: true
        kind: ReplicaSet
        name: metrics-server-84c5f94fbc
        uid: c9fa0347-3429-4264-909d-616eb8aeb75f
      resourceVersion: "6399"
      uid: d0fde8de-d0d9-4f19-815b-2f94f8cd5190
    spec:
      containers:
      - args:
        - --cert-dir=/tmp
        - --secure-port=4443
        - --kubelet-preferred-address-types=InternalIP,ExternalIP,Hostname
        - --kubelet-use-node-status-port
        - --metric-resolution=60s
        - --kubelet-insecure-tls
        image: registry.k8s.io/metrics-server/metrics-server:v0.7.2@sha256:ffcb2bf004d6aa0a17d90e0247cf94f2865c8901dcab4427034c341951c239f9
        imagePullPolicy: IfNotPresent
        livenessProbe:
          failureThreshold: 3
          httpGet:
            path: /livez
            port: https
            scheme: HTTPS
          periodSeconds: 10
          successThreshold: 1
          timeoutSeconds: 1
        name: metrics-server
        ports:
        - containerPort: 4443
          name: https
          protocol: TCP
        readinessProbe:
          failureThreshold: 3
          httpGet:
            path: /readyz
            port: https
            scheme: HTTPS
          periodSeconds: 10
          successThreshold: 1
          timeoutSeconds: 1
        resources:
          requests:
            cpu: 100m
            memory: 200Mi
        securityContext:
          readOnlyRootFilesystem: true
          runAsNonRoot: true
          runAsUser: 1000
        terminationMessagePath: /dev/termination-log
        terminationMessagePolicy: File
        volumeMounts:
        - mountPath: /tmp
          name: tmp-dir
        - mountPath: /var/run/secrets/kubernetes.io/serviceaccount
          name: kube-api-access-pvfng
          readOnly: true
      dnsPolicy: ClusterFirst
      enableServiceLinks: true
      nodeName: minikube
      preemptionPolicy: PreemptLowerPriority
      priority: 2000000000
      priorityClassName: system-cluster-critical
      restartPolicy: Always
      schedulerName: default-scheduler
      securityContext: {}
      serviceAccount: metrics-server
      serviceAccountName: metrics-server
      terminationGracePeriodSeconds: 30
      tolerations:
      - effect: NoExecute
        key: node.kubernetes.io/not-ready
        operator: Exists
        tolerationSeconds: 300
      - effect: NoExecute
        key: node.kubernetes.io/unreachable
        operator: Exists
        tolerationSeconds: 300
      volumes:
      - emptyDir: {}
        name: tmp-dir
      - name: kube-api-access-pvfng
        projected:
          defaultMode: 420
          sources:
          - serviceAccountToken:
              expirationSeconds: 3607
              path: token
          - configMap:
              items:
              - key: ca.crt
                path: ca.crt
              name: kube-root-ca.crt
          - downwardAPI:
              items:
              - fieldRef:
                  apiVersion: v1
                  fieldPath: metadata.namespace
                path: namespace
    status:
      conditions:
      - lastProbeTime: null
        lastTransitionTime: "2024-12-30T11:26:30Z"
        status: "True"
        type: PodReadyToStartContainers
      - lastProbeTime: null
        lastTransitionTime: "2024-12-30T11:25:47Z"
        status: "True"
        type: Initialized
      - lastProbeTime: null
        lastTransitionTime: "2024-12-30T11:26:30Z"
        status: "True"
        type: Ready
      - lastProbeTime: null
        lastTransitionTime: "2024-12-30T11:26:30Z"
        status: "True"
        type: ContainersReady
      - lastProbeTime: null
        lastTransitionTime: "2024-12-30T11:25:47Z"
        status: "True"
        type: PodScheduled
      containerStatuses:
      - containerID: docker://ff5dd69404262a7b43b8ac9e961b81f049cceddb3c180e36bf218451be5950b9
        image: registry.k8s.io/metrics-server/metrics-server@sha256:ffcb2bf004d6aa0a17d90e0247cf94f2865c8901dcab4427034c341951c239f9
        imageID: docker-pullable://registry.k8s.io/metrics-server/metrics-server@sha256:ffcb2bf004d6aa0a17d90e0247cf94f2865c8901dcab4427034c341951c239f9
        lastState: {}
        name: metrics-server
        ready: true
        restartCount: 0
        started: true
        state:
          running:
            startedAt: "2024-12-30T11:26:29Z"
        volumeMounts:
        - mountPath: /tmp
          name: tmp-dir
        - mountPath: /var/run/secrets/kubernetes.io/serviceaccount
          name: kube-api-access-pvfng
          readOnly: true
          recursiveReadOnly: Disabled
      hostIP: 192.168.49.2
      hostIPs:
      - ip: 192.168.49.2
      phase: Running
      podIP: 10.244.0.33
      podIPs:
      - ip: 10.244.0.33
      qosClass: Burstable
      startTime: "2024-12-30T11:25:47Z"
  - apiVersion: v1
    kind: Pod
    metadata:
      annotations:
        kubectl.kubernetes.io/last-applied-configuration: |
          {"apiVersion":"v1","kind":"Pod","metadata":{"annotations":{},"labels":{"addonmanager.kubernetes.io/mode":"Reconcile","integration-test":"storage-provisioner"},"name":"storage-provisioner","namespace":"kube-system"},"spec":{"containers":[{"command":["/storage-provisioner"],"image":"gcr.io/k8s-minikube/storage-provisioner:v5","imagePullPolicy":"IfNotPresent","name":"storage-provisioner","volumeMounts":[{"mountPath":"/tmp","name":"tmp"}]}],"hostNetwork":true,"serviceAccountName":"storage-provisioner","volumes":[{"hostPath":{"path":"/tmp","type":"Directory"},"name":"tmp"}]}}
      creationTimestamp: "2024-12-30T09:46:21Z"
      labels:
        addonmanager.kubernetes.io/mode: Reconcile
        integration-test: storage-provisioner
      name: storage-provisioner
      namespace: kube-system
      resourceVersion: "5394"
      uid: c9765c1c-906c-43ec-a7a0-e9fd55430fac
    spec:
      containers:
      - command:
        - /storage-provisioner
        image: gcr.io/k8s-minikube/storage-provisioner:v5
        imagePullPolicy: IfNotPresent
        name: storage-provisioner
        resources: {}
        terminationMessagePath: /dev/termination-log
        terminationMessagePolicy: File
        volumeMounts:
        - mountPath: /tmp
          name: tmp
        - mountPath: /var/run/secrets/kubernetes.io/serviceaccount
          name: kube-api-access-dcg29
          readOnly: true
      dnsPolicy: ClusterFirst
      enableServiceLinks: true
      hostNetwork: true
      nodeName: minikube
      preemptionPolicy: PreemptLowerPriority
      priority: 0
      restartPolicy: Always
      schedulerName: default-scheduler
      securityContext: {}
      serviceAccount: storage-provisioner
      serviceAccountName: storage-provisioner
      terminationGracePeriodSeconds: 30
      tolerations:
      - effect: NoExecute
        key: node.kubernetes.io/not-ready
        operator: Exists
        tolerationSeconds: 300
      - effect: NoExecute
        key: node.kubernetes.io/unreachable
        operator: Exists
        tolerationSeconds: 300
      volumes:
      - hostPath:
          path: /tmp
          type: Directory
        name: tmp
      - name: kube-api-access-dcg29
        projected:
          defaultMode: 420
          sources:
          - serviceAccountToken:
              expirationSeconds: 3607
              path: token
          - configMap:
              items:
              - key: ca.crt
                path: ca.crt
              name: kube-root-ca.crt
          - downwardAPI:
              items:
              - fieldRef:
                  apiVersion: v1
                  fieldPath: metadata.namespace
                path: namespace
    status:
      conditions:
      - lastProbeTime: null
        lastTransitionTime: "2024-12-30T11:15:04Z"
        status: "True"
        type: PodReadyToStartContainers
      - lastProbeTime: null
        lastTransitionTime: "2024-12-30T09:46:23Z"
        status: "True"
        type: Initialized
      - lastProbeTime: null
        lastTransitionTime: "2024-12-30T11:15:32Z"
        status: "True"
        type: Ready
      - lastProbeTime: null
        lastTransitionTime: "2024-12-30T11:15:32Z"
        status: "True"
        type: ContainersReady
      - lastProbeTime: null
        lastTransitionTime: "2024-12-30T09:46:23Z"
        status: "True"
        type: PodScheduled
      containerStatuses:
      - containerID: docker://07eee010334b1e5568e9b08b66a051d620c4071472a8447d12e1be80f9417f2f
        image: gcr.io/k8s-minikube/storage-provisioner:v5
        imageID: docker-pullable://gcr.io/k8s-minikube/storage-provisioner@sha256:18eb69d1418e854ad5a19e399310e52808a8321e4c441c1dddad8977a0d7a944
        lastState:
          terminated:
            containerID: docker://b370c7207a42941aa5d1cc115d623c3ddbbafa23a5bf09646b9328e678974d74
            exitCode: 1
            finishedAt: "2024-12-30T11:15:07Z"
            reason: Error
            startedAt: "2024-12-30T11:15:00Z"
        name: storage-provisioner
        ready: true
        restartCount: 3
        started: true
        state:
          running:
            startedAt: "2024-12-30T11:15:27Z"
        volumeMounts:
        - mountPath: /tmp
          name: tmp
        - mountPath: /var/run/secrets/kubernetes.io/serviceaccount
          name: kube-api-access-dcg29
          readOnly: true
          recursiveReadOnly: Disabled
      hostIP: 192.168.49.2
      hostIPs:
      - ip: 192.168.49.2
      phase: Running
      podIP: 192.168.49.2
      podIPs:
      - ip: 192.168.49.2
      qosClass: BestEffort
      startTime: "2024-12-30T09:46:23Z"
  - apiVersion: v1
    kind: Pod
    metadata:
      annotations:
        seccomp.security.alpha.kubernetes.io/pod: runtime/default
      creationTimestamp: "2024-12-30T11:25:40Z"
      generateName: dashboard-metrics-scraper-c5db448b4-
      labels:
        k8s-app: dashboard-metrics-scraper
        pod-template-hash: c5db448b4
      name: dashboard-metrics-scraper-c5db448b4-vh922
      namespace: kubernetes-dashboard
      ownerReferences:
      - apiVersion: apps/v1
        blockOwnerDeletion: true
        controller: true
        kind: ReplicaSet
        name: dashboard-metrics-scraper-c5db448b4
        uid: db1e6382-e320-45a5-9e35-70ebb342da9c
      resourceVersion: "6377"
      uid: dfc45fde-3bfa-40ad-b915-fa995037e7f0
    spec:
      containers:
      - image: docker.io/kubernetesui/metrics-scraper:v1.0.8@sha256:76049887f07a0476dc93efc2d3569b9529bf982b22d29f356092ce206e98765c
        imagePullPolicy: IfNotPresent
        livenessProbe:
          failureThreshold: 3
          httpGet:
            path: /
            port: 8000
            scheme: HTTP
          initialDelaySeconds: 30
          periodSeconds: 10
          successThreshold: 1
          timeoutSeconds: 30
        name: dashboard-metrics-scraper
        ports:
        - containerPort: 8000
          protocol: TCP
        resources: {}
        securityContext:
          allowPrivilegeEscalation: false
          readOnlyRootFilesystem: true
          runAsGroup: 2001
          runAsUser: 1001
        terminationMessagePath: /dev/termination-log
        terminationMessagePolicy: File
        volumeMounts:
        - mountPath: /tmp
          name: tmp-volume
        - mountPath: /var/run/secrets/kubernetes.io/serviceaccount
          name: kube-api-access-sn2gp
          readOnly: true
      dnsPolicy: ClusterFirst
      enableServiceLinks: true
      nodeName: minikube
      nodeSelector:
        kubernetes.io/os: linux
      preemptionPolicy: PreemptLowerPriority
      priority: 0
      restartPolicy: Always
      schedulerName: default-scheduler
      securityContext: {}
      serviceAccount: kubernetes-dashboard
      serviceAccountName: kubernetes-dashboard
      terminationGracePeriodSeconds: 30
      tolerations:
      - effect: NoSchedule
        key: node-role.kubernetes.io/master
      - effect: NoExecute
        key: node.kubernetes.io/not-ready
        operator: Exists
        tolerationSeconds: 300
      - effect: NoExecute
        key: node.kubernetes.io/unreachable
        operator: Exists
        tolerationSeconds: 300
      volumes:
      - emptyDir: {}
        name: tmp-volume
      - name: kube-api-access-sn2gp
        projected:
          defaultMode: 420
          sources:
          - serviceAccountToken:
              expirationSeconds: 3607
              path: token
          - configMap:
              items:
              - key: ca.crt
                path: ca.crt
              name: kube-root-ca.crt
          - downwardAPI:
              items:
              - fieldRef:
                  apiVersion: v1
                  fieldPath: metadata.namespace
                path: namespace
    status:
      conditions:
      - lastProbeTime: null
        lastTransitionTime: "2024-12-30T11:26:18Z"
        status: "True"
        type: PodReadyToStartContainers
      - lastProbeTime: null
        lastTransitionTime: "2024-12-30T11:25:40Z"
        status: "True"
        type: Initialized
      - lastProbeTime: null
        lastTransitionTime: "2024-12-30T11:26:18Z"
        status: "True"
        type: Ready
      - lastProbeTime: null
        lastTransitionTime: "2024-12-30T11:26:18Z"
        status: "True"
        type: ContainersReady
      - lastProbeTime: null
        lastTransitionTime: "2024-12-30T11:25:40Z"
        status: "True"
        type: PodScheduled
      containerStatuses:
      - containerID: docker://0f830d0062627e3635ba3deaa05c29116f1edb08548a8d047a439e2a7f8a4947
        image: kubernetesui/metrics-scraper@sha256:76049887f07a0476dc93efc2d3569b9529bf982b22d29f356092ce206e98765c
        imageID: docker-pullable://kubernetesui/metrics-scraper@sha256:76049887f07a0476dc93efc2d3569b9529bf982b22d29f356092ce206e98765c
        lastState: {}
        name: dashboard-metrics-scraper
        ready: true
        restartCount: 0
        started: true
        state:
          running:
            startedAt: "2024-12-30T11:26:18Z"
        volumeMounts:
        - mountPath: /tmp
          name: tmp-volume
        - mountPath: /var/run/secrets/kubernetes.io/serviceaccount
          name: kube-api-access-sn2gp
          readOnly: true
          recursiveReadOnly: Disabled
      hostIP: 192.168.49.2
      hostIPs:
      - ip: 192.168.49.2
      phase: Running
      podIP: 10.244.0.32
      podIPs:
      - ip: 10.244.0.32
      qosClass: BestEffort
      startTime: "2024-12-30T11:25:40Z"
  - apiVersion: v1
    kind: Pod
    metadata:
      creationTimestamp: "2024-12-30T11:25:40Z"
      generateName: kubernetes-dashboard-695b96c756-
      labels:
        gcp-auth-skip-secret: "true"
        k8s-app: kubernetes-dashboard
        pod-template-hash: 695b96c756
      name: kubernetes-dashboard-695b96c756-rzvk9
      namespace: kubernetes-dashboard
      ownerReferences:
      - apiVersion: apps/v1
        blockOwnerDeletion: true
        controller: true
        kind: ReplicaSet
        name: kubernetes-dashboard-695b96c756
        uid: 9d69dee3-6365-4ad7-9f63-26d13535392d
      resourceVersion: "6359"
      uid: 804093e8-b5c9-4786-9624-825aac3594ff
    spec:
      containers:
      - args:
        - --namespace=kubernetes-dashboard
        - --enable-skip-login
        - --disable-settings-authorizer
        image: docker.io/kubernetesui/dashboard:v2.7.0@sha256:2e500d29e9d5f4a086b908eb8dfe7ecac57d2ab09d65b24f588b1d449841ef93
        imagePullPolicy: IfNotPresent
        livenessProbe:
          failureThreshold: 3
          httpGet:
            path: /
            port: 9090
            scheme: HTTP
          initialDelaySeconds: 30
          periodSeconds: 10
          successThreshold: 1
          timeoutSeconds: 30
        name: kubernetes-dashboard
        ports:
        - containerPort: 9090
          protocol: TCP
        resources: {}
        securityContext:
          allowPrivilegeEscalation: false
          readOnlyRootFilesystem: true
          runAsGroup: 2001
          runAsUser: 1001
        terminationMessagePath: /dev/termination-log
        terminationMessagePolicy: File
        volumeMounts:
        - mountPath: /tmp
          name: tmp-volume
        - mountPath: /var/run/secrets/kubernetes.io/serviceaccount
          name: kube-api-access-5wk2r
          readOnly: true
      dnsPolicy: ClusterFirst
      enableServiceLinks: true
      nodeName: minikube
      nodeSelector:
        kubernetes.io/os: linux
      preemptionPolicy: PreemptLowerPriority
      priority: 0
      restartPolicy: Always
      schedulerName: default-scheduler
      securityContext: {}
      serviceAccount: kubernetes-dashboard
      serviceAccountName: kubernetes-dashboard
      terminationGracePeriodSeconds: 30
      tolerations:
      - effect: NoSchedule
        key: node-role.kubernetes.io/master
      - effect: NoExecute
        key: node.kubernetes.io/not-ready
        operator: Exists
        tolerationSeconds: 300
      - effect: NoExecute
        key: node.kubernetes.io/unreachable
        operator: Exists
        tolerationSeconds: 300
      volumes:
      - emptyDir: {}
        name: tmp-volume
      - name: kube-api-access-5wk2r
        projected:
          defaultMode: 420
          sources:
          - serviceAccountToken:
              expirationSeconds: 3607
              path: token
          - configMap:
              items:
              - key: ca.crt
                path: ca.crt
              name: kube-root-ca.crt
          - downwardAPI:
              items:
              - fieldRef:
                  apiVersion: v1
                  fieldPath: metadata.namespace
                path: namespace
    status:
      conditions:
      - lastProbeTime: null
        lastTransitionTime: "2024-12-30T11:26:09Z"
        status: "True"
        type: PodReadyToStartContainers
      - lastProbeTime: null
        lastTransitionTime: "2024-12-30T11:25:40Z"
        status: "True"
        type: Initialized
      - lastProbeTime: null
        lastTransitionTime: "2024-12-30T11:26:09Z"
        status: "True"
        type: Ready
      - lastProbeTime: null
        lastTransitionTime: "2024-12-30T11:26:09Z"
        status: "True"
        type: ContainersReady
      - lastProbeTime: null
        lastTransitionTime: "2024-12-30T11:25:40Z"
        status: "True"
        type: PodScheduled
      containerStatuses:
      - containerID: docker://80c80db0c964cf0aea22595f84acd6992fd73bca36414d3368e0ee0e6c332294
        image: kubernetesui/dashboard@sha256:2e500d29e9d5f4a086b908eb8dfe7ecac57d2ab09d65b24f588b1d449841ef93
        imageID: docker-pullable://kubernetesui/dashboard@sha256:2e500d29e9d5f4a086b908eb8dfe7ecac57d2ab09d65b24f588b1d449841ef93
        lastState: {}
        name: kubernetes-dashboard
        ready: true
        restartCount: 0
        started: true
        state:
          running:
            startedAt: "2024-12-30T11:26:08Z"
        volumeMounts:
        - mountPath: /tmp
          name: tmp-volume
        - mountPath: /var/run/secrets/kubernetes.io/serviceaccount
          name: kube-api-access-5wk2r
          readOnly: true
          recursiveReadOnly: Disabled
      hostIP: 192.168.49.2
      hostIPs:
      - ip: 192.168.49.2
      phase: Running
      podIP: 10.244.0.31
      podIPs:
      - ip: 10.244.0.31
      qosClass: BestEffort
      startTime: "2024-12-30T11:25:40Z"
  - apiVersion: v1
    kind: Pod
    metadata:
      creationTimestamp: "2024-12-30T11:19:59Z"
      generateName: model-server-664885b79f-
      labels:
        app.kubernetes.io/name: model-server
        pod-template-hash: 664885b79f
      name: model-server-664885b79f-g7q85
      namespace: prod
      ownerReferences:
      - apiVersion: apps/v1
        blockOwnerDeletion: true
        controller: true
        kind: ReplicaSet
        name: model-server-664885b79f
        uid: f93fce3f-d8c5-43a5-acce-44781d50db32
      resourceVersion: "5862"
      uid: de280078-d53b-4f2e-b625-fd5ead994b26
    spec:
      containers:
      - env:
        - name: REDIS_HOST
          valueFrom:
            configMapKeyRef:
              key: hostname
              name: redis-config-v1
        - name: REDIS_PORT
          valueFrom:
            configMapKeyRef:
              key: port
              name: redis-config-v1
        - name: REDIS_PASSWORD
          valueFrom:
            secretKeyRef:
              key: db_password
              name: redis-secret-v1
        - name: MODEL_NAME
          valueFrom:
            configMapKeyRef:
              key: model_name
              name: model-server-config-v1
        image: model-server:latest
        imagePullPolicy: Never
        name: model-server
        ports:
        - containerPort: 80
          name: http
          protocol: TCP
        resources:
          limits:
            cpu: "1"
            memory: 2Gi
          requests:
            cpu: "1"
            memory: 2Gi
        terminationMessagePath: /dev/termination-log
        terminationMessagePolicy: File
        volumeMounts:
        - mountPath: /var/run/secrets/kubernetes.io/serviceaccount
          name: kube-api-access-k9xzz
          readOnly: true
      dnsPolicy: ClusterFirst
      enableServiceLinks: true
      nodeName: minikube
      preemptionPolicy: PreemptLowerPriority
      priority: 0
      restartPolicy: Always
      schedulerName: default-scheduler
      securityContext: {}
      serviceAccount: default
      serviceAccountName: default
      terminationGracePeriodSeconds: 30
      tolerations:
      - effect: NoExecute
        key: node.kubernetes.io/not-ready
        operator: Exists
        tolerationSeconds: 300
      - effect: NoExecute
        key: node.kubernetes.io/unreachable
        operator: Exists
        tolerationSeconds: 300
      volumes:
      - name: kube-api-access-k9xzz
        projected:
          defaultMode: 420
          sources:
          - serviceAccountToken:
              expirationSeconds: 3607
              path: token
          - configMap:
              items:
              - key: ca.crt
                path: ca.crt
              name: kube-root-ca.crt
          - downwardAPI:
              items:
              - fieldRef:
                  apiVersion: v1
                  fieldPath: metadata.namespace
                path: namespace
    status:
      conditions:
      - lastProbeTime: null
        lastTransitionTime: "2024-12-30T11:20:04Z"
        status: "True"
        type: PodReadyToStartContainers
      - lastProbeTime: null
        lastTransitionTime: "2024-12-30T11:20:00Z"
        status: "True"
        type: Initialized
      - lastProbeTime: null
        lastTransitionTime: "2024-12-30T11:20:04Z"
        status: "True"
        type: Ready
      - lastProbeTime: null
        lastTransitionTime: "2024-12-30T11:20:04Z"
        status: "True"
        type: ContainersReady
      - lastProbeTime: null
        lastTransitionTime: "2024-12-30T11:19:59Z"
        status: "True"
        type: PodScheduled
      containerStatuses:
      - containerID: docker://a434b50d85b13874aad3f7f0d3d0ced24ff5aa0cbe3a655f139029654bcb34bc
        image: model-server:latest
        imageID: docker://sha256:7b09b0acbbfa7baf666665468a5dbd930895258597ffcfa0e83ab22e09f3f57d
        lastState: {}
        name: model-server
        ready: true
        restartCount: 0
        started: true
        state:
          running:
            startedAt: "2024-12-30T11:20:02Z"
        volumeMounts:
        - mountPath: /var/run/secrets/kubernetes.io/serviceaccount
          name: kube-api-access-k9xzz
          readOnly: true
          recursiveReadOnly: Disabled
      hostIP: 192.168.49.2
      hostIPs:
      - ip: 192.168.49.2
      phase: Running
      podIP: 10.244.0.25
      podIPs:
      - ip: 10.244.0.25
      qosClass: Guaranteed
      startTime: "2024-12-30T11:20:00Z"
  - apiVersion: v1
    kind: Pod
    metadata:
      creationTimestamp: "2024-12-30T11:20:00Z"
      generateName: model-server-664885b79f-
      labels:
        app.kubernetes.io/name: model-server
        pod-template-hash: 664885b79f
      name: model-server-664885b79f-qc4ck
      namespace: prod
      ownerReferences:
      - apiVersion: apps/v1
        blockOwnerDeletion: true
        controller: true
        kind: ReplicaSet
        name: model-server-664885b79f
        uid: f93fce3f-d8c5-43a5-acce-44781d50db32
      resourceVersion: "5853"
      uid: c0c892c7-0508-4a0b-ad64-e253fe77247e
    spec:
      containers:
      - env:
        - name: REDIS_HOST
          valueFrom:
            configMapKeyRef:
              key: hostname
              name: redis-config-v1
        - name: REDIS_PORT
          valueFrom:
            configMapKeyRef:
              key: port
              name: redis-config-v1
        - name: REDIS_PASSWORD
          valueFrom:
            secretKeyRef:
              key: db_password
              name: redis-secret-v1
        - name: MODEL_NAME
          valueFrom:
            configMapKeyRef:
              key: model_name
              name: model-server-config-v1
        image: model-server:latest
        imagePullPolicy: Never
        name: model-server
        ports:
        - containerPort: 80
          name: http
          protocol: TCP
        resources:
          limits:
            cpu: "1"
            memory: 2Gi
          requests:
            cpu: "1"
            memory: 2Gi
        terminationMessagePath: /dev/termination-log
        terminationMessagePolicy: File
        volumeMounts:
        - mountPath: /var/run/secrets/kubernetes.io/serviceaccount
          name: kube-api-access-hbrt8
          readOnly: true
      dnsPolicy: ClusterFirst
      enableServiceLinks: true
      nodeName: minikube
      preemptionPolicy: PreemptLowerPriority
      priority: 0
      restartPolicy: Always
      schedulerName: default-scheduler
      securityContext: {}
      serviceAccount: default
      serviceAccountName: default
      terminationGracePeriodSeconds: 30
      tolerations:
      - effect: NoExecute
        key: node.kubernetes.io/not-ready
        operator: Exists
        tolerationSeconds: 300
      - effect: NoExecute
        key: node.kubernetes.io/unreachable
        operator: Exists
        tolerationSeconds: 300
      volumes:
      - name: kube-api-access-hbrt8
        projected:
          defaultMode: 420
          sources:
          - serviceAccountToken:
              expirationSeconds: 3607
              path: token
          - configMap:
              items:
              - key: ca.crt
                path: ca.crt
              name: kube-root-ca.crt
          - downwardAPI:
              items:
              - fieldRef:
                  apiVersion: v1
                  fieldPath: metadata.namespace
                path: namespace
    status:
      conditions:
      - lastProbeTime: null
        lastTransitionTime: "2024-12-30T11:20:04Z"
        status: "True"
        type: PodReadyToStartContainers
      - lastProbeTime: null
        lastTransitionTime: "2024-12-30T11:20:00Z"
        status: "True"
        type: Initialized
      - lastProbeTime: null
        lastTransitionTime: "2024-12-30T11:20:04Z"
        status: "True"
        type: Ready
      - lastProbeTime: null
        lastTransitionTime: "2024-12-30T11:20:04Z"
        status: "True"
        type: ContainersReady
      - lastProbeTime: null
        lastTransitionTime: "2024-12-30T11:20:00Z"
        status: "True"
        type: PodScheduled
      containerStatuses:
      - containerID: docker://f9adfeb2160f5452315ce8b29d0bfd1966195d854cd3ac4a1698f98d010289bd
        image: model-server:latest
        imageID: docker://sha256:7b09b0acbbfa7baf666665468a5dbd930895258597ffcfa0e83ab22e09f3f57d
        lastState: {}
        name: model-server
        ready: true
        restartCount: 0
        started: true
        state:
          running:
            startedAt: "2024-12-30T11:20:03Z"
        volumeMounts:
        - mountPath: /var/run/secrets/kubernetes.io/serviceaccount
          name: kube-api-access-hbrt8
          readOnly: true
          recursiveReadOnly: Disabled
      hostIP: 192.168.49.2
      hostIPs:
      - ip: 192.168.49.2
      phase: Running
      podIP: 10.244.0.27
      podIPs:
      - ip: 10.244.0.27
      qosClass: Guaranteed
      startTime: "2024-12-30T11:20:00Z"
  - apiVersion: v1
    kind: Pod
    metadata:
      creationTimestamp: "2024-12-30T11:20:00Z"
      generateName: redis-69cf9b5676-
      labels:
        app.kubernetes.io/name: redis
        pod-template-hash: 69cf9b5676
        role: master
      name: redis-69cf9b5676-ksgqb
      namespace: prod
      ownerReferences:
      - apiVersion: apps/v1
        blockOwnerDeletion: true
        controller: true
        kind: ReplicaSet
        name: redis-69cf9b5676
        uid: d4b047b4-9892-4b81-aabe-2afc086c62f7
      resourceVersion: "5872"
      uid: 9b233fce-0560-4467-ab1b-05af7ed4d518
    spec:
      containers:
      - args:
        - --requirepass
        - $(REDIS_PASSWORD)
        command:
        - redis-server
        env:
        - name: REDIS_PASSWORD
          valueFrom:
            secretKeyRef:
              key: db_password
              name: redis-secret-v1
        image: redis:7.4.1
        imagePullPolicy: IfNotPresent
        name: redis
        ports:
        - containerPort: 6379
          name: redis
          protocol: TCP
        resources:
          limits:
            cpu: 200m
            memory: 200Mi
          requests:
            cpu: 200m
            memory: 200Mi
        terminationMessagePath: /dev/termination-log
        terminationMessagePolicy: File
        volumeMounts:
        - mountPath: /data
          name: redis-storage
        - mountPath: /var/run/secrets/kubernetes.io/serviceaccount
          name: kube-api-access-54b62
          readOnly: true
      dnsPolicy: ClusterFirst
      enableServiceLinks: true
      nodeName: minikube
      preemptionPolicy: PreemptLowerPriority
      priority: 0
      restartPolicy: Always
      schedulerName: default-scheduler
      securityContext: {}
      serviceAccount: default
      serviceAccountName: default
      terminationGracePeriodSeconds: 30
      tolerations:
      - effect: NoExecute
        key: node.kubernetes.io/not-ready
        operator: Exists
        tolerationSeconds: 300
      - effect: NoExecute
        key: node.kubernetes.io/unreachable
        operator: Exists
        tolerationSeconds: 300
      volumes:
      - name: redis-storage
        persistentVolumeClaim:
          claimName: redis-pvc
      - name: kube-api-access-54b62
        projected:
          defaultMode: 420
          sources:
          - serviceAccountToken:
              expirationSeconds: 3607
              path: token
          - configMap:
              items:
              - key: ca.crt
                path: ca.crt
              name: kube-root-ca.crt
          - downwardAPI:
              items:
              - fieldRef:
                  apiVersion: v1
                  fieldPath: metadata.namespace
                path: namespace
    status:
      conditions:
      - lastProbeTime: null
        lastTransitionTime: "2024-12-30T11:20:04Z"
        status: "True"
        type: PodReadyToStartContainers
      - lastProbeTime: null
        lastTransitionTime: "2024-12-30T11:20:00Z"
        status: "True"
        type: Initialized
      - lastProbeTime: null
        lastTransitionTime: "2024-12-30T11:20:04Z"
        status: "True"
        type: Ready
      - lastProbeTime: null
        lastTransitionTime: "2024-12-30T11:20:04Z"
        status: "True"
        type: ContainersReady
      - lastProbeTime: null
        lastTransitionTime: "2024-12-30T11:20:00Z"
        status: "True"
        type: PodScheduled
      containerStatuses:
      - containerID: docker://56f47c7cada60042797f82e86db5013538e6fda674ff77897ed9130071f0b60a
        image: redis:7.4.1
        imageID: docker-pullable://redis@sha256:bb142a9c18ac18a16713c1491d779697b4e107c22a97266616099d288237ef47
        lastState: {}
        name: redis
        ready: true
        restartCount: 0
        started: true
        state:
          running:
            startedAt: "2024-12-30T11:20:02Z"
        volumeMounts:
        - mountPath: /data
          name: redis-storage
        - mountPath: /var/run/secrets/kubernetes.io/serviceaccount
          name: kube-api-access-54b62
          readOnly: true
          recursiveReadOnly: Disabled
      hostIP: 192.168.49.2
      hostIPs:
      - ip: 192.168.49.2
      phase: Running
      podIP: 10.244.0.24
      podIPs:
      - ip: 10.244.0.24
      qosClass: Guaranteed
      startTime: "2024-12-30T11:20:00Z"
  - apiVersion: v1
    kind: Pod
    metadata:
      creationTimestamp: "2024-12-30T11:19:59Z"
      generateName: web-server-5c89b7fd87-
      labels:
        app.kubernetes.io/name: web-server
        pod-template-hash: 5c89b7fd87
      name: web-server-5c89b7fd87-5c928
      namespace: prod
      ownerReferences:
      - apiVersion: apps/v1
        blockOwnerDeletion: true
        controller: true
        kind: ReplicaSet
        name: web-server-5c89b7fd87
        uid: f824fd91-34c3-4ed4-aa00-0a635ddff1ed
      resourceVersion: "5867"
      uid: 82882f82-daa4-46cd-9e51-5a3106ebef15
    spec:
      containers:
      - env:
        - name: REDIS_HOST
          valueFrom:
            configMapKeyRef:
              key: hostname
              name: redis-config-v1
        - name: REDIS_PORT
          valueFrom:
            configMapKeyRef:
              key: port
              name: redis-config-v1
        - name: REDIS_PASSWORD
          valueFrom:
            secretKeyRef:
              key: db_password
              name: redis-secret-v1
        - name: MODEL_SERVER_URL
          valueFrom:
            configMapKeyRef:
              key: model_server_url
              name: model-server-config-v1
        image: web-server:latest
        imagePullPolicy: Never
        name: web-server
        ports:
        - containerPort: 80
          name: http
          protocol: TCP
        resources: {}
        terminationMessagePath: /dev/termination-log
        terminationMessagePolicy: File
        volumeMounts:
        - mountPath: /var/run/secrets/kubernetes.io/serviceaccount
          name: kube-api-access-4k7dx
          readOnly: true
      dnsPolicy: ClusterFirst
      enableServiceLinks: true
      nodeName: minikube
      preemptionPolicy: PreemptLowerPriority
      priority: 0
      restartPolicy: Always
      schedulerName: default-scheduler
      securityContext: {}
      serviceAccount: default
      serviceAccountName: default
      terminationGracePeriodSeconds: 30
      tolerations:
      - effect: NoExecute
        key: node.kubernetes.io/not-ready
        operator: Exists
        tolerationSeconds: 300
      - effect: NoExecute
        key: node.kubernetes.io/unreachable
        operator: Exists
        tolerationSeconds: 300
      volumes:
      - name: kube-api-access-4k7dx
        projected:
          defaultMode: 420
          sources:
          - serviceAccountToken:
              expirationSeconds: 3607
              path: token
          - configMap:
              items:
              - key: ca.crt
                path: ca.crt
              name: kube-root-ca.crt
          - downwardAPI:
              items:
              - fieldRef:
                  apiVersion: v1
                  fieldPath: metadata.namespace
                path: namespace
    status:
      conditions:
      - lastProbeTime: null
        lastTransitionTime: "2024-12-30T11:20:04Z"
        status: "True"
        type: PodReadyToStartContainers
      - lastProbeTime: null
        lastTransitionTime: "2024-12-30T11:20:00Z"
        status: "True"
        type: Initialized
      - lastProbeTime: null
        lastTransitionTime: "2024-12-30T11:20:04Z"
        status: "True"
        type: Ready
      - lastProbeTime: null
        lastTransitionTime: "2024-12-30T11:20:04Z"
        status: "True"
        type: ContainersReady
      - lastProbeTime: null
        lastTransitionTime: "2024-12-30T11:19:59Z"
        status: "True"
        type: PodScheduled
      containerStatuses:
      - containerID: docker://e2f09b5dae687ffb80a41ed5313f49fcb7ff2212f883a0bc798ebe299d4cbc39
        image: web-server:latest
        imageID: docker://sha256:c7cc6d48367bb4147ac5ac200583fe06a6d1bcefd02377f384a8965ec6ec9899
        lastState: {}
        name: web-server
        ready: true
        restartCount: 0
        started: true
        state:
          running:
            startedAt: "2024-12-30T11:20:03Z"
        volumeMounts:
        - mountPath: /var/run/secrets/kubernetes.io/serviceaccount
          name: kube-api-access-4k7dx
          readOnly: true
          recursiveReadOnly: Disabled
      hostIP: 192.168.49.2
      hostIPs:
      - ip: 192.168.49.2
      phase: Running
      podIP: 10.244.0.26
      podIPs:
      - ip: 10.244.0.26
      qosClass: BestEffort
      startTime: "2024-12-30T11:20:00Z"
  - apiVersion: v1
    kind: Pod
    metadata:
      creationTimestamp: "2024-12-30T11:19:59Z"
      generateName: web-server-5c89b7fd87-
      labels:
        app.kubernetes.io/name: web-server
        pod-template-hash: 5c89b7fd87
      name: web-server-5c89b7fd87-vh7kk
      namespace: prod
      ownerReferences:
      - apiVersion: apps/v1
        blockOwnerDeletion: true
        controller: true
        kind: ReplicaSet
        name: web-server-5c89b7fd87
        uid: f824fd91-34c3-4ed4-aa00-0a635ddff1ed
      resourceVersion: "5857"
      uid: d60f06ff-6168-44bf-9ac1-52463637c2f7
    spec:
      containers:
      - env:
        - name: REDIS_HOST
          valueFrom:
            configMapKeyRef:
              key: hostname
              name: redis-config-v1
        - name: REDIS_PORT
          valueFrom:
            configMapKeyRef:
              key: port
              name: redis-config-v1
        - name: REDIS_PASSWORD
          valueFrom:
            secretKeyRef:
              key: db_password
              name: redis-secret-v1
        - name: MODEL_SERVER_URL
          valueFrom:
            configMapKeyRef:
              key: model_server_url
              name: model-server-config-v1
        image: web-server:latest
        imagePullPolicy: Never
        name: web-server
        ports:
        - containerPort: 80
          name: http
          protocol: TCP
        resources: {}
        terminationMessagePath: /dev/termination-log
        terminationMessagePolicy: File
        volumeMounts:
        - mountPath: /var/run/secrets/kubernetes.io/serviceaccount
          name: kube-api-access-c8rtm
          readOnly: true
      dnsPolicy: ClusterFirst
      enableServiceLinks: true
      nodeName: minikube
      preemptionPolicy: PreemptLowerPriority
      priority: 0
      restartPolicy: Always
      schedulerName: default-scheduler
      securityContext: {}
      serviceAccount: default
      serviceAccountName: default
      terminationGracePeriodSeconds: 30
      tolerations:
      - effect: NoExecute
        key: node.kubernetes.io/not-ready
        operator: Exists
        tolerationSeconds: 300
      - effect: NoExecute
        key: node.kubernetes.io/unreachable
        operator: Exists
        tolerationSeconds: 300
      volumes:
      - name: kube-api-access-c8rtm
        projected:
          defaultMode: 420
          sources:
          - serviceAccountToken:
              expirationSeconds: 3607
              path: token
          - configMap:
              items:
              - key: ca.crt
                path: ca.crt
              name: kube-root-ca.crt
          - downwardAPI:
              items:
              - fieldRef:
                  apiVersion: v1
                  fieldPath: metadata.namespace
                path: namespace
    status:
      conditions:
      - lastProbeTime: null
        lastTransitionTime: "2024-12-30T11:20:04Z"
        status: "True"
        type: PodReadyToStartContainers
      - lastProbeTime: null
        lastTransitionTime: "2024-12-30T11:20:00Z"
        status: "True"
        type: Initialized
      - lastProbeTime: null
        lastTransitionTime: "2024-12-30T11:20:04Z"
        status: "True"
        type: Ready
      - lastProbeTime: null
        lastTransitionTime: "2024-12-30T11:20:04Z"
        status: "True"
        type: ContainersReady
      - lastProbeTime: null
        lastTransitionTime: "2024-12-30T11:19:59Z"
        status: "True"
        type: PodScheduled
      containerStatuses:
      - containerID: docker://e932dc2cd156ebefe65109d79aeb481115a8d8c8c60f892ff3f1e5769cd81c39
        image: web-server:latest
        imageID: docker://sha256:c7cc6d48367bb4147ac5ac200583fe06a6d1bcefd02377f384a8965ec6ec9899
        lastState: {}
        name: web-server
        ready: true
        restartCount: 0
        started: true
        state:
          running:
            startedAt: "2024-12-30T11:20:02Z"
        volumeMounts:
        - mountPath: /var/run/secrets/kubernetes.io/serviceaccount
          name: kube-api-access-c8rtm
          readOnly: true
          recursiveReadOnly: Disabled
      hostIP: 192.168.49.2
      hostIPs:
      - ip: 192.168.49.2
      phase: Running
      podIP: 10.244.0.23
      podIPs:
      - ip: 10.244.0.23
      qosClass: BestEffort
      startTime: "2024-12-30T11:20:00Z"
  - apiVersion: v1
    kind: Service
    metadata:
      creationTimestamp: "2024-12-30T09:46:18Z"
      labels:
        component: apiserver
        provider: kubernetes
      name: kubernetes
      namespace: default
      resourceVersion: "200"
      uid: 46c65bb4-0c08-4cf3-8e5d-6b63ca57b6bc
    spec:
      clusterIP: 10.96.0.1
      clusterIPs:
      - 10.96.0.1
      internalTrafficPolicy: Cluster
      ipFamilies:
      - IPv4
      ipFamilyPolicy: SingleStack
      ports:
      - name: https
        port: 443
        protocol: TCP
        targetPort: 8443
      sessionAffinity: None
      type: ClusterIP
    status:
      loadBalancer: {}
  - apiVersion: v1
    kind: Service
    metadata:
      annotations:
        kubectl.kubernetes.io/last-applied-configuration: |
          {"apiVersion":"v1","kind":"Service","metadata":{"annotations":{},"labels":{"app.kubernetes.io/component":"controller","app.kubernetes.io/instance":"ingress-nginx","app.kubernetes.io/name":"ingress-nginx"},"name":"ingress-nginx-controller","namespace":"ingress-nginx"},"spec":{"ipFamilies":["IPv4"],"ipFamilyPolicy":"SingleStack","ports":[{"appProtocol":"http","name":"http","port":80,"protocol":"TCP","targetPort":"http"},{"appProtocol":"https","name":"https","port":443,"protocol":"TCP","targetPort":"https"}],"selector":{"app.kubernetes.io/component":"controller","app.kubernetes.io/instance":"ingress-nginx","app.kubernetes.io/name":"ingress-nginx"},"type":"NodePort"}}
      creationTimestamp: "2024-12-30T11:24:36Z"
      labels:
        app.kubernetes.io/component: controller
        app.kubernetes.io/instance: ingress-nginx
        app.kubernetes.io/name: ingress-nginx
      name: ingress-nginx-controller
      namespace: ingress-nginx
      resourceVersion: "6103"
      uid: ed5d7684-d9b3-4b87-8ad2-f41378270e56
    spec:
      clusterIP: 10.99.251.135
      clusterIPs:
      - 10.99.251.135
      externalTrafficPolicy: Cluster
      internalTrafficPolicy: Cluster
      ipFamilies:
      - IPv4
      ipFamilyPolicy: SingleStack
      ports:
      - appProtocol: http
        name: http
        nodePort: 31503
        port: 80
        protocol: TCP
        targetPort: http
      - appProtocol: https
        name: https
        nodePort: 31018
        port: 443
        protocol: TCP
        targetPort: https
      selector:
        app.kubernetes.io/component: controller
        app.kubernetes.io/instance: ingress-nginx
        app.kubernetes.io/name: ingress-nginx
      sessionAffinity: None
      type: NodePort
    status:
      loadBalancer: {}
  - apiVersion: v1
    kind: Service
    metadata:
      annotations:
        kubectl.kubernetes.io/last-applied-configuration: |
          {"apiVersion":"v1","kind":"Service","metadata":{"annotations":{},"labels":{"app.kubernetes.io/component":"controller","app.kubernetes.io/instance":"ingress-nginx","app.kubernetes.io/name":"ingress-nginx"},"name":"ingress-nginx-controller-admission","namespace":"ingress-nginx"},"spec":{"ports":[{"appProtocol":"https","name":"https-webhook","port":443,"targetPort":"webhook"}],"selector":{"app.kubernetes.io/component":"controller","app.kubernetes.io/instance":"ingress-nginx","app.kubernetes.io/name":"ingress-nginx"},"type":"ClusterIP"}}
      creationTimestamp: "2024-12-30T11:24:36Z"
      labels:
        app.kubernetes.io/component: controller
        app.kubernetes.io/instance: ingress-nginx
        app.kubernetes.io/name: ingress-nginx
      name: ingress-nginx-controller-admission
      namespace: ingress-nginx
      resourceVersion: "6107"
      uid: 5ba10ab3-ae3a-4851-be88-6a713aac7dd7
    spec:
      clusterIP: 10.106.137.167
      clusterIPs:
      - 10.106.137.167
      internalTrafficPolicy: Cluster
      ipFamilies:
      - IPv4
      ipFamilyPolicy: SingleStack
      ports:
      - appProtocol: https
        name: https-webhook
        port: 443
        protocol: TCP
        targetPort: webhook
      selector:
        app.kubernetes.io/component: controller
        app.kubernetes.io/instance: ingress-nginx
        app.kubernetes.io/name: ingress-nginx
      sessionAffinity: None
      type: ClusterIP
    status:
      loadBalancer: {}
  - apiVersion: v1
    kind: Service
    metadata:
      annotations:
        prometheus.io/port: "9153"
        prometheus.io/scrape: "true"
      creationTimestamp: "2024-12-30T09:46:19Z"
      labels:
        k8s-app: kube-dns
        kubernetes.io/cluster-service: "true"
        kubernetes.io/name: CoreDNS
      name: kube-dns
      namespace: kube-system
      resourceVersion: "275"
      uid: 63ce0e6c-ea38-4744-9e25-89c4397d92b0
    spec:
      clusterIP: 10.96.0.10
      clusterIPs:
      - 10.96.0.10
      internalTrafficPolicy: Cluster
      ipFamilies:
      - IPv4
      ipFamilyPolicy: SingleStack
      ports:
      - name: dns
        port: 53
        protocol: UDP
        targetPort: 53
      - name: dns-tcp
        port: 53
        protocol: TCP
        targetPort: 53
      - name: metrics
        port: 9153
        protocol: TCP
        targetPort: 9153
      selector:
        k8s-app: kube-dns
      sessionAffinity: None
      type: ClusterIP
    status:
      loadBalancer: {}
  - apiVersion: v1
    kind: Service
    metadata:
      annotations:
        kubectl.kubernetes.io/last-applied-configuration: |
          {"apiVersion":"v1","kind":"Service","metadata":{"annotations":{},"labels":{"addonmanager.kubernetes.io/mode":"Reconcile","k8s-app":"metrics-server","kubernetes.io/minikube-addons":"metrics-server","kubernetes.io/minikube-addons-endpoint":"metrics-server","kubernetes.io/name":"Metrics-server"},"name":"metrics-server","namespace":"kube-system"},"spec":{"ports":[{"name":"https","port":443,"protocol":"TCP","targetPort":"https"}],"selector":{"k8s-app":"metrics-server"}}}
      creationTimestamp: "2024-12-30T11:25:47Z"
      labels:
        addonmanager.kubernetes.io/mode: Reconcile
        k8s-app: metrics-server
        kubernetes.io/minikube-addons: metrics-server
        kubernetes.io/minikube-addons-endpoint: metrics-server
        kubernetes.io/name: Metrics-server
      name: metrics-server
      namespace: kube-system
      resourceVersion: "6329"
      uid: e92998a4-d8be-4e19-82c8-d349bf8dd5d1
    spec:
      clusterIP: 10.96.91.0
      clusterIPs:
      - 10.96.91.0
      internalTrafficPolicy: Cluster
      ipFamilies:
      - IPv4
      ipFamilyPolicy: SingleStack
      ports:
      - name: https
        port: 443
        protocol: TCP
        targetPort: https
      selector:
        k8s-app: metrics-server
      sessionAffinity: None
      type: ClusterIP
    status:
      loadBalancer: {}
  - apiVersion: v1
    kind: Service
    metadata:
      annotations:
        kubectl.kubernetes.io/last-applied-configuration: |
          {"apiVersion":"v1","kind":"Service","metadata":{"annotations":{},"labels":{"addonmanager.kubernetes.io/mode":"Reconcile","k8s-app":"dashboard-metrics-scraper","kubernetes.io/minikube-addons":"dashboard"},"name":"dashboard-metrics-scraper","namespace":"kubernetes-dashboard"},"spec":{"ports":[{"port":8000,"targetPort":8000}],"selector":{"k8s-app":"dashboard-metrics-scraper"}}}
      creationTimestamp: "2024-12-30T11:25:40Z"
      labels:
        addonmanager.kubernetes.io/mode: Reconcile
        k8s-app: dashboard-metrics-scraper
        kubernetes.io/minikube-addons: dashboard
      name: dashboard-metrics-scraper
      namespace: kubernetes-dashboard
      resourceVersion: "6282"
      uid: 9493a947-ae69-4d9e-92ae-14d0257dc0ac
    spec:
      clusterIP: 10.96.189.93
      clusterIPs:
      - 10.96.189.93
      internalTrafficPolicy: Cluster
      ipFamilies:
      - IPv4
      ipFamilyPolicy: SingleStack
      ports:
      - port: 8000
        protocol: TCP
        targetPort: 8000
      selector:
        k8s-app: dashboard-metrics-scraper
      sessionAffinity: None
      type: ClusterIP
    status:
      loadBalancer: {}
  - apiVersion: v1
    kind: Service
    metadata:
      annotations:
        kubectl.kubernetes.io/last-applied-configuration: |
          {"apiVersion":"v1","kind":"Service","metadata":{"annotations":{},"labels":{"addonmanager.kubernetes.io/mode":"Reconcile","k8s-app":"kubernetes-dashboard","kubernetes.io/minikube-addons":"dashboard"},"name":"kubernetes-dashboard","namespace":"kubernetes-dashboard"},"spec":{"ports":[{"port":80,"targetPort":9090}],"selector":{"k8s-app":"kubernetes-dashboard"}}}
      creationTimestamp: "2024-12-30T11:25:40Z"
      labels:
        addonmanager.kubernetes.io/mode: Reconcile
        k8s-app: kubernetes-dashboard
        kubernetes.io/minikube-addons: dashboard
      name: kubernetes-dashboard
      namespace: kubernetes-dashboard
      resourceVersion: "6278"
      uid: 072b1637-68aa-4689-857c-4c5ea146f54a
    spec:
      clusterIP: 10.105.245.59
      clusterIPs:
      - 10.105.245.59
      internalTrafficPolicy: Cluster
      ipFamilies:
      - IPv4
      ipFamilyPolicy: SingleStack
      ports:
      - port: 80
        protocol: TCP
        targetPort: 9090
      selector:
        k8s-app: kubernetes-dashboard
      sessionAffinity: None
      type: ClusterIP
    status:
      loadBalancer: {}
  - apiVersion: v1
    kind: Service
    metadata:
      annotations:
        meta.helm.sh/release-name: fastapi-release-prod
        meta.helm.sh/release-namespace: production
      creationTimestamp: "2024-12-30T11:19:59Z"
      labels:
        app.kubernetes.io/managed-by: Helm
        app.kubernetes.io/name: model-server
        app.kubernetes.io/part-of: fastapi-app
      name: model-server-service
      namespace: prod
      resourceVersion: "5775"
      uid: 87e32a05-e6ac-49bd-9757-5e7273bfd894
    spec:
      clusterIP: 10.101.245.219
      clusterIPs:
      - 10.101.245.219
      internalTrafficPolicy: Cluster
      ipFamilies:
      - IPv4
      ipFamilyPolicy: SingleStack
      ports:
      - name: http
        port: 80
        protocol: TCP
        targetPort: 80
      selector:
        app.kubernetes.io/name: model-server
      sessionAffinity: None
      type: ClusterIP
    status:
      loadBalancer: {}
  - apiVersion: v1
    kind: Service
    metadata:
      annotations:
        meta.helm.sh/release-name: fastapi-release-prod
        meta.helm.sh/release-namespace: production
      creationTimestamp: "2024-12-30T11:19:59Z"
      labels:
        app.kubernetes.io/managed-by: Helm
        app.kubernetes.io/name: redis
        app.kubernetes.io/part-of: fastapi-app
        role: master
      name: redis-service
      namespace: prod
      resourceVersion: "5780"
      uid: a9a046b8-0343-4f9a-a668-7e60b4503f98
    spec:
      clusterIP: 10.111.174.14
      clusterIPs:
      - 10.111.174.14
      internalTrafficPolicy: Cluster
      ipFamilies:
      - IPv4
      ipFamilyPolicy: SingleStack
      ports:
      - name: redis
        port: 6379
        protocol: TCP
        targetPort: 6379
      selector:
        app.kubernetes.io/name: redis
        role: master
      sessionAffinity: None
      type: ClusterIP
    status:
      loadBalancer: {}
  - apiVersion: v1
    kind: Service
    metadata:
      annotations:
        meta.helm.sh/release-name: fastapi-release-prod
        meta.helm.sh/release-namespace: production
      creationTimestamp: "2024-12-30T11:19:59Z"
      labels:
        app.kubernetes.io/instance: fastapi-release-prod
        app.kubernetes.io/managed-by: Helm
        app.kubernetes.io/name: web-server
        app.kubernetes.io/part-of: fastapi-app
      name: web-server-service
      namespace: prod
      resourceVersion: "5770"
      uid: 519f2c0c-0b21-4417-aa86-a677375322ed
    spec:
      clusterIP: 10.105.133.69
      clusterIPs:
      - 10.105.133.69
      internalTrafficPolicy: Cluster
      ipFamilies:
      - IPv4
      ipFamilyPolicy: SingleStack
      ports:
      - name: http
        port: 80
        protocol: TCP
        targetPort: 80
      selector:
        app.kubernetes.io/name: web-server
      sessionAffinity: None
      type: ClusterIP
    status:
      loadBalancer: {}
  - apiVersion: apps/v1
    kind: DaemonSet
    metadata:
      annotations:
        deprecated.daemonset.template.generation: "1"
      creationTimestamp: "2024-12-30T09:46:19Z"
      generation: 1
      labels:
        k8s-app: kube-proxy
      name: kube-proxy
      namespace: kube-system
      resourceVersion: "402"
      uid: 46b4a363-ef53-42bf-85be-c7329f1ae879
    spec:
      revisionHistoryLimit: 10
      selector:
        matchLabels:
          k8s-app: kube-proxy
      template:
        metadata:
          creationTimestamp: null
          labels:
            k8s-app: kube-proxy
        spec:
          containers:
          - command:
            - /usr/local/bin/kube-proxy
            - --config=/var/lib/kube-proxy/config.conf
            - --hostname-override=$(NODE_NAME)
            env:
            - name: NODE_NAME
              valueFrom:
                fieldRef:
                  apiVersion: v1
                  fieldPath: spec.nodeName
            image: registry.k8s.io/kube-proxy:v1.31.0
            imagePullPolicy: IfNotPresent
            name: kube-proxy
            resources: {}
            securityContext:
              privileged: true
            terminationMessagePath: /dev/termination-log
            terminationMessagePolicy: File
            volumeMounts:
            - mountPath: /var/lib/kube-proxy
              name: kube-proxy
            - mountPath: /run/xtables.lock
              name: xtables-lock
            - mountPath: /lib/modules
              name: lib-modules
              readOnly: true
          dnsPolicy: ClusterFirst
          hostNetwork: true
          nodeSelector:
            kubernetes.io/os: linux
          priorityClassName: system-node-critical
          restartPolicy: Always
          schedulerName: default-scheduler
          securityContext: {}
          serviceAccount: kube-proxy
          serviceAccountName: kube-proxy
          terminationGracePeriodSeconds: 30
          tolerations:
          - operator: Exists
          volumes:
          - configMap:
              defaultMode: 420
              name: kube-proxy
            name: kube-proxy
          - hostPath:
              path: /run/xtables.lock
              type: FileOrCreate
            name: xtables-lock
          - hostPath:
              path: /lib/modules
              type: ""
            name: lib-modules
      updateStrategy:
        rollingUpdate:
          maxSurge: 0
          maxUnavailable: 1
        type: RollingUpdate
    status:
      currentNumberScheduled: 1
      desiredNumberScheduled: 1
      numberAvailable: 1
      numberMisscheduled: 0
      numberReady: 1
      observedGeneration: 1
      updatedNumberScheduled: 1
  - apiVersion: apps/v1
    kind: Deployment
    metadata:
      annotations:
        deployment.kubernetes.io/revision: "1"
        kubectl.kubernetes.io/last-applied-configuration: |
          {"apiVersion":"apps/v1","kind":"Deployment","metadata":{"annotations":{},"labels":{"app.kubernetes.io/component":"controller","app.kubernetes.io/instance":"ingress-nginx","app.kubernetes.io/name":"ingress-nginx"},"name":"ingress-nginx-controller","namespace":"ingress-nginx"},"spec":{"minReadySeconds":0,"revisionHistoryLimit":10,"selector":{"matchLabels":{"app.kubernetes.io/component":"controller","app.kubernetes.io/instance":"ingress-nginx","app.kubernetes.io/name":"ingress-nginx"}},"strategy":{"rollingUpdate":{"maxUnavailable":1},"type":"RollingUpdate"},"template":{"metadata":{"labels":{"app.kubernetes.io/component":"controller","app.kubernetes.io/instance":"ingress-nginx","app.kubernetes.io/name":"ingress-nginx","gcp-auth-skip-secret":"true"}},"spec":{"containers":[{"args":["/nginx-ingress-controller","--election-id=ingress-nginx-leader","--controller-class=k8s.io/ingress-nginx","--watch-ingress-without-class=true","--configmap=$(POD_NAMESPACE)/ingress-nginx-controller","--tcp-services-configmap=$(POD_NAMESPACE)/tcp-services","--udp-services-configmap=$(POD_NAMESPACE)/udp-services","--validating-webhook=:8443","--validating-webhook-certificate=/usr/local/certificates/cert","--validating-webhook-key=/usr/local/certificates/key"],"env":[{"name":"POD_NAME","valueFrom":{"fieldRef":{"fieldPath":"metadata.name"}}},{"name":"POD_NAMESPACE","valueFrom":{"fieldRef":{"fieldPath":"metadata.namespace"}}},{"name":"LD_PRELOAD","value":"/usr/local/lib/libmimalloc.so"}],"image":"registry.k8s.io/ingress-nginx/controller:v1.11.2@sha256:d5f8217feeac4887cb1ed21f27c2674e58be06bd8f5184cacea2a69abaf78dce","imagePullPolicy":"IfNotPresent","lifecycle":{"preStop":{"exec":{"command":["/wait-shutdown"]}}},"livenessProbe":{"failureThreshold":5,"httpGet":{"path":"/healthz","port":10254,"scheme":"HTTP"},"initialDelaySeconds":10,"periodSeconds":10,"successThreshold":1,"timeoutSeconds":1},"name":"controller","ports":[{"containerPort":80,"hostPort":80,"name":"http","protocol":"TCP"},{"containerPort":443,"hostPort":443,"name":"https","protocol":"TCP"},{"containerPort":8443,"name":"webhook","protocol":"TCP"}],"readinessProbe":{"failureThreshold":3,"httpGet":{"path":"/healthz","port":10254,"scheme":"HTTP"},"initialDelaySeconds":10,"periodSeconds":10,"successThreshold":1,"timeoutSeconds":1},"resources":{"requests":{"cpu":"100m","memory":"90Mi"}},"securityContext":{"allowPrivilegeEscalation":true,"capabilities":{"add":["NET_BIND_SERVICE"],"drop":["ALL"]},"runAsUser":101},"volumeMounts":[{"mountPath":"/usr/local/certificates/","name":"webhook-cert","readOnly":true}]}],"dnsPolicy":"ClusterFirst","nodeSelector":{"kubernetes.io/os":"linux","minikube.k8s.io/primary":"true"},"serviceAccountName":"ingress-nginx","terminationGracePeriodSeconds":0,"tolerations":[{"effect":"NoSchedule","key":"node-role.kubernetes.io/master","operator":"Equal"}],"volumes":[{"name":"webhook-cert","secret":{"secretName":"ingress-nginx-admission"}}]}}}}
      creationTimestamp: "2024-12-30T11:24:36Z"
      generation: 1
      labels:
        app.kubernetes.io/component: controller
        app.kubernetes.io/instance: ingress-nginx
        app.kubernetes.io/name: ingress-nginx
      name: ingress-nginx-controller
      namespace: ingress-nginx
      resourceVersion: "6301"
      uid: f7dc4043-2827-4cbd-8312-4f5a58aec950
    spec:
      progressDeadlineSeconds: 600
      replicas: 1
      revisionHistoryLimit: 10
      selector:
        matchLabels:
          app.kubernetes.io/component: controller
          app.kubernetes.io/instance: ingress-nginx
          app.kubernetes.io/name: ingress-nginx
      strategy:
        rollingUpdate:
          maxSurge: 25%
          maxUnavailable: 1
        type: RollingUpdate
      template:
        metadata:
          creationTimestamp: null
          labels:
            app.kubernetes.io/component: controller
            app.kubernetes.io/instance: ingress-nginx
            app.kubernetes.io/name: ingress-nginx
            gcp-auth-skip-secret: "true"
        spec:
          containers:
          - args:
            - /nginx-ingress-controller
            - --election-id=ingress-nginx-leader
            - --controller-class=k8s.io/ingress-nginx
            - --watch-ingress-without-class=true
            - --configmap=$(POD_NAMESPACE)/ingress-nginx-controller
            - --tcp-services-configmap=$(POD_NAMESPACE)/tcp-services
            - --udp-services-configmap=$(POD_NAMESPACE)/udp-services
            - --validating-webhook=:8443
            - --validating-webhook-certificate=/usr/local/certificates/cert
            - --validating-webhook-key=/usr/local/certificates/key
            env:
            - name: POD_NAME
              valueFrom:
                fieldRef:
                  apiVersion: v1
                  fieldPath: metadata.name
            - name: POD_NAMESPACE
              valueFrom:
                fieldRef:
                  apiVersion: v1
                  fieldPath: metadata.namespace
            - name: LD_PRELOAD
              value: /usr/local/lib/libmimalloc.so
            image: registry.k8s.io/ingress-nginx/controller:v1.11.2@sha256:d5f8217feeac4887cb1ed21f27c2674e58be06bd8f5184cacea2a69abaf78dce
            imagePullPolicy: IfNotPresent
            lifecycle:
              preStop:
                exec:
                  command:
                  - /wait-shutdown
            livenessProbe:
              failureThreshold: 5
              httpGet:
                path: /healthz
                port: 10254
                scheme: HTTP
              initialDelaySeconds: 10
              periodSeconds: 10
              successThreshold: 1
              timeoutSeconds: 1
            name: controller
            ports:
            - containerPort: 80
              hostPort: 80
              name: http
              protocol: TCP
            - containerPort: 443
              hostPort: 443
              name: https
              protocol: TCP
            - containerPort: 8443
              name: webhook
              protocol: TCP
            readinessProbe:
              failureThreshold: 3
              httpGet:
                path: /healthz
                port: 10254
                scheme: HTTP
              initialDelaySeconds: 10
              periodSeconds: 10
              successThreshold: 1
              timeoutSeconds: 1
            resources:
              requests:
                cpu: 100m
                memory: 90Mi
            securityContext:
              allowPrivilegeEscalation: true
              capabilities:
                add:
                - NET_BIND_SERVICE
                drop:
                - ALL
              runAsUser: 101
            terminationMessagePath: /dev/termination-log
            terminationMessagePolicy: File
            volumeMounts:
            - mountPath: /usr/local/certificates/
              name: webhook-cert
              readOnly: true
          dnsPolicy: ClusterFirst
          nodeSelector:
            kubernetes.io/os: linux
            minikube.k8s.io/primary: "true"
          restartPolicy: Always
          schedulerName: default-scheduler
          securityContext: {}
          serviceAccount: ingress-nginx
          serviceAccountName: ingress-nginx
          terminationGracePeriodSeconds: 0
          tolerations:
          - effect: NoSchedule
            key: node-role.kubernetes.io/master
            operator: Equal
          volumes:
          - name: webhook-cert
            secret:
              defaultMode: 420
              secretName: ingress-nginx-admission
    status:
      availableReplicas: 1
      conditions:
      - lastTransitionTime: "2024-12-30T11:24:37Z"
        lastUpdateTime: "2024-12-30T11:24:37Z"
        message: Deployment has minimum availability.
        reason: MinimumReplicasAvailable
        status: "True"
        type: Available
      - lastTransitionTime: "2024-12-30T11:24:36Z"
        lastUpdateTime: "2024-12-30T11:25:45Z"
        message: ReplicaSet "ingress-nginx-controller-bc57996ff" has successfully progressed.
        reason: NewReplicaSetAvailable
        status: "True"
        type: Progressing
      observedGeneration: 1
      readyReplicas: 1
      replicas: 1
      updatedReplicas: 1
  - apiVersion: apps/v1
    kind: Deployment
    metadata:
      annotations:
        deployment.kubernetes.io/revision: "1"
      creationTimestamp: "2024-12-30T09:46:19Z"
      generation: 2
      labels:
        k8s-app: kube-dns
      name: coredns
      namespace: kube-system
      resourceVersion: "5477"
      uid: 7692e7bd-e741-4529-94fa-b3f3d056772c
    spec:
      progressDeadlineSeconds: 600
      replicas: 1
      revisionHistoryLimit: 10
      selector:
        matchLabels:
          k8s-app: kube-dns
      strategy:
        rollingUpdate:
          maxSurge: 25%
          maxUnavailable: 1
        type: RollingUpdate
      template:
        metadata:
          creationTimestamp: null
          labels:
            k8s-app: kube-dns
        spec:
          affinity:
            podAntiAffinity:
              preferredDuringSchedulingIgnoredDuringExecution:
              - podAffinityTerm:
                  labelSelector:
                    matchExpressions:
                    - key: k8s-app
                      operator: In
                      values:
                      - kube-dns
                  topologyKey: kubernetes.io/hostname
                weight: 100
          containers:
          - args:
            - -conf
            - /etc/coredns/Corefile
            image: registry.k8s.io/coredns/coredns:v1.11.1
            imagePullPolicy: IfNotPresent
            livenessProbe:
              failureThreshold: 5
              httpGet:
                path: /health
                port: 8080
                scheme: HTTP
              initialDelaySeconds: 60
              periodSeconds: 10
              successThreshold: 1
              timeoutSeconds: 5
            name: coredns
            ports:
            - containerPort: 53
              name: dns
              protocol: UDP
            - containerPort: 53
              name: dns-tcp
              protocol: TCP
            - containerPort: 9153
              name: metrics
              protocol: TCP
            readinessProbe:
              failureThreshold: 3
              httpGet:
                path: /ready
                port: 8181
                scheme: HTTP
              periodSeconds: 10
              successThreshold: 1
              timeoutSeconds: 1
            resources:
              limits:
                memory: 170Mi
              requests:
                cpu: 100m
                memory: 70Mi
            securityContext:
              allowPrivilegeEscalation: false
              capabilities:
                add:
                - NET_BIND_SERVICE
                drop:
                - ALL
              readOnlyRootFilesystem: true
            terminationMessagePath: /dev/termination-log
            terminationMessagePolicy: File
            volumeMounts:
            - mountPath: /etc/coredns
              name: config-volume
              readOnly: true
          dnsPolicy: Default
          nodeSelector:
            kubernetes.io/os: linux
          priorityClassName: system-cluster-critical
          restartPolicy: Always
          schedulerName: default-scheduler
          securityContext: {}
          serviceAccount: coredns
          serviceAccountName: coredns
          terminationGracePeriodSeconds: 30
          tolerations:
          - key: CriticalAddonsOnly
            operator: Exists
          - effect: NoSchedule
            key: node-role.kubernetes.io/control-plane
          volumes:
          - configMap:
              defaultMode: 420
              items:
              - key: Corefile
                path: Corefile
              name: coredns
            name: config-volume
    status:
      availableReplicas: 1
      conditions:
      - lastTransitionTime: "2024-12-30T09:46:23Z"
        lastUpdateTime: "2024-12-30T09:46:23Z"
        message: Deployment has minimum availability.
        reason: MinimumReplicasAvailable
        status: "True"
        type: Available
      - lastTransitionTime: "2024-12-30T09:46:23Z"
        lastUpdateTime: "2024-12-30T09:47:07Z"
        message: ReplicaSet "coredns-6f6b679f8f" has successfully progressed.
        reason: NewReplicaSetAvailable
        status: "True"
        type: Progressing
      observedGeneration: 2
      readyReplicas: 1
      replicas: 1
      updatedReplicas: 1
  - apiVersion: apps/v1
    kind: Deployment
    metadata:
      annotations:
        deployment.kubernetes.io/revision: "1"
        kubectl.kubernetes.io/last-applied-configuration: |
          {"apiVersion":"apps/v1","kind":"Deployment","metadata":{"annotations":{},"labels":{"addonmanager.kubernetes.io/mode":"Reconcile","k8s-app":"metrics-server","kubernetes.io/minikube-addons":"metrics-server"},"name":"metrics-server","namespace":"kube-system"},"spec":{"selector":{"matchLabels":{"k8s-app":"metrics-server"}},"strategy":{"rollingUpdate":{"maxUnavailable":0}},"template":{"metadata":{"labels":{"k8s-app":"metrics-server"},"name":"metrics-server"},"spec":{"containers":[{"args":["--cert-dir=/tmp","--secure-port=4443","--kubelet-preferred-address-types=InternalIP,ExternalIP,Hostname","--kubelet-use-node-status-port","--metric-resolution=60s","--kubelet-insecure-tls"],"image":"registry.k8s.io/metrics-server/metrics-server:v0.7.2@sha256:ffcb2bf004d6aa0a17d90e0247cf94f2865c8901dcab4427034c341951c239f9","imagePullPolicy":"IfNotPresent","livenessProbe":{"failureThreshold":3,"httpGet":{"path":"/livez","port":"https","scheme":"HTTPS"},"periodSeconds":10},"name":"metrics-server","ports":[{"containerPort":4443,"name":"https","protocol":"TCP"}],"readinessProbe":{"failureThreshold":3,"httpGet":{"path":"/readyz","port":"https","scheme":"HTTPS"},"periodSeconds":10},"resources":{"requests":{"cpu":"100m","memory":"200Mi"}},"securityContext":{"readOnlyRootFilesystem":true,"runAsNonRoot":true,"runAsUser":1000},"volumeMounts":[{"mountPath":"/tmp","name":"tmp-dir"}]}],"priorityClassName":"system-cluster-critical","serviceAccountName":"metrics-server","volumes":[{"emptyDir":{},"name":"tmp-dir"}]}}}}
      creationTimestamp: "2024-12-30T11:25:47Z"
      generation: 1
      labels:
        addonmanager.kubernetes.io/mode: Reconcile
        k8s-app: metrics-server
        kubernetes.io/minikube-addons: metrics-server
      name: metrics-server
      namespace: kube-system
      resourceVersion: "6404"
      uid: fa6a5982-379f-423a-b34f-1a2f0b6ccccd
    spec:
      progressDeadlineSeconds: 600
      replicas: 1
      revisionHistoryLimit: 10
      selector:
        matchLabels:
          k8s-app: metrics-server
      strategy:
        rollingUpdate:
          maxSurge: 25%
          maxUnavailable: 0
        type: RollingUpdate
      template:
        metadata:
          creationTimestamp: null
          labels:
            k8s-app: metrics-server
          name: metrics-server
        spec:
          containers:
          - args:
            - --cert-dir=/tmp
            - --secure-port=4443
            - --kubelet-preferred-address-types=InternalIP,ExternalIP,Hostname
            - --kubelet-use-node-status-port
            - --metric-resolution=60s
            - --kubelet-insecure-tls
            image: registry.k8s.io/metrics-server/metrics-server:v0.7.2@sha256:ffcb2bf004d6aa0a17d90e0247cf94f2865c8901dcab4427034c341951c239f9
            imagePullPolicy: IfNotPresent
            livenessProbe:
              failureThreshold: 3
              httpGet:
                path: /livez
                port: https
                scheme: HTTPS
              periodSeconds: 10
              successThreshold: 1
              timeoutSeconds: 1
            name: metrics-server
            ports:
            - containerPort: 4443
              name: https
              protocol: TCP
            readinessProbe:
              failureThreshold: 3
              httpGet:
                path: /readyz
                port: https
                scheme: HTTPS
              periodSeconds: 10
              successThreshold: 1
              timeoutSeconds: 1
            resources:
              requests:
                cpu: 100m
                memory: 200Mi
            securityContext:
              readOnlyRootFilesystem: true
              runAsNonRoot: true
              runAsUser: 1000
            terminationMessagePath: /dev/termination-log
            terminationMessagePolicy: File
            volumeMounts:
            - mountPath: /tmp
              name: tmp-dir
          dnsPolicy: ClusterFirst
          priorityClassName: system-cluster-critical
          restartPolicy: Always
          schedulerName: default-scheduler
          securityContext: {}
          serviceAccount: metrics-server
          serviceAccountName: metrics-server
          terminationGracePeriodSeconds: 30
          volumes:
          - emptyDir: {}
            name: tmp-dir
    status:
      availableReplicas: 1
      conditions:
      - lastTransitionTime: "2024-12-30T11:26:30Z"
        lastUpdateTime: "2024-12-30T11:26:30Z"
        message: Deployment has minimum availability.
        reason: MinimumReplicasAvailable
        status: "True"
        type: Available
      - lastTransitionTime: "2024-12-30T11:25:47Z"
        lastUpdateTime: "2024-12-30T11:26:30Z"
        message: ReplicaSet "metrics-server-84c5f94fbc" has successfully progressed.
        reason: NewReplicaSetAvailable
        status: "True"
        type: Progressing
      observedGeneration: 1
      readyReplicas: 1
      replicas: 1
      updatedReplicas: 1
  - apiVersion: apps/v1
    kind: Deployment
    metadata:
      annotations:
        deployment.kubernetes.io/revision: "1"
        kubectl.kubernetes.io/last-applied-configuration: |
          {"apiVersion":"apps/v1","kind":"Deployment","metadata":{"annotations":{},"labels":{"addonmanager.kubernetes.io/mode":"Reconcile","k8s-app":"dashboard-metrics-scraper","kubernetes.io/minikube-addons":"dashboard"},"name":"dashboard-metrics-scraper","namespace":"kubernetes-dashboard"},"spec":{"replicas":1,"revisionHistoryLimit":10,"selector":{"matchLabels":{"k8s-app":"dashboard-metrics-scraper"}},"template":{"metadata":{"annotations":{"seccomp.security.alpha.kubernetes.io/pod":"runtime/default"},"labels":{"k8s-app":"dashboard-metrics-scraper"}},"spec":{"containers":[{"image":"docker.io/kubernetesui/metrics-scraper:v1.0.8@sha256:76049887f07a0476dc93efc2d3569b9529bf982b22d29f356092ce206e98765c","livenessProbe":{"httpGet":{"path":"/","port":8000,"scheme":"HTTP"},"initialDelaySeconds":30,"timeoutSeconds":30},"name":"dashboard-metrics-scraper","ports":[{"containerPort":8000,"protocol":"TCP"}],"securityContext":{"allowPrivilegeEscalation":false,"readOnlyRootFilesystem":true,"runAsGroup":2001,"runAsUser":1001},"volumeMounts":[{"mountPath":"/tmp","name":"tmp-volume"}]}],"nodeSelector":{"kubernetes.io/os":"linux"},"serviceAccountName":"kubernetes-dashboard","tolerations":[{"effect":"NoSchedule","key":"node-role.kubernetes.io/master"}],"volumes":[{"emptyDir":{},"name":"tmp-volume"}]}}}}
      creationTimestamp: "2024-12-30T11:25:39Z"
      generation: 1
      labels:
        addonmanager.kubernetes.io/mode: Reconcile
        k8s-app: dashboard-metrics-scraper
        kubernetes.io/minikube-addons: dashboard
      name: dashboard-metrics-scraper
      namespace: kubernetes-dashboard
      resourceVersion: "6381"
      uid: e67c0f1d-1a86-4bb3-9e31-ee4f3132002a
    spec:
      progressDeadlineSeconds: 600
      replicas: 1
      revisionHistoryLimit: 10
      selector:
        matchLabels:
          k8s-app: dashboard-metrics-scraper
      strategy:
        rollingUpdate:
          maxSurge: 25%
          maxUnavailable: 25%
        type: RollingUpdate
      template:
        metadata:
          annotations:
            seccomp.security.alpha.kubernetes.io/pod: runtime/default
          creationTimestamp: null
          labels:
            k8s-app: dashboard-metrics-scraper
        spec:
          containers:
          - image: docker.io/kubernetesui/metrics-scraper:v1.0.8@sha256:76049887f07a0476dc93efc2d3569b9529bf982b22d29f356092ce206e98765c
            imagePullPolicy: IfNotPresent
            livenessProbe:
              failureThreshold: 3
              httpGet:
                path: /
                port: 8000
                scheme: HTTP
              initialDelaySeconds: 30
              periodSeconds: 10
              successThreshold: 1
              timeoutSeconds: 30
            name: dashboard-metrics-scraper
            ports:
            - containerPort: 8000
              protocol: TCP
            resources: {}
            securityContext:
              allowPrivilegeEscalation: false
              readOnlyRootFilesystem: true
              runAsGroup: 2001
              runAsUser: 1001
            terminationMessagePath: /dev/termination-log
            terminationMessagePolicy: File
            volumeMounts:
            - mountPath: /tmp
              name: tmp-volume
          dnsPolicy: ClusterFirst
          nodeSelector:
            kubernetes.io/os: linux
          restartPolicy: Always
          schedulerName: default-scheduler
          securityContext: {}
          serviceAccount: kubernetes-dashboard
          serviceAccountName: kubernetes-dashboard
          terminationGracePeriodSeconds: 30
          tolerations:
          - effect: NoSchedule
            key: node-role.kubernetes.io/master
          volumes:
          - emptyDir: {}
            name: tmp-volume
    status:
      availableReplicas: 1
      conditions:
      - lastTransitionTime: "2024-12-30T11:26:18Z"
        lastUpdateTime: "2024-12-30T11:26:18Z"
        message: Deployment has minimum availability.
        reason: MinimumReplicasAvailable
        status: "True"
        type: Available
      - lastTransitionTime: "2024-12-30T11:25:39Z"
        lastUpdateTime: "2024-12-30T11:26:18Z"
        message: ReplicaSet "dashboard-metrics-scraper-c5db448b4" has successfully progressed.
        reason: NewReplicaSetAvailable
        status: "True"
        type: Progressing
      observedGeneration: 1
      readyReplicas: 1
      replicas: 1
      updatedReplicas: 1
  - apiVersion: apps/v1
    kind: Deployment
    metadata:
      annotations:
        deployment.kubernetes.io/revision: "1"
        kubectl.kubernetes.io/last-applied-configuration: |
          {"apiVersion":"apps/v1","kind":"Deployment","metadata":{"annotations":{},"labels":{"addonmanager.kubernetes.io/mode":"Reconcile","k8s-app":"kubernetes-dashboard","kubernetes.io/minikube-addons":"dashboard"},"name":"kubernetes-dashboard","namespace":"kubernetes-dashboard"},"spec":{"replicas":1,"revisionHistoryLimit":10,"selector":{"matchLabels":{"k8s-app":"kubernetes-dashboard"}},"template":{"metadata":{"labels":{"gcp-auth-skip-secret":"true","k8s-app":"kubernetes-dashboard"}},"spec":{"containers":[{"args":["--namespace=kubernetes-dashboard","--enable-skip-login","--disable-settings-authorizer"],"image":"docker.io/kubernetesui/dashboard:v2.7.0@sha256:2e500d29e9d5f4a086b908eb8dfe7ecac57d2ab09d65b24f588b1d449841ef93","livenessProbe":{"httpGet":{"path":"/","port":9090},"initialDelaySeconds":30,"timeoutSeconds":30},"name":"kubernetes-dashboard","ports":[{"containerPort":9090,"protocol":"TCP"}],"securityContext":{"allowPrivilegeEscalation":false,"readOnlyRootFilesystem":true,"runAsGroup":2001,"runAsUser":1001},"volumeMounts":[{"mountPath":"/tmp","name":"tmp-volume"}]}],"nodeSelector":{"kubernetes.io/os":"linux"},"serviceAccountName":"kubernetes-dashboard","tolerations":[{"effect":"NoSchedule","key":"node-role.kubernetes.io/master"}],"volumes":[{"emptyDir":{},"name":"tmp-volume"}]}}}}
      creationTimestamp: "2024-12-30T11:25:39Z"
      generation: 1
      labels:
        addonmanager.kubernetes.io/mode: Reconcile
        k8s-app: kubernetes-dashboard
        kubernetes.io/minikube-addons: dashboard
      name: kubernetes-dashboard
      namespace: kubernetes-dashboard
      resourceVersion: "6363"
      uid: 4d22a9b0-f026-47cf-a8f7-486284fab9c8
    spec:
      progressDeadlineSeconds: 600
      replicas: 1
      revisionHistoryLimit: 10
      selector:
        matchLabels:
          k8s-app: kubernetes-dashboard
      strategy:
        rollingUpdate:
          maxSurge: 25%
          maxUnavailable: 25%
        type: RollingUpdate
      template:
        metadata:
          creationTimestamp: null
          labels:
            gcp-auth-skip-secret: "true"
            k8s-app: kubernetes-dashboard
        spec:
          containers:
          - args:
            - --namespace=kubernetes-dashboard
            - --enable-skip-login
            - --disable-settings-authorizer
            image: docker.io/kubernetesui/dashboard:v2.7.0@sha256:2e500d29e9d5f4a086b908eb8dfe7ecac57d2ab09d65b24f588b1d449841ef93
            imagePullPolicy: IfNotPresent
            livenessProbe:
              failureThreshold: 3
              httpGet:
                path: /
                port: 9090
                scheme: HTTP
              initialDelaySeconds: 30
              periodSeconds: 10
              successThreshold: 1
              timeoutSeconds: 30
            name: kubernetes-dashboard
            ports:
            - containerPort: 9090
              protocol: TCP
            resources: {}
            securityContext:
              allowPrivilegeEscalation: false
              readOnlyRootFilesystem: true
              runAsGroup: 2001
              runAsUser: 1001
            terminationMessagePath: /dev/termination-log
            terminationMessagePolicy: File
            volumeMounts:
            - mountPath: /tmp
              name: tmp-volume
          dnsPolicy: ClusterFirst
          nodeSelector:
            kubernetes.io/os: linux
          restartPolicy: Always
          schedulerName: default-scheduler
          securityContext: {}
          serviceAccount: kubernetes-dashboard
          serviceAccountName: kubernetes-dashboard
          terminationGracePeriodSeconds: 30
          tolerations:
          - effect: NoSchedule
            key: node-role.kubernetes.io/master
          volumes:
          - emptyDir: {}
            name: tmp-volume
    status:
      availableReplicas: 1
      conditions:
      - lastTransitionTime: "2024-12-30T11:26:09Z"
        lastUpdateTime: "2024-12-30T11:26:09Z"
        message: Deployment has minimum availability.
        reason: MinimumReplicasAvailable
        status: "True"
        type: Available
      - lastTransitionTime: "2024-12-30T11:25:40Z"
        lastUpdateTime: "2024-12-30T11:26:09Z"
        message: ReplicaSet "kubernetes-dashboard-695b96c756" has successfully progressed.
        reason: NewReplicaSetAvailable
        status: "True"
        type: Progressing
      observedGeneration: 1
      readyReplicas: 1
      replicas: 1
      updatedReplicas: 1
  - apiVersion: apps/v1
    kind: Deployment
    metadata:
      annotations:
        deployment.kubernetes.io/revision: "1"
        meta.helm.sh/release-name: fastapi-release-prod
        meta.helm.sh/release-namespace: production
      creationTimestamp: "2024-12-30T11:19:59Z"
      generation: 1
      labels:
        app.kubernetes.io/managed-by: Helm
        app.kubernetes.io/name: model-server
        app.kubernetes.io/part-of: fastapi-app
      name: model-server
      namespace: prod
      resourceVersion: "5868"
      uid: bfecbf4c-d1b5-4ba4-acd1-1a1e6ed6adb6
    spec:
      progressDeadlineSeconds: 600
      replicas: 2
      revisionHistoryLimit: 10
      selector:
        matchLabels:
          app.kubernetes.io/name: model-server
      strategy:
        rollingUpdate:
          maxSurge: 25%
          maxUnavailable: 25%
        type: RollingUpdate
      template:
        metadata:
          creationTimestamp: null
          labels:
            app.kubernetes.io/name: model-server
        spec:
          containers:
          - env:
            - name: REDIS_HOST
              valueFrom:
                configMapKeyRef:
                  key: hostname
                  name: redis-config-v1
            - name: REDIS_PORT
              valueFrom:
                configMapKeyRef:
                  key: port
                  name: redis-config-v1
            - name: REDIS_PASSWORD
              valueFrom:
                secretKeyRef:
                  key: db_password
                  name: redis-secret-v1
            - name: MODEL_NAME
              valueFrom:
                configMapKeyRef:
                  key: model_name
                  name: model-server-config-v1
            image: model-server:latest
            imagePullPolicy: Never
            name: model-server
            ports:
            - containerPort: 80
              name: http
              protocol: TCP
            resources:
              limits:
                cpu: "1"
                memory: 2Gi
            terminationMessagePath: /dev/termination-log
            terminationMessagePolicy: File
          dnsPolicy: ClusterFirst
          restartPolicy: Always
          schedulerName: default-scheduler
          securityContext: {}
          terminationGracePeriodSeconds: 30
    status:
      availableReplicas: 2
      conditions:
      - lastTransitionTime: "2024-12-30T11:20:04Z"
        lastUpdateTime: "2024-12-30T11:20:04Z"
        message: Deployment has minimum availability.
        reason: MinimumReplicasAvailable
        status: "True"
        type: Available
      - lastTransitionTime: "2024-12-30T11:19:59Z"
        lastUpdateTime: "2024-12-30T11:20:04Z"
        message: ReplicaSet "model-server-664885b79f" has successfully progressed.
        reason: NewReplicaSetAvailable
        status: "True"
        type: Progressing
      observedGeneration: 1
      readyReplicas: 2
      replicas: 2
      updatedReplicas: 2
  - apiVersion: apps/v1
    kind: Deployment
    metadata:
      annotations:
        deployment.kubernetes.io/revision: "1"
        meta.helm.sh/release-name: fastapi-release-prod
        meta.helm.sh/release-namespace: production
      creationTimestamp: "2024-12-30T11:19:59Z"
      generation: 1
      labels:
        app.kubernetes.io/managed-by: Helm
        app.kubernetes.io/name: redis
        app.kubernetes.io/part-of: fastapi-app
      name: redis
      namespace: prod
      resourceVersion: "5877"
      uid: 947ad68c-43e9-48a3-9930-50a6b64f0c58
    spec:
      progressDeadlineSeconds: 600
      replicas: 1
      revisionHistoryLimit: 10
      selector:
        matchLabels:
          app.kubernetes.io/name: redis
          role: master
      strategy:
        rollingUpdate:
          maxSurge: 25%
          maxUnavailable: 25%
        type: RollingUpdate
      template:
        metadata:
          creationTimestamp: null
          labels:
            app.kubernetes.io/name: redis
            role: master
        spec:
          containers:
          - args:
            - --requirepass
            - $(REDIS_PASSWORD)
            command:
            - redis-server
            env:
            - name: REDIS_PASSWORD
              valueFrom:
                secretKeyRef:
                  key: db_password
                  name: redis-secret-v1
            image: redis:7.4.1
            imagePullPolicy: IfNotPresent
            name: redis
            ports:
            - containerPort: 6379
              name: redis
              protocol: TCP
            resources:
              limits:
                cpu: 200m
                memory: 200Mi
            terminationMessagePath: /dev/termination-log
            terminationMessagePolicy: File
            volumeMounts:
            - mountPath: /data
              name: redis-storage
          dnsPolicy: ClusterFirst
          restartPolicy: Always
          schedulerName: default-scheduler
          securityContext: {}
          terminationGracePeriodSeconds: 30
          volumes:
          - name: redis-storage
            persistentVolumeClaim:
              claimName: redis-pvc
    status:
      availableReplicas: 1
      conditions:
      - lastTransitionTime: "2024-12-30T11:20:04Z"
        lastUpdateTime: "2024-12-30T11:20:04Z"
        message: Deployment has minimum availability.
        reason: MinimumReplicasAvailable
        status: "True"
        type: Available
      - lastTransitionTime: "2024-12-30T11:19:59Z"
        lastUpdateTime: "2024-12-30T11:20:04Z"
        message: ReplicaSet "redis-69cf9b5676" has successfully progressed.
        reason: NewReplicaSetAvailable
        status: "True"
        type: Progressing
      observedGeneration: 1
      readyReplicas: 1
      replicas: 1
      updatedReplicas: 1
  - apiVersion: apps/v1
    kind: Deployment
    metadata:
      annotations:
        deployment.kubernetes.io/revision: "1"
        meta.helm.sh/release-name: fastapi-release-prod
        meta.helm.sh/release-namespace: production
      creationTimestamp: "2024-12-30T11:19:59Z"
      generation: 1
      labels:
        app.kubernetes.io/managed-by: Helm
        app.kubernetes.io/name: web-server
        app.kubernetes.io/part-of: fastapi-app
      name: web-server
      namespace: prod
      resourceVersion: "5876"
      uid: 133ab6d3-ca64-43e3-bab1-59dae7c0cdf2
    spec:
      progressDeadlineSeconds: 600
      replicas: 2
      revisionHistoryLimit: 10
      selector:
        matchLabels:
          app.kubernetes.io/name: web-server
      strategy:
        rollingUpdate:
          maxSurge: 25%
          maxUnavailable: 25%
        type: RollingUpdate
      template:
        metadata:
          creationTimestamp: null
          labels:
            app.kubernetes.io/name: web-server
        spec:
          containers:
          - env:
            - name: REDIS_HOST
              valueFrom:
                configMapKeyRef:
                  key: hostname
                  name: redis-config-v1
            - name: REDIS_PORT
              valueFrom:
                configMapKeyRef:
                  key: port
                  name: redis-config-v1
            - name: REDIS_PASSWORD
              valueFrom:
                secretKeyRef:
                  key: db_password
                  name: redis-secret-v1
            - name: MODEL_SERVER_URL
              valueFrom:
                configMapKeyRef:
                  key: model_server_url
                  name: model-server-config-v1
            image: web-server:latest
            imagePullPolicy: Never
            name: web-server
            ports:
            - containerPort: 80
              name: http
              protocol: TCP
            resources: {}
            terminationMessagePath: /dev/termination-log
            terminationMessagePolicy: File
          dnsPolicy: ClusterFirst
          restartPolicy: Always
          schedulerName: default-scheduler
          securityContext: {}
          terminationGracePeriodSeconds: 30
    status:
      availableReplicas: 2
      conditions:
      - lastTransitionTime: "2024-12-30T11:20:04Z"
        lastUpdateTime: "2024-12-30T11:20:04Z"
        message: Deployment has minimum availability.
        reason: MinimumReplicasAvailable
        status: "True"
        type: Available
      - lastTransitionTime: "2024-12-30T11:19:59Z"
        lastUpdateTime: "2024-12-30T11:20:04Z"
        message: ReplicaSet "web-server-5c89b7fd87" has successfully progressed.
        reason: NewReplicaSetAvailable
        status: "True"
        type: Progressing
      observedGeneration: 1
      readyReplicas: 2
      replicas: 2
      updatedReplicas: 2
  - apiVersion: apps/v1
    kind: ReplicaSet
    metadata:
      annotations:
        deployment.kubernetes.io/desired-replicas: "1"
        deployment.kubernetes.io/max-replicas: "2"
        deployment.kubernetes.io/revision: "1"
      creationTimestamp: "2024-12-30T11:24:36Z"
      generation: 1
      labels:
        app.kubernetes.io/component: controller
        app.kubernetes.io/instance: ingress-nginx
        app.kubernetes.io/name: ingress-nginx
        gcp-auth-skip-secret: "true"
        pod-template-hash: bc57996ff
      name: ingress-nginx-controller-bc57996ff
      namespace: ingress-nginx
      ownerReferences:
      - apiVersion: apps/v1
        blockOwnerDeletion: true
        controller: true
        kind: Deployment
        name: ingress-nginx-controller
        uid: f7dc4043-2827-4cbd-8312-4f5a58aec950
      resourceVersion: "6300"
      uid: 5fcd67e7-65b4-408f-b284-c6b214d36e05
    spec:
      replicas: 1
      selector:
        matchLabels:
          app.kubernetes.io/component: controller
          app.kubernetes.io/instance: ingress-nginx
          app.kubernetes.io/name: ingress-nginx
          pod-template-hash: bc57996ff
      template:
        metadata:
          creationTimestamp: null
          labels:
            app.kubernetes.io/component: controller
            app.kubernetes.io/instance: ingress-nginx
            app.kubernetes.io/name: ingress-nginx
            gcp-auth-skip-secret: "true"
            pod-template-hash: bc57996ff
        spec:
          containers:
          - args:
            - /nginx-ingress-controller
            - --election-id=ingress-nginx-leader
            - --controller-class=k8s.io/ingress-nginx
            - --watch-ingress-without-class=true
            - --configmap=$(POD_NAMESPACE)/ingress-nginx-controller
            - --tcp-services-configmap=$(POD_NAMESPACE)/tcp-services
            - --udp-services-configmap=$(POD_NAMESPACE)/udp-services
            - --validating-webhook=:8443
            - --validating-webhook-certificate=/usr/local/certificates/cert
            - --validating-webhook-key=/usr/local/certificates/key
            env:
            - name: POD_NAME
              valueFrom:
                fieldRef:
                  apiVersion: v1
                  fieldPath: metadata.name
            - name: POD_NAMESPACE
              valueFrom:
                fieldRef:
                  apiVersion: v1
                  fieldPath: metadata.namespace
            - name: LD_PRELOAD
              value: /usr/local/lib/libmimalloc.so
            image: registry.k8s.io/ingress-nginx/controller:v1.11.2@sha256:d5f8217feeac4887cb1ed21f27c2674e58be06bd8f5184cacea2a69abaf78dce
            imagePullPolicy: IfNotPresent
            lifecycle:
              preStop:
                exec:
                  command:
                  - /wait-shutdown
            livenessProbe:
              failureThreshold: 5
              httpGet:
                path: /healthz
                port: 10254
                scheme: HTTP
              initialDelaySeconds: 10
              periodSeconds: 10
              successThreshold: 1
              timeoutSeconds: 1
            name: controller
            ports:
            - containerPort: 80
              hostPort: 80
              name: http
              protocol: TCP
            - containerPort: 443
              hostPort: 443
              name: https
              protocol: TCP
            - containerPort: 8443
              name: webhook
              protocol: TCP
            readinessProbe:
              failureThreshold: 3
              httpGet:
                path: /healthz
                port: 10254
                scheme: HTTP
              initialDelaySeconds: 10
              periodSeconds: 10
              successThreshold: 1
              timeoutSeconds: 1
            resources:
              requests:
                cpu: 100m
                memory: 90Mi
            securityContext:
              allowPrivilegeEscalation: true
              capabilities:
                add:
                - NET_BIND_SERVICE
                drop:
                - ALL
              runAsUser: 101
            terminationMessagePath: /dev/termination-log
            terminationMessagePolicy: File
            volumeMounts:
            - mountPath: /usr/local/certificates/
              name: webhook-cert
              readOnly: true
          dnsPolicy: ClusterFirst
          nodeSelector:
            kubernetes.io/os: linux
            minikube.k8s.io/primary: "true"
          restartPolicy: Always
          schedulerName: default-scheduler
          securityContext: {}
          serviceAccount: ingress-nginx
          serviceAccountName: ingress-nginx
          terminationGracePeriodSeconds: 0
          tolerations:
          - effect: NoSchedule
            key: node-role.kubernetes.io/master
            operator: Equal
          volumes:
          - name: webhook-cert
            secret:
              defaultMode: 420
              secretName: ingress-nginx-admission
    status:
      availableReplicas: 1
      fullyLabeledReplicas: 1
      observedGeneration: 1
      readyReplicas: 1
      replicas: 1
  - apiVersion: apps/v1
    kind: ReplicaSet
    metadata:
      annotations:
        deployment.kubernetes.io/desired-replicas: "1"
        deployment.kubernetes.io/max-replicas: "2"
        deployment.kubernetes.io/revision: "1"
      creationTimestamp: "2024-12-30T09:46:23Z"
      generation: 1
      labels:
        k8s-app: kube-dns
        pod-template-hash: 6f6b679f8f
      name: coredns-6f6b679f8f
      namespace: kube-system
      ownerReferences:
      - apiVersion: apps/v1
        blockOwnerDeletion: true
        controller: true
        kind: Deployment
        name: coredns
        uid: 7692e7bd-e741-4529-94fa-b3f3d056772c
      resourceVersion: "5476"
      uid: 0fc88bea-a82e-40e1-bf89-235b47d32db4
    spec:
      replicas: 1
      selector:
        matchLabels:
          k8s-app: kube-dns
          pod-template-hash: 6f6b679f8f
      template:
        metadata:
          creationTimestamp: null
          labels:
            k8s-app: kube-dns
            pod-template-hash: 6f6b679f8f
        spec:
          affinity:
            podAntiAffinity:
              preferredDuringSchedulingIgnoredDuringExecution:
              - podAffinityTerm:
                  labelSelector:
                    matchExpressions:
                    - key: k8s-app
                      operator: In
                      values:
                      - kube-dns
                  topologyKey: kubernetes.io/hostname
                weight: 100
          containers:
          - args:
            - -conf
            - /etc/coredns/Corefile
            image: registry.k8s.io/coredns/coredns:v1.11.1
            imagePullPolicy: IfNotPresent
            livenessProbe:
              failureThreshold: 5
              httpGet:
                path: /health
                port: 8080
                scheme: HTTP
              initialDelaySeconds: 60
              periodSeconds: 10
              successThreshold: 1
              timeoutSeconds: 5
            name: coredns
            ports:
            - containerPort: 53
              name: dns
              protocol: UDP
            - containerPort: 53
              name: dns-tcp
              protocol: TCP
            - containerPort: 9153
              name: metrics
              protocol: TCP
            readinessProbe:
              failureThreshold: 3
              httpGet:
                path: /ready
                port: 8181
                scheme: HTTP
              periodSeconds: 10
              successThreshold: 1
              timeoutSeconds: 1
            resources:
              limits:
                memory: 170Mi
              requests:
                cpu: 100m
                memory: 70Mi
            securityContext:
              allowPrivilegeEscalation: false
              capabilities:
                add:
                - NET_BIND_SERVICE
                drop:
                - ALL
              readOnlyRootFilesystem: true
            terminationMessagePath: /dev/termination-log
            terminationMessagePolicy: File
            volumeMounts:
            - mountPath: /etc/coredns
              name: config-volume
              readOnly: true
          dnsPolicy: Default
          nodeSelector:
            kubernetes.io/os: linux
          priorityClassName: system-cluster-critical
          restartPolicy: Always
          schedulerName: default-scheduler
          securityContext: {}
          serviceAccount: coredns
          serviceAccountName: coredns
          terminationGracePeriodSeconds: 30
          tolerations:
          - key: CriticalAddonsOnly
            operator: Exists
          - effect: NoSchedule
            key: node-role.kubernetes.io/control-plane
          volumes:
          - configMap:
              defaultMode: 420
              items:
              - key: Corefile
                path: Corefile
              name: coredns
            name: config-volume
    status:
      availableReplicas: 1
      fullyLabeledReplicas: 1
      observedGeneration: 1
      readyReplicas: 1
      replicas: 1
  - apiVersion: apps/v1
    kind: ReplicaSet
    metadata:
      annotations:
        deployment.kubernetes.io/desired-replicas: "1"
        deployment.kubernetes.io/max-replicas: "2"
        deployment.kubernetes.io/revision: "1"
      creationTimestamp: "2024-12-30T11:25:47Z"
      generation: 1
      labels:
        k8s-app: metrics-server
        pod-template-hash: 84c5f94fbc
      name: metrics-server-84c5f94fbc
      namespace: kube-system
      ownerReferences:
      - apiVersion: apps/v1
        blockOwnerDeletion: true
        controller: true
        kind: Deployment
        name: metrics-server
        uid: fa6a5982-379f-423a-b34f-1a2f0b6ccccd
      resourceVersion: "6402"
      uid: c9fa0347-3429-4264-909d-616eb8aeb75f
    spec:
      replicas: 1
      selector:
        matchLabels:
          k8s-app: metrics-server
          pod-template-hash: 84c5f94fbc
      template:
        metadata:
          creationTimestamp: null
          labels:
            k8s-app: metrics-server
            pod-template-hash: 84c5f94fbc
          name: metrics-server
        spec:
          containers:
          - args:
            - --cert-dir=/tmp
            - --secure-port=4443
            - --kubelet-preferred-address-types=InternalIP,ExternalIP,Hostname
            - --kubelet-use-node-status-port
            - --metric-resolution=60s
            - --kubelet-insecure-tls
            image: registry.k8s.io/metrics-server/metrics-server:v0.7.2@sha256:ffcb2bf004d6aa0a17d90e0247cf94f2865c8901dcab4427034c341951c239f9
            imagePullPolicy: IfNotPresent
            livenessProbe:
              failureThreshold: 3
              httpGet:
                path: /livez
                port: https
                scheme: HTTPS
              periodSeconds: 10
              successThreshold: 1
              timeoutSeconds: 1
            name: metrics-server
            ports:
            - containerPort: 4443
              name: https
              protocol: TCP
            readinessProbe:
              failureThreshold: 3
              httpGet:
                path: /readyz
                port: https
                scheme: HTTPS
              periodSeconds: 10
              successThreshold: 1
              timeoutSeconds: 1
            resources:
              requests:
                cpu: 100m
                memory: 200Mi
            securityContext:
              readOnlyRootFilesystem: true
              runAsNonRoot: true
              runAsUser: 1000
            terminationMessagePath: /dev/termination-log
            terminationMessagePolicy: File
            volumeMounts:
            - mountPath: /tmp
              name: tmp-dir
          dnsPolicy: ClusterFirst
          priorityClassName: system-cluster-critical
          restartPolicy: Always
          schedulerName: default-scheduler
          securityContext: {}
          serviceAccount: metrics-server
          serviceAccountName: metrics-server
          terminationGracePeriodSeconds: 30
          volumes:
          - emptyDir: {}
            name: tmp-dir
    status:
      availableReplicas: 1
      fullyLabeledReplicas: 1
      observedGeneration: 1
      readyReplicas: 1
      replicas: 1
  - apiVersion: apps/v1
    kind: ReplicaSet
    metadata:
      annotations:
        deployment.kubernetes.io/desired-replicas: "1"
        deployment.kubernetes.io/max-replicas: "2"
        deployment.kubernetes.io/revision: "1"
      creationTimestamp: "2024-12-30T11:25:39Z"
      generation: 1
      labels:
        k8s-app: dashboard-metrics-scraper
        pod-template-hash: c5db448b4
      name: dashboard-metrics-scraper-c5db448b4
      namespace: kubernetes-dashboard
      ownerReferences:
      - apiVersion: apps/v1
        blockOwnerDeletion: true
        controller: true
        kind: Deployment
        name: dashboard-metrics-scraper
        uid: e67c0f1d-1a86-4bb3-9e31-ee4f3132002a
      resourceVersion: "6379"
      uid: db1e6382-e320-45a5-9e35-70ebb342da9c
    spec:
      replicas: 1
      selector:
        matchLabels:
          k8s-app: dashboard-metrics-scraper
          pod-template-hash: c5db448b4
      template:
        metadata:
          annotations:
            seccomp.security.alpha.kubernetes.io/pod: runtime/default
          creationTimestamp: null
          labels:
            k8s-app: dashboard-metrics-scraper
            pod-template-hash: c5db448b4
        spec:
          containers:
          - image: docker.io/kubernetesui/metrics-scraper:v1.0.8@sha256:76049887f07a0476dc93efc2d3569b9529bf982b22d29f356092ce206e98765c
            imagePullPolicy: IfNotPresent
            livenessProbe:
              failureThreshold: 3
              httpGet:
                path: /
                port: 8000
                scheme: HTTP
              initialDelaySeconds: 30
              periodSeconds: 10
              successThreshold: 1
              timeoutSeconds: 30
            name: dashboard-metrics-scraper
            ports:
            - containerPort: 8000
              protocol: TCP
            resources: {}
            securityContext:
              allowPrivilegeEscalation: false
              readOnlyRootFilesystem: true
              runAsGroup: 2001
              runAsUser: 1001
            terminationMessagePath: /dev/termination-log
            terminationMessagePolicy: File
            volumeMounts:
            - mountPath: /tmp
              name: tmp-volume
          dnsPolicy: ClusterFirst
          nodeSelector:
            kubernetes.io/os: linux
          restartPolicy: Always
          schedulerName: default-scheduler
          securityContext: {}
          serviceAccount: kubernetes-dashboard
          serviceAccountName: kubernetes-dashboard
          terminationGracePeriodSeconds: 30
          tolerations:
          - effect: NoSchedule
            key: node-role.kubernetes.io/master
          volumes:
          - emptyDir: {}
            name: tmp-volume
    status:
      availableReplicas: 1
      fullyLabeledReplicas: 1
      observedGeneration: 1
      readyReplicas: 1
      replicas: 1
  - apiVersion: apps/v1
    kind: ReplicaSet
    metadata:
      annotations:
        deployment.kubernetes.io/desired-replicas: "1"
        deployment.kubernetes.io/max-replicas: "2"
        deployment.kubernetes.io/revision: "1"
      creationTimestamp: "2024-12-30T11:25:39Z"
      generation: 1
      labels:
        gcp-auth-skip-secret: "true"
        k8s-app: kubernetes-dashboard
        pod-template-hash: 695b96c756
      name: kubernetes-dashboard-695b96c756
      namespace: kubernetes-dashboard
      ownerReferences:
      - apiVersion: apps/v1
        blockOwnerDeletion: true
        controller: true
        kind: Deployment
        name: kubernetes-dashboard
        uid: 4d22a9b0-f026-47cf-a8f7-486284fab9c8
      resourceVersion: "6362"
      uid: 9d69dee3-6365-4ad7-9f63-26d13535392d
    spec:
      replicas: 1
      selector:
        matchLabels:
          k8s-app: kubernetes-dashboard
          pod-template-hash: 695b96c756
      template:
        metadata:
          creationTimestamp: null
          labels:
            gcp-auth-skip-secret: "true"
            k8s-app: kubernetes-dashboard
            pod-template-hash: 695b96c756
        spec:
          containers:
          - args:
            - --namespace=kubernetes-dashboard
            - --enable-skip-login
            - --disable-settings-authorizer
            image: docker.io/kubernetesui/dashboard:v2.7.0@sha256:2e500d29e9d5f4a086b908eb8dfe7ecac57d2ab09d65b24f588b1d449841ef93
            imagePullPolicy: IfNotPresent
            livenessProbe:
              failureThreshold: 3
              httpGet:
                path: /
                port: 9090
                scheme: HTTP
              initialDelaySeconds: 30
              periodSeconds: 10
              successThreshold: 1
              timeoutSeconds: 30
            name: kubernetes-dashboard
            ports:
            - containerPort: 9090
              protocol: TCP
            resources: {}
            securityContext:
              allowPrivilegeEscalation: false
              readOnlyRootFilesystem: true
              runAsGroup: 2001
              runAsUser: 1001
            terminationMessagePath: /dev/termination-log
            terminationMessagePolicy: File
            volumeMounts:
            - mountPath: /tmp
              name: tmp-volume
          dnsPolicy: ClusterFirst
          nodeSelector:
            kubernetes.io/os: linux
          restartPolicy: Always
          schedulerName: default-scheduler
          securityContext: {}
          serviceAccount: kubernetes-dashboard
          serviceAccountName: kubernetes-dashboard
          terminationGracePeriodSeconds: 30
          tolerations:
          - effect: NoSchedule
            key: node-role.kubernetes.io/master
          volumes:
          - emptyDir: {}
            name: tmp-volume
    status:
      availableReplicas: 1
      fullyLabeledReplicas: 1
      observedGeneration: 1
      readyReplicas: 1
      replicas: 1
  - apiVersion: apps/v1
    kind: ReplicaSet
    metadata:
      annotations:
        deployment.kubernetes.io/desired-replicas: "2"
        deployment.kubernetes.io/max-replicas: "3"
        deployment.kubernetes.io/revision: "1"
        meta.helm.sh/release-name: fastapi-release-prod
        meta.helm.sh/release-namespace: production
      creationTimestamp: "2024-12-30T11:19:59Z"
      generation: 1
      labels:
        app.kubernetes.io/name: model-server
        pod-template-hash: 664885b79f
      name: model-server-664885b79f
      namespace: prod
      ownerReferences:
      - apiVersion: apps/v1
        blockOwnerDeletion: true
        controller: true
        kind: Deployment
        name: model-server
        uid: bfecbf4c-d1b5-4ba4-acd1-1a1e6ed6adb6
      resourceVersion: "5865"
      uid: f93fce3f-d8c5-43a5-acce-44781d50db32
    spec:
      replicas: 2
      selector:
        matchLabels:
          app.kubernetes.io/name: model-server
          pod-template-hash: 664885b79f
      template:
        metadata:
          creationTimestamp: null
          labels:
            app.kubernetes.io/name: model-server
            pod-template-hash: 664885b79f
        spec:
          containers:
          - env:
            - name: REDIS_HOST
              valueFrom:
                configMapKeyRef:
                  key: hostname
                  name: redis-config-v1
            - name: REDIS_PORT
              valueFrom:
                configMapKeyRef:
                  key: port
                  name: redis-config-v1
            - name: REDIS_PASSWORD
              valueFrom:
                secretKeyRef:
                  key: db_password
                  name: redis-secret-v1
            - name: MODEL_NAME
              valueFrom:
                configMapKeyRef:
                  key: model_name
                  name: model-server-config-v1
            image: model-server:latest
            imagePullPolicy: Never
            name: model-server
            ports:
            - containerPort: 80
              name: http
              protocol: TCP
            resources:
              limits:
                cpu: "1"
                memory: 2Gi
            terminationMessagePath: /dev/termination-log
            terminationMessagePolicy: File
          dnsPolicy: ClusterFirst
          restartPolicy: Always
          schedulerName: default-scheduler
          securityContext: {}
          terminationGracePeriodSeconds: 30
    status:
      availableReplicas: 2
      fullyLabeledReplicas: 2
      observedGeneration: 1
      readyReplicas: 2
      replicas: 2
  - apiVersion: apps/v1
    kind: ReplicaSet
    metadata:
      annotations:
        deployment.kubernetes.io/desired-replicas: "1"
        deployment.kubernetes.io/max-replicas: "2"
        deployment.kubernetes.io/revision: "1"
        meta.helm.sh/release-name: fastapi-release-prod
        meta.helm.sh/release-namespace: production
      creationTimestamp: "2024-12-30T11:19:59Z"
      generation: 1
      labels:
        app.kubernetes.io/name: redis
        pod-template-hash: 69cf9b5676
        role: master
      name: redis-69cf9b5676
      namespace: prod
      ownerReferences:
      - apiVersion: apps/v1
        blockOwnerDeletion: true
        controller: true
        kind: Deployment
        name: redis
        uid: 947ad68c-43e9-48a3-9930-50a6b64f0c58
      resourceVersion: "5873"
      uid: d4b047b4-9892-4b81-aabe-2afc086c62f7
    spec:
      replicas: 1
      selector:
        matchLabels:
          app.kubernetes.io/name: redis
          pod-template-hash: 69cf9b5676
          role: master
      template:
        metadata:
          creationTimestamp: null
          labels:
            app.kubernetes.io/name: redis
            pod-template-hash: 69cf9b5676
            role: master
        spec:
          containers:
          - args:
            - --requirepass
            - $(REDIS_PASSWORD)
            command:
            - redis-server
            env:
            - name: REDIS_PASSWORD
              valueFrom:
                secretKeyRef:
                  key: db_password
                  name: redis-secret-v1
            image: redis:7.4.1
            imagePullPolicy: IfNotPresent
            name: redis
            ports:
            - containerPort: 6379
              name: redis
              protocol: TCP
            resources:
              limits:
                cpu: 200m
                memory: 200Mi
            terminationMessagePath: /dev/termination-log
            terminationMessagePolicy: File
            volumeMounts:
            - mountPath: /data
              name: redis-storage
          dnsPolicy: ClusterFirst
          restartPolicy: Always
          schedulerName: default-scheduler
          securityContext: {}
          terminationGracePeriodSeconds: 30
          volumes:
          - name: redis-storage
            persistentVolumeClaim:
              claimName: redis-pvc
    status:
      availableReplicas: 1
      fullyLabeledReplicas: 1
      observedGeneration: 1
      readyReplicas: 1
      replicas: 1
  - apiVersion: apps/v1
    kind: ReplicaSet
    metadata:
      annotations:
        deployment.kubernetes.io/desired-replicas: "2"
        deployment.kubernetes.io/max-replicas: "3"
        deployment.kubernetes.io/revision: "1"
        meta.helm.sh/release-name: fastapi-release-prod
        meta.helm.sh/release-namespace: production
      creationTimestamp: "2024-12-30T11:19:59Z"
      generation: 1
      labels:
        app.kubernetes.io/name: web-server
        pod-template-hash: 5c89b7fd87
      name: web-server-5c89b7fd87
      namespace: prod
      ownerReferences:
      - apiVersion: apps/v1
        blockOwnerDeletion: true
        controller: true
        kind: Deployment
        name: web-server
        uid: 133ab6d3-ca64-43e3-bab1-59dae7c0cdf2
      resourceVersion: "5871"
      uid: f824fd91-34c3-4ed4-aa00-0a635ddff1ed
    spec:
      replicas: 2
      selector:
        matchLabels:
          app.kubernetes.io/name: web-server
          pod-template-hash: 5c89b7fd87
      template:
        metadata:
          creationTimestamp: null
          labels:
            app.kubernetes.io/name: web-server
            pod-template-hash: 5c89b7fd87
        spec:
          containers:
          - env:
            - name: REDIS_HOST
              valueFrom:
                configMapKeyRef:
                  key: hostname
                  name: redis-config-v1
            - name: REDIS_PORT
              valueFrom:
                configMapKeyRef:
                  key: port
                  name: redis-config-v1
            - name: REDIS_PASSWORD
              valueFrom:
                secretKeyRef:
                  key: db_password
                  name: redis-secret-v1
            - name: MODEL_SERVER_URL
              valueFrom:
                configMapKeyRef:
                  key: model_server_url
                  name: model-server-config-v1
            image: web-server:latest
            imagePullPolicy: Never
            name: web-server
            ports:
            - containerPort: 80
              name: http
              protocol: TCP
            resources: {}
            terminationMessagePath: /dev/termination-log
            terminationMessagePolicy: File
          dnsPolicy: ClusterFirst
          restartPolicy: Always
          schedulerName: default-scheduler
          securityContext: {}
          terminationGracePeriodSeconds: 30
    status:
      availableReplicas: 2
      fullyLabeledReplicas: 2
      observedGeneration: 1
      readyReplicas: 2
      replicas: 2
  - apiVersion: batch/v1
    kind: Job
    metadata:
      annotations:
        kubectl.kubernetes.io/last-applied-configuration: |
          {"apiVersion":"batch/v1","kind":"Job","metadata":{"annotations":{},"labels":{"app.kubernetes.io/component":"admission-webhook","app.kubernetes.io/instance":"ingress-nginx","app.kubernetes.io/name":"ingress-nginx"},"name":"ingress-nginx-admission-create","namespace":"ingress-nginx"},"spec":{"template":{"metadata":{"labels":{"app.kubernetes.io/component":"admission-webhook","app.kubernetes.io/instance":"ingress-nginx","app.kubernetes.io/name":"ingress-nginx"},"name":"ingress-nginx-admission-create"},"spec":{"containers":[{"args":["create","--host=ingress-nginx-controller-admission,ingress-nginx-controller-admission.$(POD_NAMESPACE).svc","--namespace=$(POD_NAMESPACE)","--secret-name=ingress-nginx-admission"],"env":[{"name":"POD_NAMESPACE","valueFrom":{"fieldRef":{"fieldPath":"metadata.namespace"}}}],"image":"registry.k8s.io/ingress-nginx/kube-webhook-certgen:v1.4.3@sha256:a320a50cc91bd15fd2d6fa6de58bd98c1bd64b9a6f926ce23a600d87043455a3","imagePullPolicy":"IfNotPresent","name":"create","securityContext":{"allowPrivilegeEscalation":false}}],"nodeSelector":{"kubernetes.io/os":"linux","minikube.k8s.io/primary":"true"},"restartPolicy":"OnFailure","securityContext":{"runAsNonRoot":true,"runAsUser":2000},"serviceAccountName":"ingress-nginx-admission"}}}}
      creationTimestamp: "2024-12-30T11:24:36Z"
      generation: 1
      labels:
        app.kubernetes.io/component: admission-webhook
        app.kubernetes.io/instance: ingress-nginx
        app.kubernetes.io/name: ingress-nginx
      name: ingress-nginx-admission-create
      namespace: ingress-nginx
      resourceVersion: "6174"
      uid: 4656eb27-4c5b-4f8a-8a24-dd97448d8f05
    spec:
      backoffLimit: 6
      completionMode: NonIndexed
      completions: 1
      manualSelector: false
      parallelism: 1
      podReplacementPolicy: TerminatingOrFailed
      selector:
        matchLabels:
          batch.kubernetes.io/controller-uid: 4656eb27-4c5b-4f8a-8a24-dd97448d8f05
      suspend: false
      template:
        metadata:
          creationTimestamp: null
          labels:
            app.kubernetes.io/component: admission-webhook
            app.kubernetes.io/instance: ingress-nginx
            app.kubernetes.io/name: ingress-nginx
            batch.kubernetes.io/controller-uid: 4656eb27-4c5b-4f8a-8a24-dd97448d8f05
            batch.kubernetes.io/job-name: ingress-nginx-admission-create
            controller-uid: 4656eb27-4c5b-4f8a-8a24-dd97448d8f05
            job-name: ingress-nginx-admission-create
          name: ingress-nginx-admission-create
        spec:
          containers:
          - args:
            - create
            - --host=ingress-nginx-controller-admission,ingress-nginx-controller-admission.$(POD_NAMESPACE).svc
            - --namespace=$(POD_NAMESPACE)
            - --secret-name=ingress-nginx-admission
            env:
            - name: POD_NAMESPACE
              valueFrom:
                fieldRef:
                  apiVersion: v1
                  fieldPath: metadata.namespace
            image: registry.k8s.io/ingress-nginx/kube-webhook-certgen:v1.4.3@sha256:a320a50cc91bd15fd2d6fa6de58bd98c1bd64b9a6f926ce23a600d87043455a3
            imagePullPolicy: IfNotPresent
            name: create
            resources: {}
            securityContext:
              allowPrivilegeEscalation: false
            terminationMessagePath: /dev/termination-log
            terminationMessagePolicy: File
          dnsPolicy: ClusterFirst
          nodeSelector:
            kubernetes.io/os: linux
            minikube.k8s.io/primary: "true"
          restartPolicy: OnFailure
          schedulerName: default-scheduler
          securityContext:
            runAsNonRoot: true
            runAsUser: 2000
          serviceAccount: ingress-nginx-admission
          serviceAccountName: ingress-nginx-admission
          terminationGracePeriodSeconds: 30
    status:
      completionTime: "2024-12-30T11:24:55Z"
      conditions:
      - lastProbeTime: "2024-12-30T11:24:55Z"
        lastTransitionTime: "2024-12-30T11:24:55Z"
        message: Reached expected number of succeeded pods
        reason: CompletionsReached
        status: "True"
        type: SuccessCriteriaMet
      - lastProbeTime: "2024-12-30T11:24:55Z"
        lastTransitionTime: "2024-12-30T11:24:55Z"
        message: Reached expected number of succeeded pods
        reason: CompletionsReached
        status: "True"
        type: Complete
      ready: 0
      startTime: "2024-12-30T11:24:37Z"
      succeeded: 1
      terminating: 0
      uncountedTerminatedPods: {}
  - apiVersion: batch/v1
    kind: Job
    metadata:
      annotations:
        kubectl.kubernetes.io/last-applied-configuration: |
          {"apiVersion":"batch/v1","kind":"Job","metadata":{"annotations":{},"labels":{"app.kubernetes.io/component":"admission-webhook","app.kubernetes.io/instance":"ingress-nginx","app.kubernetes.io/name":"ingress-nginx"},"name":"ingress-nginx-admission-patch","namespace":"ingress-nginx"},"spec":{"template":{"metadata":{"labels":{"app.kubernetes.io/component":"admission-webhook","app.kubernetes.io/instance":"ingress-nginx","app.kubernetes.io/name":"ingress-nginx"},"name":"ingress-nginx-admission-patch"},"spec":{"containers":[{"args":["patch","--webhook-name=ingress-nginx-admission","--namespace=$(POD_NAMESPACE)","--patch-mutating=false","--secret-name=ingress-nginx-admission","--patch-failure-policy=Fail"],"env":[{"name":"POD_NAMESPACE","valueFrom":{"fieldRef":{"fieldPath":"metadata.namespace"}}}],"image":"registry.k8s.io/ingress-nginx/kube-webhook-certgen:v1.4.3@sha256:a320a50cc91bd15fd2d6fa6de58bd98c1bd64b9a6f926ce23a600d87043455a3","imagePullPolicy":"IfNotPresent","name":"patch","securityContext":{"allowPrivilegeEscalation":false}}],"nodeSelector":{"kubernetes.io/os":"linux","minikube.k8s.io/primary":"true"},"restartPolicy":"OnFailure","securityContext":{"runAsNonRoot":true,"runAsUser":2000},"serviceAccountName":"ingress-nginx-admission"}}}}
      creationTimestamp: "2024-12-30T11:24:37Z"
      generation: 1
      labels:
        app.kubernetes.io/component: admission-webhook
        app.kubernetes.io/instance: ingress-nginx
        app.kubernetes.io/name: ingress-nginx
      name: ingress-nginx-admission-patch
      namespace: ingress-nginx
      resourceVersion: "6180"
      uid: 251e2330-8e81-4f38-83ac-3fba38d28aa4
    spec:
      backoffLimit: 6
      completionMode: NonIndexed
      completions: 1
      manualSelector: false
      parallelism: 1
      podReplacementPolicy: TerminatingOrFailed
      selector:
        matchLabels:
          batch.kubernetes.io/controller-uid: 251e2330-8e81-4f38-83ac-3fba38d28aa4
      suspend: false
      template:
        metadata:
          creationTimestamp: null
          labels:
            app.kubernetes.io/component: admission-webhook
            app.kubernetes.io/instance: ingress-nginx
            app.kubernetes.io/name: ingress-nginx
            batch.kubernetes.io/controller-uid: 251e2330-8e81-4f38-83ac-3fba38d28aa4
            batch.kubernetes.io/job-name: ingress-nginx-admission-patch
            controller-uid: 251e2330-8e81-4f38-83ac-3fba38d28aa4
            job-name: ingress-nginx-admission-patch
          name: ingress-nginx-admission-patch
        spec:
          containers:
          - args:
            - patch
            - --webhook-name=ingress-nginx-admission
            - --namespace=$(POD_NAMESPACE)
            - --patch-mutating=false
            - --secret-name=ingress-nginx-admission
            - --patch-failure-policy=Fail
            env:
            - name: POD_NAMESPACE
              valueFrom:
                fieldRef:
                  apiVersion: v1
                  fieldPath: metadata.namespace
            image: registry.k8s.io/ingress-nginx/kube-webhook-certgen:v1.4.3@sha256:a320a50cc91bd15fd2d6fa6de58bd98c1bd64b9a6f926ce23a600d87043455a3
            imagePullPolicy: IfNotPresent
            name: patch
            resources: {}
            securityContext:
              allowPrivilegeEscalation: false
            terminationMessagePath: /dev/termination-log
            terminationMessagePolicy: File
          dnsPolicy: ClusterFirst
          nodeSelector:
            kubernetes.io/os: linux
            minikube.k8s.io/primary: "true"
          restartPolicy: OnFailure
          schedulerName: default-scheduler
          securityContext:
            runAsNonRoot: true
            runAsUser: 2000
          serviceAccount: ingress-nginx-admission
          serviceAccountName: ingress-nginx-admission
          terminationGracePeriodSeconds: 30
    status:
      completionTime: "2024-12-30T11:24:56Z"
      conditions:
      - lastProbeTime: "2024-12-30T11:24:56Z"
        lastTransitionTime: "2024-12-30T11:24:56Z"
        message: Reached expected number of succeeded pods
        reason: CompletionsReached
        status: "True"
        type: SuccessCriteriaMet
      - lastProbeTime: "2024-12-30T11:24:56Z"
        lastTransitionTime: "2024-12-30T11:24:56Z"
        message: Reached expected number of succeeded pods
        reason: CompletionsReached
        status: "True"
        type: Complete
      ready: 0
      startTime: "2024-12-30T11:24:37Z"
      succeeded: 1
      terminating: 0
      uncountedTerminatedPods: {}
  kind: List
  metadata:
    resourceVersion: ""
  ```