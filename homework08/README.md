# HW 08: Holidapp
## Project Description
To observe & use the dataset provided by the HUGO Gene Nomenclature Committee (HGNC), that holds the unique id & meaningful name for each gene. With this homework we'll utilize Redis via a Flask interface, and the help of kubernetes structures. As such I've implemented PVCs, deployments and services. In addition, we're now utilizing two redis databases at once. One for storing the dataset, and using that database to construct a simple plot, which is then stored and accessed via second database.

## Project Objective
The purpose of this assignment was to allow us to become more comfortable with the utilization of Redis,Flask, and combination of Docker. Additonally, to allow 
us to understand the structure behind kubernetes clusters & the flow between PVCs, deployments and service files. As such, we had to create a final product that connected back to our flask & redis application developed in homework six. Additionall,y it was to further demonstrate the potential interconnectivity between programs, datasets & databases by utilizing two redis databases at once.

## Data
The data used with this homework is a JSON file that contains information about the genes found on the human genome. This dataset is regulated by the HGNC, a group that is in charge of naming each gene. This dataset holds the information on every gene that the HGNC has named.

As such the data can be found here: (https://www.genenames.org/download/archive/)

## Scripts, Files & Flask Routes:
`gene_api.py`:
Is the Flask application that allows us to make queries into the dataset. It aids us in finding specific hgnc_ids & returning the data in a digestible manner.


As such here are the following routes used in the aplication:

| Route         | Method        | Return |
| ------------- |:-------------:| ------------- |
| `/data`     | GET | Return all data in Redis database | 
| | DELETE |  Delete data from Redis database | 
| | POST | Post data into Redis database | 
| `/genes`    | GET |  Returns the unique hgnc_id of all the genes in the data set      |
| `/genes/<hgnc_id>`  | GET |  Return all data associated with a specific hgnc_id |
|`/image`    | GET | Returns plot file from Redis_image database|
| | DELETE |  Deletes plot from Redis_image database | 
| | POST | Posts plot into Redis_image database | 

### Note: 
<hgnc_id> is a string variable that has the following shape: HGNC:123, where 123 can be any unique ID value as given from the HGNC.

`Dockerfile`: Holds the commands that allow the docker image associated with gene_api, to build the container when ran

`docker-compose.yml`: YAML script controlling the containerization and port destination of the flask & redis applications

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
$docker run -it --rm -p <dockerhubusername>/<script>:<version>
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
$kubectl exec -it  py-debug-deployment-f484b4b99-898lt -- /bin/bash
root@py-debug-deployment-f484b4b99-898lt:/#
```
Before we are able to run curl commands to the Flask app we need to get the flask service IP. 
```
$ kubectl get services
NAME                        TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)    AGE
kebabo-test-flask-service   ClusterIP   10.233.61.208   <none>        5000/TCP   24m
kebabo-test-redis-service   ClusterIP   10.233.27.113   <none>        6379/TCP   41m
```
We are now in the bash of our debug pod where we're able to run curl commands.

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
