# HW 07: Containerized Flask Application for HGNC Human Genome Data Using Redis Database
## Purpose
Currently the non-profit Humand Genome Organization (HUGO) which oversees the HUGO Gene Nomenclature Commmittee (HGNC) has approved almost 43,000 symbols (genes). It is important that there are standardize names for genes to minimize confusion and make it much easier to work with genes. Due to the work of the HGNC we always know that we are talking about the same gene! 

As mentioned there are nearly 43,0000 symbols so it can be difficult to search through the data and get the information you need. This project contianerizes a flask application which is deisgned to make it much eaiser to find the needed gene and information. It also creates a base for developers to build upon the application and create interesting projects.   
## Data
The public [data](https://www.genenames.org/download/archive/) used is provided and maintained by HUGO. At the bottom you will find all of the different formats. The one used for this is 'Current JSON format hgnc_complete_set file'. Furthemore, within the /genes/<hgnc_id> route you will find much more detailed information about what the dataset contains.

## Important Files
**gene_api.py**: Flask app containing all of the routes allowing user to make a request and get a response. It also contains the code regarding redis, a noSQL database, which allows us to store the data. This is important so that all the data is stored in the case that the flask application stops.

**Dockerfile**: Containerizes the gene_api.py application. Containerization is important as it allows the script to function the same despite the host device. It will install the necessary libraries used such as Flask, Redis, JSON, and Python. It also makes it easy to share the application once it has been pushed to Docker Hub.

**docker-compose.yaml**: Makes it much easier to run and stop the entire application. Brlow is the command to launch the application along with redis.  
```
$ docker-compose up -d
```
Closing the application:
```
$ docker-compose down
```
All other files relate to Kubernetes and information about them can be found in the Kubernetes section.

## Pull and use image from Docker Hub
1. Clone this repository onto your machine & make a directory named data.
2. Pull the image from dockerhub.
```
$dockerpull kobiekabo/gene_api:hw07-1.0
```
3. Use docker-compose
```
$ docker-compose up -d
```
You can now use curl commands.

## Build new image from Docker file
If you wish to edit or tailor the code to your needs you can also build your own image. Note that 
1. Clone repository onto your machine & make a directory named data.
2. Create docker image
```
$docker build -t <dockerhubusername>/<script>:<version> .
```
3.Running the image:
```
$docker run -it --rm -p <dockerhubusername>/<script name without the .py>:<version>
```   
### Pushing the image to DockerHub
If you wish to push the image to DockerHub:
```
$docker push <dockerhubusername>/<script name without the .py>:<version>
```
4. Use docker-compose
```
$ docker-compose up -d
```
You can now use curl commands.

## Kubernetes 
Kubernetes is a container orchestration system that supports Docker. Follow instructions below to run the gene_api app on a Kubernetes cluster:
```
$ kubectl apply -f kebabo-test-redis-pvc.yml 
$ kubectl apply -f kebabo-test-redis-deployment.yml
$ kubectl apply -f kebabo-test-redis-service.yml
$ kubectl apply -f kebabo-test-flask-deployment.yml
$ kubectl apply -f kebabo-test-flask-service.yml
$ kubectl apply -f kebabo-python-debug.yml
```
An output declaring the PVC, deployment or service being created, updated, or unchanged will then follow.
### Kubernetes yml Files

**kebabo-test-redis-pvc.yml**: creates a persistant volume claim for Redis database.

**kebabo-test-redis-deployment.yml**: creates deployment for Redis database

**kebabo-test-redis-service.yml**: creates Redis service which allows us to have a persistent IP address to use with the Redis database. 

**kebabo-test-flask-deployment.yml**: creates a deployment for gene_api image from dockerhub. 

**kebabo-test-flask-service.yml**: creates Flask service which allows us to have a persistent IP address to use with our Flask application.

### Using Kubernetes cluster
```
$kubectl get pods
NAME                                            READY   STATUS    RESTARTS   AGE
kebabo-test-flask-deployment-6859c57db6-bp6db   1/1     Running   0          8m55s
kebabo-test-redis-deployment-697c4cc6d7-dxj56   1/1     Running   0          43m
py-debug-deployment-f484b4b99-898lt             1/1     Running   0          18m
```
We will now access the bash within the py-debug pod
```
$kubectl exec -it  py-debug-deployment-f484b4b99-t6mvf -- /bin/bash
root@py-debug-deployment-f484b4b99-t6mvf:/#
```
Before we are able to run curl commands to the Flask app we need to get the flask service IP. 
```
$ kubectl get services
NAME                        TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)    AGE
kebabo-test-flask-service   ClusterIP   10.233.61.208   <none>        5000/TCP   24m
kebabo-test-redis-service   ClusterIP   10.233.27.113   <none>        6379/TCP   41m
```
We are now in the bash of our debug pod where we're able to run curl commands.
```

```
### Notes

If you plan on using your own image and Kubernetes you will need to push the image to dockerhub. Instructions on how to do this are above. You will then need to modify the kebabo-test-flask-deployment.yml file. Replace the value of the image key with your own image.

```
spec:
      containers:
        - name: flask-container
          imagePullPolicy: Always
          image: kobiekabo/gene_api:hw7-1.0
          ports:
          - name: flask
            containerPort: 5000
```

## Usage

Note that if you are not using Kubernetes you will need to modify the gene_api.py file. Within line 18 change host='kebabo-test-redis-service' to host='redis-db'

| Route | Method | Description |
| --- | --- | --- |
| `/data` | POST | Store data into redis |
| | GET | Return all data from redis |
| | DELETE | Delete all data in redis |
| `/genes` | GET | Return json-formatted list of all the hgnc_ids |
| `/genes/<hgnc_id>` | GET | Return all data associated with <hgnc_id> |
