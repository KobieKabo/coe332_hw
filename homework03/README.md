# Homework 3: "The World Has Turned and Left Me Turbid" 

### Project Description:
This project uses different water samples and analyzes their quality, with an emphasis on the turbidity levels in order to determine the safety level of the water. The analyze_water.py file contained within this directory pulls data down from https://raw.githubusercontent.com/wjallen/turbidity/main/turbidity_data.json, where it then takes the five most recent data samples taken and determines if the water is below a safety threshold, and if it isn't it returns how long it will take until the water is safe once again. The test_analyze_water.py is a unit tester script that ensures everything is working correctly within the analyze_water.py file, with tests that check math, and ensuring the proper data types are being returned by the given functions.

#### Project Purpose:
The purpose of this project is to become familiar with working with API's via the python requests module, and unit testing. Additonally, to become more familiar with
using docstrings when writing functions, and having properly documented code.

### Data:
Data used was again sourced from this url: https://raw.githubusercontent.com/wjallen/turbidity/main/turbidity_data.json, with a sample looking like:
        ```
{
  "turbidity_data": [
    {
      "datetime": "2023-02-01 00:00",
      "sample_volume": 1.19,
      "calibration_constant": 1.022,
      "detector_current": 1.137,
      "analyzed_by": "C. Milligan"
    },
    {
      "datetime": "2023-02-01 01:00",
      "sample_volume": 1.15,
      "calibration_constant": 0.975,
      "detector_current": 1.141,
      "analyzed_by": "C. Milligan"
    },
    ... etc
### Scripts:

    'analyze_water.py':
        Pulls data down from the url listed above twice, and creates a dictionary from the given data. This dictionary is then used
        to perform multiple functions, such as compute the average turbidity of the five most recent data samples taken. This average is then compared to a constant safety threshold, where if the threshold is exceeded a time value is computed to determine how long
        until the water would be safe once more.

    'test_analyze_water.py':
        Applies simple unit tests, to each function within analyze_water.py to ensure everything is working as intended.

### Installation:

    Ensure both the pytest, and requests module are installed, this is done by using the following commands while on the command line within a unix shell.

    pip3 install --user requests
    &
    pip3 install --user pytest

    These will both allow the unit test script, and data collecting script to work as intended.

### Running the code & Testing:

    After cloning the repository, move into the homework03 directory. From there on the command line all you need to do is type the following:

    ``` 
    $ pytest test_analyze_water.py
    ```

    This should have an output of:
    ```
    ============================= test session starts ================================
                    platform linux -- Python 3.8.10, pytest-7.2.1, pluggy-1.0.0
                    rootdir: /home/kebabo/coe332_hw/homework03
                    collected 4 items                                                                                                                                         

                    test_analyze_waterpy ....                                                                                                                                                                                               [100%]
================================== 4 passed in 0.12s =================================
    ```

    Then after ensuring the analyze_water.py function is working you simply do:
    ```
    $ python3 analyze_water.py
    ```
    yielding an output such as:
    ```
    Average turbidity based on most recent five measurements = 1.15388 NTU.
    The current turbidity exceeds the safety threshold.
    Minimum time required to return below a safe threshold 7.085 hours.
    ```
