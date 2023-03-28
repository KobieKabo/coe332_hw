# Homework 6: 'Say it Ain't Genes'

#### Project Description:
To observe & use the dataset provided by the HUGO Gene Nomenclature Committee (HGNC), that holds the unique id & meaningful name for each gene. With this homework we'll 
utilize Redis via a Flask interface.

#### Project Objective:
The purpose of this assignment was to allow us to become more comfortable with the utilization of Redis, and become capable to 
employing it via containerization with Docker.

### Data:
The data used with this homework is a JSON file that contains information about the genes found on the human genome. This dataset is regulated by the HGNC, a group that
is in charge of naming each gene. This dataset holds the information on every gene that the HGNC has named.

As such the data can be found here: (https://www.genenames.org/download/archive/)

## Scripts & Flask Routes:
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

### Note: 
<hgnc_id> is a string variable that has the following shape: HGNC:123, where 123 can be any unique ID value as given from the HGNC.

`Dockerfile`: Holds the commands that allow the docker image associated with gene_api, to build the container when ran
`docker-compose.yml`: YAML script controlling the containerization and port destination of the flask & redis applications

## Installation & Setup:
#### note:
before use, ensure that you have a directory named 'data' created by you the user to ensure writing privileges.
```
$ mkdir data
```
### Method 1: Pulling my existing Docker Image
To pull down my existing docker image simply use the following command:
```
docker pull kobiekabo/gene_api:1.0
```
This will pull down my image from Docker Hub, and can be checked with the `docker images` command

### Method 2: Creating your own image
To create your own image you'll need to both edit the compose file, & use the docker build commands.
Firstly use:
```
docker build -t <yourdockerusername>/<codename>:<version>
```
Then go into the docker-compose file & edit the following line to make sure it matches up with what you chose for you image name.
```
image: kobiekabo/gene_api:1.0
```
You'd be replacing my username with yours, and gene_api:1.0 with whatever you chose to name your image.

## Launching the application:
To launch the application we simply need to use the following command:
```
$ docker-compose up
```
yielding a result that should look like the following:
```
Starting homework06_redis-db_1 ... done
.
.
.
flask-app_1  |  * Debugger is active!
flask-app_1  |  * Debugger PIN: 411-831-197
```
The flask application can now be curled with the routes from above!
To close the application simply do the following:
```
$ docker-compose down
```
yielding a result like the following:
```
Stopping homework06_flask-app_1 ... done
Stopping homework06_redis-db_1  ... done
Removing homework06_flask-app_1 ... done
Removing homework06_redis-db_1  ... done
Removing network homework06_default
```
