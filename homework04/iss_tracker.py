from flask import Flask
import requests
import xmltodict

app = Flask(__name__)

def get_nasa_data() -> dict:
    url = 'https://nasa-public-data.s3.amazonaws.com/iss-coords/current/ISS_OEM/ISS.OEM_J2K_EPH.xml'
    r = requests.get(url)
    data = xmltodict.parse(r.content)
    
    # Path was found using .keys function 
    return data['ndm']['oem']['body']['segment']['data']['stateVector']

@app.route('/', methods = ['GET'])
def get_All_Data() -> dict:
    data = get_nasa_data()
    return data

@app.route('/epochs', methods = ['GET'])
def epochs_Only() -> list:
    epochs = []
    for data in get_nasa_data():
        epochs.append(data['EPOCH'])
    return epochs

@app.route('/epochs/<int:epoch>', methods = ['GET'])
def get_Epoch_Entry(epoch) -> dict:
    data = get_nasa_data()
    return data[int(epoch)]

@app.route('/epochs/<int:epoch>/position', methods = ['GET'])
def get_Epoch_Position(epoch) -> dict:
    epoch_Data = get_Epoch_Entry(epoch)
    return {'X': epoch_Data['X']['#text'], 'Y': epoch_Data['Y']['#text'], 'Z': epoch_Data['Z']['#text']}

@app.route('/epochs/<int:epoch>/speed', methods = ['GET'])
def get_Epoch_Speed(epoch) -> dict:
    coords = []
    epoch_Data = get_Epoch_Entry(epoch)
    coords.append(epoch_Data['X_DOT']['#text'])
    coords.append(epoch_Data['Y_DOT']['#text'])
    coords.append(epoch_Data['Z_DOT']['#text'])
   
    speed = sum(float(i)**2 for i in coords)
    return {'Speed' : speed}

if __name__ == '__main__':
    app.run(debug =True, host = '0.0.0.0')
