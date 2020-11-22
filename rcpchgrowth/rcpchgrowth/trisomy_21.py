import json
import pkg_resources
from .constants import *
# from .global_functions import z_score, cubic_interpolation, linear_interpolation, centile, measurement_for_z, nearest_lowest_index, fetch_lms
# import timeit #see below, comment back in if timing functions in this module

"""
birth_date: date of birth
observation_date: date of observation
sex: sex (string, MALE or FEMALE)
decimal_age: chronological, decimal
corrected_age: corrected for prematurity, decimal
measurement_method: height, weight, bmi, ofc (decimal)
observation: value (float)
gestation_weeks: gestational age(weeks), integer
gestation_days: supplementary days of gestation
lms: L, M or S
reference: reference data
"""

#load the reference data

T21_DATA = pkg_resources.resource_filename(__name__, "/data_tables/trisomy_21.json")
with open(T21_DATA) as json_file:
            T21_DATA = json.load(json_file)
            json_file.close()

def reference_data_absent( 
        age: float,
        measurement_method: str,
        sex: str
    ) -> (bool, str):
    """
    Helper function.
    Returns boolean
    Tests presence of valid reference data for a given measurement request

    Reference data is not complete for all ages/sexes/measurements.
     - There is only BMI reference data until 18.92y
     - Head circumference reference data is available until 18.0y
     - lowest threshold is 0 weeks, upper threshold is 20y
    """

    if age < 0: # lower threshold of T21 data
        return True, "Trisomy 21 reference data does not include prematurity."
    
    if age > TWENTY_YEARS: # upper threshold of T21 data
        return True
        
    elif measurement_method == "bmi" and age > 18.82:
        return True, "Trisomy BMI reference data does not exist > 18.82 y"
    
    elif measurement_method == "ofc":
        if age > EIGHTEEN_YEARS:
            return True, "Trisomy head circumference reference data does not exist > 18 y"
        else:
            return False, ""
    else:
        return False, ""

def trisomy_21_lms_array_for_measurement_and_sex(
        measurement_method: str,
        sex: str,
        age: float
    ):

    data_invalid, data_error = reference_data_absent(age=age, measurement_method=measurement_method, sex=sex)

    if data_invalid:
        raise LookupError(data_error)
    else:
        return T21_DATA["measurement"][measurement_method][sex]