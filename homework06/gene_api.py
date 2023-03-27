from flask import Flask, request
import json
import requests
import redis

app = Flask(__name__)

def get_redis_client():
    return redis.Redis(host='127.0.0.1', port=6379, db=0, decode_responses=True)

rd = get_redis_client

def data_status():
    global data_state
    if data_state == False:
        return 'Data has been deleted. Please re-post the data before using the application.\n'


@app.route('/data', methods = ['GET','DELETE','POST'])
def data_handler():
    
    if request.method == 'DELTE':
        rd.flushdb()
        global data_state 
        data_state = False
        return 'Data has been deleted.\n'

    elif request.method == 'GET':
        if data_state == False:
            return data_status()

        data_list = []
        for key in rd.keys():
            data_list.append(rd.hgetall(key))
        return data_list

    elif request.method == 'POST':
        url = "https://ftp.ebi.ac.uk/pub/databases/genenames/hgnc/json/hgnc_complete_set.json"
        r = requests.get(url)
        data = r.json()

        for item in data['gene_data']:
            key = f'{item["name"]}:{item["id"]}'
            rd.hset(key,mapping=item)

        data_state = True
        return 'Data has been posted to the Redis database.\n'
    
    else:
        return 'Invalid method has been provided. Please use either POST, DELETE, or GET. Refer to README for assistance.\n'

@app.route('/genes', methods = ['GET'])
def get_all_gene_ids() -> list:
    try:
        if data_state == False:
            return data_status()

        gene_keys = rd.keys()
        gene_data = []

        for gene_keys in gene_keys:
            hgnc_id = rd.hget(key, 'hgnc_id')
            if hgnc_id:
                gene_data.append(hgnc_id)
        return gene_data

@app.route('/genes/<string:hgnc_id>', methods = ['GET'])
def get_gene_id_data(hgnc_id):
    try:
        if data_state == False:
            return data_status()
        gene_data = {}
        gene_data = rd.hgetall(hgnc_id)

        if not gene_data:
            return f'{hgnc_id}: is not a valid gene id.\n'
        return gene_data

if __name__ == '__main__':
    app.run(debug = True, host = '0.0.0.0')
