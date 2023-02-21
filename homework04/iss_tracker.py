from flask import Flask
import requests
import xmltodict
import math

app = Flask(__name__)

def get_nasa_data() -> dict:
    """
    Function grabs the XML data from the Nasa data-base, and converts it into a usable python dictionary.

    Args:
        None.

    Returns:
        data (dict) : a dictionary of the information within the stateVectors key that was pulled from the XML file. 
                      This route was found using the .keys function, with the XML data.
    """
    url = 'https://nasa-public-data.s3.amazonaws.com/iss-coords/current/ISS_OEM/ISS.OEM_J2K_EPH.xml'
    r = requests.get(url)
    data = xmltodict.parse(r.content)

    return data['ndm']['oem']['body']['segment']['data']['stateVector']

@app.route('/', methods = ['GET'])
def get_All_Data() -> dict:
    """
    This function takes the python dictionary from get_Nasa_Data & returns it.
    
    Args:
        None

    Returns:
        data (dict): python dictionary of all Epochs & the associated data.
    """
    data = get_nasa_data()
    return data

@app.route('/epochs', methods = ['GET'])
def epochs_Only() -> list:
    """
    Function takes the python dictonary created with get_Nasa_Data & creates a list of all current Epochs.

    Args:
        None.

    Returns:
        epochs (list) : A list that holds all the epochs.
    """
    epochs = []
    for data in get_nasa_data():
        epochs.append(data['EPOCH'])
    return epochs

@app.route('/epochs/<int:epoch>', methods = ['GET'])
def get_Epoch_Entry(epoch) -> dict:
    """
    Function takes in a specific epoch, from the list created in epochs_Only. This epoch is specified
    by an integer value.

    Args:
        epoch (int): an integer value that identifies the specific epoch from the epochs list
                     that we want the data from.

    Returns:
        data (dict): returns a dictionary that holds the data from the specific epoch identified earlier.
    """
    data = get_nasa_data()
    return data[int(epoch)]

@app.route('/epochs/<int:epoch>/position', methods = ['GET'])
def get_Epoch_Position(epoch) -> dict:
    """
    Function takes in a specific epoch, from the list created in epochs_Only. This epoch is specified
    by an integer value. It then returns the X, Y, & Z position coordinates contained within that epoch.

    Args:
        epoch (int): an integer value that identifies the specific epoch from the epochs list
                     that we want the data from.

    Returns:
        dictionary: returns a dictionary containing the X Y Z coordinates & a key that is associated with 
                    the specific coordinate plane.
    """
    epoch_Data = get_Epoch_Entry(epoch)
    return {'X': epoch_Data['X']['#text'], 'Y': epoch_Data['Y']['#text'], 'Z': epoch_Data['Z']['#text']}

@app.route('/epochs/<int:epoch>/speed', methods = ['GET'])
def get_Epoch_Speed(epoch) -> dict:
    """
    Function takes in a specific epoch, from the list created in epochs_Only. This epoch is specified by
    an integer value. It then returns a dictionary holding the final speed value of the epoch.

    Args:
        epoch (int): an integer value that identifies the specific epoch from the epochs list
                     that we want the data from.

    Returns:
        Speed (dict): The speed of the ISS within the specified epoch. 
    """
    epoch_Data = get_Epoch_Entry(epoch)
    x_Speed = float(epoch_Data['X_DOT']['#text'])
    y_Speed = float(epoch_Data['Y_DOT']['#text'])
    z_Speed = float(epoch_Data['Z_DOT']['#text'])
   
    speed = math.sqrt(x_Speed**2 + y_Speed**2 + z_Speed**2)
    return {'Speed' : speed}

if __name__ == '__main__':
    app.run(debug =True, host = '0.0.0.0')
