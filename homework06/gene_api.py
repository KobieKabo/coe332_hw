import json
import redis
import requests
import matplotlib.pyplot as plt
import numpy as np
from flask import Flask, request

app = Flask(__name__)

def get_redis():
    """
    Constructs the redis client that's used to store data.

    Args: none

    Returns: A redis client
    """
    return redis.Redis(host = 'redis-db', port=6379, db=0, decode_responses = True)

rd = get_redis()

@app.route('/data', methods = ['GET','POST','DELETE'])
def handle_data():
    """
    Method that handles the dataset we're working with.

    Args: None

    Curl Methods:
        Get: Returns data from redis db
        Post: posts data into the redis db
        Delete: deletes the data from the redis db

    Returns:
        Get: A list of the dataset
        Post: A string declaring the data as posted
        Delete: A string declaring the data as deleted
    """
    global rd

    if request.method == 'DELETE':
        rd.flushdb()
        return 'Data has been deleted.\n'
    
    elif request.method == 'POST':
        r = requests.get(url = 'https://ftp.ebi.ac.uk/pub/databases/genenames/hgnc/json/hgnc_complete_set.json')
        gene_data = r.json()

        for item in gene_data['response']['docs']:
            key = f'{item[hgnc_id]}'
            rd.hset(key, mapping = item)
        return 'Data has been posted.\n'

    elif request.method == 'GET':
        data_list = []
        for item in rd.keys():
            data_list.append(rd.hgetall(item))
        return data_list
    
    else:
        return 'An incorrect method was provided. Please use POST, GET or DELETE.\n'

@app.route('/genes', methods = ['GET'])
def get_all_hgncID() -> list:
    """
    Creates a json formated list of all the hgnc gene IDs.

    Args: 
    None

    Returns:
        List of the hgnc_id's within the dataset    
    """

    geneIDs = []

    for key in rd.keys():
        geneIDs.append(key)
    return geneIDs

@app.route('/genes.<hgnc_id>', methods = ['GET'])
def get_hgnc_data(hgnc_id) -> dict:
    """
    Returns all of the information associated with a specific hgnc_id

    Args: None

    Returns:
        A dictionary of the data associated with the given hgnc_id
    """
    if len(rd.keys()) == 0:
        return 'Database is empty. please re-post the data.\n'
    
    for key in rd.keys():
        if str(key) == str(hgnc_id):
            return json.loads(rd.get(key))

    return 'The given hgnc_id did not have a match. Please try another.\n'

@app.route('/plot', methods = ['GET'])
def get_sine_plot():
    """
    Returns a simple sine plot & saves the image to the redis db

    Args: 
        none

    Returns:
        A plot png to the redis db
    """
    x = np.linspace(0, 2*np.pi, 50)
    plt.plot(x, np.sin(x),'r-x', label='Sin(x)')
    plt.legend()
    plt.xlabel('Rads')
    plt.ylabel('Amplitude')
    plt.title('Sine Wave')

    plt.savefig('my_sinewave.png')
    
    sineFigure_bytes = open('/tmp/my_sinewave.png','rb').read()

    rd.set('key',sineFigure_bytes)

if __name__ == '__main__':
    app.run(debug = True, host = '0.0.0.0')
