#!/usr/bin/env python3

import requests
import math

def calc_Turbidity(a0:float, I90: float) -> float:
    """
    Calculates the turbidity of the water.
    
    Args:
        a0 (float) = Calibatrion constant associated with the measured data when checking the quality of the water
        I90 (float) = Ninety degree detector constant associated with the measured data when checking the quality of the water
        
    Returns:
        Turbidity (float) = the turbidity of the water in units of NTU
    """
    turbidity = a0*abs(I90)
    
    return (turbidity)

def safe_Turbidity_Threshold(current_Turbidity: float, safety_threshold: float) -> bool:
    """
    Checks if the current turbidity value of the water is at a safe level or not, by checking it against
    a safety threshold value.
    
    Args:
        current_Turbidity (float) = the waters current turbidity level
        safety_threshold (float) = safety threshold the turbidity cannot exceed for safe use
        
    Returns:
        True or False, depended on the current turbidity exceeding the safety threshold or not
    """
    if current_Turbidity > safety_threshold:
        print('The current turbidity exceeds the safety threshold.')
        return False
    else:
        print ('The water is safe for use.')
        
    return True

def timer_For_Safe_Threshold(current_Turbidity: float, safety_threshold: float, decay_Factor: float) -> float:
    """
    Computes the necessary time required for the turbidity of the water to return to safe levels
    if it exceeds a safety threshold. This is based on the following relationship Ts > T0(1 - d)^b.
    
    Args:
        current_Turbidity (float) = the waters current turbidity level
        safety_threshold (float) = safety threshold the turbidity cannot exceed for safe use
        decay_factor (float) = factor associdated with how water turbidity decreases over time
    
    Returns:
        hours_need (float) = time required for the water to reach safe levels
    """
    if current_Turbidity <= safety_threshold:
        hours_needed = 0
    else:
        hours_needed = abs(math.log(safety_threshold / current_Turbidity, 1 - decay_Factor))
   
    print(f'Minimum time required to return below a safe threshold {hours_needed:.3f} hours.')
    return hours_needed

def get_Water_Data(website:str) -> dict:
    """
    This function takes in a string element, that should lead to the website that holds the water quality data in a JSON format.
    
    Args:
        website (str) = URL that leads to the water quality website that holds the data necessary for the other functions.
    
    Returns:
        turbidity_Data (dict) = Dictionary holding all of the water quality data in a JSON format.
    """
    response = requests.get(url = website)
    turbidity_Data = response.json()

    return turbidity_Data

def main():
    
    # pulling data from the necessary URL & initializing required variables 
    turbidity_Data = get_Water_Data('https://raw.githubusercontent.com/wjallen/turbidity/main/turbidity_data.json')
    decay_Factor = 0.02
    safety_threshold = 1.0
    counter = 0
    turbidity_sum = 0
    samples = 5
    
    for sample in turbidity_Data['turbidity_data']:
        current_Calibration = sample['calibration_constant']
        current_Detector = sample['detector_current']
        turbidity = calc_Turbidity(current_Calibration,current_Detector)
        turbidity_sum = turbidity + turbidity_sum
        counter += 1
        if counter == samples:
            break
    turbidity_average = turbidity_sum / samples
    print(f'Average turbidity based on most recent five measurements = {turbidity_average:.6} NTU.')
    
    safe_Turbidity_Threshold(turbidity_average,safety_threshold)
    timer_For_Safe_Threshold(turbidity_average,safety_threshold,decay_Factor)
    

if __name__ == '__main__':
    main()