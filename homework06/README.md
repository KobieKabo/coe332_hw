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
