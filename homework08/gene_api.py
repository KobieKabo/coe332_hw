import json
import redis
import requests
import csv
import os
import io
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
    redis_ip = os.environ.get('REDIS-IP')
    if not redis_ip:
        raise Exception()
    return redis.Redis(host = redis_ip, port=6379, db=0, decode_responses = True)

def get_redis_image():
    """
    Constructs the redis db thats to be used for image data storage.
    Args: none
    Returns: A redis client
    """
    redis_ip = os.environ.get('REDIS-IP')
    if not redis_ip:
        raise Exception()
    return redis.Redis(host=redis_ip, port=6379, db=1)

rd = get_redis()

rd_image = get_redis_image()

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

    if request.method == 'GET':
        data_list = []
        for item in rd.keys():
            gene_list.append(json.loads(rd.get(key)))
        return data_list

    elif request.method == 'POST':
        response = requests.get(url= 'https://ftp.ebi.ac.uk/pub/databases/genenames/hgnc/json/hgnc_complete_set.json')
        for item in response.json()['response']['docs']:
            key = f'{item["hgnc_id"]}'
            rd.set(key, json.dumps(item))
        return 'Data has been posted\n'

    elif request.method == 'DELETE':
        rd.flushdb()
        return f'Data has been deleted.\n'

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

    gene_IDS = []

    for key in rd.keys():
        gene_IDS.append(key)
    return gene_IDS

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

@app.route('/image', methods = ['GET','POST','DELETE'])
def handle_image():
    """
    Method that handles the dataset we're working with.
    Args: None
    Curl Methods:
        Get: Returns the image from redis image_db
        Post: posts the image into the redis image_db
        Delete: deletes the image from the redis image_db
    Returns:
        Get: A plot of some of the data in the dataset
        Post: Puts a plot image in the redis image_db
        Delete: Removes a plot image in the redis image_db

    """
    if request.method == 'DELETE':
        rd_image.flushdb()
        return 'The plot has been removed from the redis database.\n'

    elif request.method == 'POST':
        keys = rd.keys()
        if not keys:
            return 'No data is available.\n'

        gene_locus_type = ['pseudogene','gene with protein product','RNA, long non-coding','other']
        gene_locus_type_counter = [0,0,0,0]
        percentages_locus = [0,0,0,0]
        counter = 0

        for key in keys:
            value = rd.hget(key, 'locus_type')
            if value in gene_locus_type:
                index = gene_locus_type(value)
                gene_locus_type_counter[index] += 1
            else:
                gene_locus_type_counter[3] += 1

        counter = sum(gene_locus_type_counter)

        for i in gene_locus_type_counter:
            if i == 0:
                percentages_locus.append(0)
            else:
                percentages_locus.append(i/counter)

        labels = [gene_locus_type[i] for i in range(len(percentages_locus))]

        values = [percentages_locus[i] for i in range(len(percentage_locus))]

        plt.pie(values, labels=labels, autopct='%1.1f%%')
        plt.title('Gene Locus Type Distribution')
        plt.axis('equal')

        buf = io.BytesIO()
        plt.savefig(buf, format ='jpg')
        buf.seef(0)

        rd_image.set('image', buf.getvalue())

        return 'Image has been posted.\n'


    elif request.method == 'GET':
        image = rd_image.get('image')
        buf = io.BytesIO(image)
        buf.seek(0)

        existing_images = rd_image.keys() == 0

        file_name = f'image{existing_images}.jpg'

        return send_file(buf, mimetype = 'image/jpg')

    else:
        return 'The method used is not supported. Please use GET, DELETE, or POST.'

if __name__ == '__main__':
    app.run(debug = True, host = '0.0.0.0')
