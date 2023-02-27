# Homework 5: "Undone: The Sweater Container"

### Project Description:
This project was to develop a Flask-web based application that provides the user with current information about the International Space Station(ISS). This information
contains its position, and speed at different points and time. In addition, we were required to create a working docker container that can be used to ensure our application works in any enviroment by having the correct versions of modules & packages in use. 

#### Project Objective:
The purpose of this project was to become more familiar with Flask application development & the use of the DELETE method. In addition we also became more familiar with the creation of docker images, and pulling and pushing docker images.

### Data:
The data used was sourced from: https://nasa-public-data.s3.amazonaws.com/iss-coords/current/ISS_OEM/ISS.OEM_J2K_EPH.xml
Which was easily converted into a python dictionary with the use of the xmltodict module.

### Scripts:
`iss_tracker.py`: Flask application that is used to query for information about the ISS. Application loads in data from the URL referenced above in the data section. 
Depending on the route used different information is returned. 

### Flask Application & Routes:

| Route         | Return        | 
| ------------- |:-------------:| 
| `/`     | the full data set | 
| `/epochs`       | all epochs in the data set      |
| `/epochs/<epoch>`  | the data (state vectors) associated with the specified epoch      |
| `/epochs/<epoch>/position`  | the positional coordinates of the specified epoch     |
| `/epochs/<epoch>/speed`  | the speed of the specified epoch      |
| `/delete-data` | deletes the data & renders the other routes useless |
| `/post-data` | re-inserts the data from the URL above & allows the other routes to be used again |

Where `<epoch>` is any integer value. If a non-integer is used, you'll receive an error message.

### Usage & Installation:

To begin, first clone the repo & ensure that the xmltodict, flask and requests modules are installed as well.

To double check do this for each module:
```
pip3 install --user xmltodict

pip3 install --user requests

pip3 install --user flask
```
With the necessary modules installed, and the repo cloned the iss_tracker flask application can now be run.

This is accomplished by doing the following:
```
flask --app iss_tracker --debug run
```
This starts the flask application, and queries are now accessible using the API.

Now from a new terminal window that's within the same machine you're able to make queries via the command line. Using curl requests & the routes from above we can begin to get results like the following:

Route One: `/`
```
curl localhost:5000/
{
    "EPOCH": "2023-063T12:00:00.000Z",
    "X": {
      "#text": "2820.04422055639",
      "@units": "km"
    },
    "X_DOT": {
      "#text": "5.0375825820999403",
      "@units": "km/s"
    },
    "Y": {
      "#text": "-5957.89709645725",
      "@units": "km"
    },
    "Y_DOT": {
      "#text": "0.78494316057540003",
      "@units": "km/s"
    },
    "Z": {
      "#text": "1652.0698653803699",
      "@units": "km"
    },
    "Z_DOT": {
      "#text": "-5.7191913150960803",
      "@units": "km/s"
    }
  }
```
It should also be noted that on your other terminal you should be receiving messages like the following after each route call.
```
127.0.0.1 - - [21/Feb/2023 05:31:34] "GET / HTTP/1.1" 200 -
```
Now, for Route Two: `/epochs`
```
curl localhost:5000/epochs
[
  "2023-048T12:00:00.000Z",
  "2023-048T12:04:00.000Z",
  "2023-048T12:08:00.000Z",
  "2023-048T12:12:00.000Z",
  "2023-048T12:16:00.000Z",
  "2023-048T12:20:00.000Z",
  "2023-048T12:24:00.000Z",
  "2023-048T12:28:00.000Z",
  "2023-048T12:32:00.000Z",
  ...
]
```
Route Three: `/epochs/<epoch>`
```
curl localhost:5000/epoch/1
{
  "EPOCH": "2023-048T12:04:00.000Z",
  "X": {
    "#text": "-5998.4652356788401",
    "@units": "km"
  },
  "X_DOT": {
    "#text": "-2.8799691318087701",
    "@units": "km/s"
  },
  "Y": {
    "#text": "391.26194859011099",
    "@units": "km"
  },
  "Y_DOT": {
    "#text": "-5.2020406581448801",
    "@units": "km/s"
  },
  "Z": {
    "#text": "-3164.26047476555",
    "@units": "km"
  },
  "Z_DOT": {
    "#text": "4.8323394499086101",
    "@units": "km/s"
  }
}
```
For the previous route & the routes that follow, if anything but an integer is used for <epoch> you will receive the following message:
```
Bad input. Please input an integer value between 1 and 5882.
```
Route Four: `/epochs/<epoch>/position`
```
curl localhost:5000/epoch/1/position
{
  "X": "-5998.4652356788401",
  "Y": "391.26194859011099",
  "Z": "-3164.26047476555"
}
```
Route Five: `/epochs/<epoch>/speed`
```
curl localhost:5000/epoch/1/speed
{
  "Speed": 7.662046317290625
}
```

### Credits:

For assistance on formatting, I took inspiration from Jacksons' README.md found at the following URL https://github.com/jthet/my-coe332-hws/blob/main/homework04/README.md
