#!/usr/bin/env python3

import pytest
from analyze_water import calc_Turbidity, safe_Turbidity_Threshold, timer_For_Safe_Threshold,get_Water_Data

def test_calc_Turbidity():
    assert calc_Turbidity(2,-2) == 4
    assert calc_Turbidity(0.945,1.12) == 1.0584
    # prints if the assertions pass, meaning it works!
    print('The math is right!')
    
def test_safety_check():
    assert safe_Turbidity_Threshold(1.74,1.0) == False
    assert safe_Turbidity_Threshold(0,1) == True
    assert safe_Turbidity_Threshold(-1,1) == True
    
def test_timer_For_Safe_Threshold():
    turbidity_avg1 = 1.74
    turbidity_avg2 = 1.00
    turbidity_avg3 = 0.000
    turbidity_avg4 = 0.999
    turbidity_avg5 = -1
    safety_threshold = 1.00
    decay_factor = 0.02
    assert timer_For_Safe_Threshold(turbidity_avg1,safety_threshold,decay_factor) > 0.000
    assert timer_For_Safe_Threshold(turbidity_avg2,safety_threshold,decay_factor) == 0.000
    assert timer_For_Safe_Threshold(turbidity_avg3,safety_threshold,decay_factor) == 0.000
    assert timer_For_Safe_Threshold(turbidity_avg4,safety_threshold,decay_factor) == 0.000
    assert timer_For_Safe_Threshold(turbidity_avg5,safety_threshold,decay_factor) == 0.000

def test_get_water_data():
    assert type(get_Water_Data('https://raw.githubusercontent.com/wjallen/turbidity/main/turbidity_data.json')) == dict
    # prints if the assertions pass, meaning it works!
    print('It returns a dictionary!')
    
def main():
    test_calc_Turbidity()
    test_safety_check()
    test_timer_For_Safe_Threshold()
    test_get_water_data()
    
if __name__ == '__main__':
    main()