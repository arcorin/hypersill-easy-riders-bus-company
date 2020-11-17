# https://hyperskill.org/projects/128?track=2
# Project: Easy Riders Bus Company
# Stage 1/6: Checking the data type
# Stage 2/6:
# Stage 3/6:
# Stage 4/6:
# Stage 5/6:
# Stage 6/6:

import json
from datetime import datetime
import re
from collections import Counter


# create a dictionary with lists of errors for each key in the input dictionaries
# the first element of each list is the sum of errors in that list
errors = {"bus_id": [0],
          "stop_id": [0],
          "stop_name": [0],
          "next_stop": [0],
          "stop_type": [0],
          "a_time": [0]
          }

# create a dictionary with lists of values for each key in the input dictionaries
all_values = {
    "bus_id": [],
    "stop_id": [],
    "stop_name": [],
    "next_stop": [],
    "stop_type": [],
    "a_time": []
    }

stop_type_list = ["S", "O", "F", ""]
start_stops = []
transfer_stops = []
final_stops = []

# create a dictionary with lists of arrival times for each bus line
buses = {}

# create a dictionary with lists of correct arrival times for each bus line
buses_correct = {}

# create a dictionary with lists of incorrect arrival times for each bus line
buses_incorrect = {}

# stage 4
# create a dictionary with lists of stop types and stop names for each bus line
buses_stops = {}

# regex for checking if the stop names, stop type and arrival times are correct
stop_name_regex = r"([A-Z][a-z]+\s)+(Street|Boulevard|Road|Avenue)$"
stop_type_regex = r"^[FOS]?$"
a_time_regex = r"^[012]?[0-9]:[012345][0-9]$"


def check_data_types(d):
    """ check if values in a dictionary are the right data types and comply with requirements"""

    # append to the dictionary containing all values, the values of the current input dictionary
    for k, v in d.items():
        all_values[k].append(v)
    '''
    print()
    for k, v in d.items():
        print(f"{k}: {v}")
    '''

    # check for every item in the dictionary if data types of the values match and ...
    # ... if data types doesn't match, the values in errors dictionary are increased
    if type(d["bus_id"]) != int:
        errors["bus_id"][0] += 1
        errors["bus_id"].append(d["bus_id"])

    if type(d["stop_id"]) != int:
        errors["stop_id"][0] += 1
        errors["stop_id"].append(d["stop_id"])

    # add stop name and stop type to the list of each bus_id
    if str(d["bus_id"]) not in buses_stops.keys():
        buses_stops[str(d["bus_id"])] = {"stop_names": [], "stop_types": []}
    buses_stops[str(d["bus_id"])]["stop_names"].append(d["stop_name"])
    buses_stops[str(d["bus_id"])]["stop_types"].append(d["stop_type"])

    # check stop_name
    if type(d["stop_name"]) != str or \
            not bool(re.match(stop_name_regex, d["stop_name"])):
        errors["stop_name"][0] += 1
        errors["stop_name"].append(d["stop_name"])

    # check stop type data type
    if type(d["stop_type"]) != str or not bool(re.match(stop_type_regex, d["stop_type"])):
        errors["stop_type"][0] += 1
        errors["stop_type"].append(d["stop_type"])

    # if stop type is "S" or "F", append stop name to the respective list
    if d["stop_type"] == "S":
        if d["stop_name"] not in start_stops:
            start_stops.append(d["stop_name"])
    if d["stop_type"] == "F":
        if d["stop_name"] not in final_stops:
            final_stops.append(d["stop_name"])

    # check next stop data type
    if type(d["next_stop"]) != int:
        errors["next_stop"][0] += 1
        errors["next_stop"].append(d["next_stop"])

    # add arrival time to the list of arrival times of each bus_id
    if str(d["bus_id"]) not in buses.keys():
        buses[str(d["bus_id"])] = []
    buses[str(d["bus_id"])].append(d["a_time"])

    # check arrival time data type
    if type(d["a_time"]) == str and bool(re.match(a_time_regex, d["a_time"])):
        if str(d["bus_id"]) not in buses_correct.keys():
            buses_correct[str(d["bus_id"])] = []
        # add correct data type arrival times and stop name to the buses_correct dictionary
        buses_correct[str(d["bus_id"])].append((d["a_time"], d["stop_name"]))

    if type(d["a_time"]) != str or not bool(re.match(a_time_regex, d["a_time"])):
        # print(f'{d["a_time"]} does not match the expression\n')
        errors["a_time"][0] += 1
        errors["a_time"].append(d["a_time"])


def check_stop_names_and_types():
    ''' check if each bus line has exactly one starting point and one final stop
        if all bus lines meet the condition, count the number of start, transfer and
         final points and print their unique names '''

    correct = True

    # iterate over buses_stops dictionary
    # check if each bus line has exactly one starting point and one final stop
    for k, v in buses_stops.items():
        # if there is a bus line with more than one start or final stop - break counting ...
        # ... and print a message about it
        if v["stop_types"].count("S") != 1 or v["stop_types"].count("F") != 1:
            correct = False
            print(f"There is no start or end stop for the line: {k}.")
            break

    if correct:
        # find transfer stops - common stops for two or more bus lines
        freq_stops_dict = Counter(all_values["stop_name"])
        for key, value in freq_stops_dict.items():
            if value > 1:
                transfer_stops.append(key)

        # print(freq_stops_dict)

        # sort the lists of start, transfer and final stops
        start_stops.sort()
        transfer_stops.sort()
        final_stops.sort()

        '''
        # stage 4
        # print the number of start stops and their unique names
        print(f"Start stops: {len(start_stops)} {start_stops}")

        # print the number of transfer stops and their unique names
        print(f"Transfer stops: {len(transfer_stops)} {transfer_stops}")

        # print the number of final stops and their unique names
        print(f"Finish stops: {len(final_stops)} {final_stops}")
        '''


def check_arrival_times():

    ''' check if the values of arrival times are increasing
        by iterating over each stop time in each bus line =
        = check if every correct arrival time is greater than
        previous correct arrival time
    '''

    for k, v in buses_correct.items():
        # add bus line id keys from buses_correct arrival times dictionary ...
        # ... to the keys of buses_incorrect arrival times dictionary
        if k not in buses_incorrect.keys():
            buses_incorrect[k] = []

        # if there are 0 or 1 correct arrival times values ...
        # ... => correct values are not increasing => error
        if len(v) < 2:
            errors["a_time"][0] += 1
        # if there are at least 2 correct arrival times values ...
        # ... check if each 2 consecutive values are increasing
        else:
            for i in range(1, len(v)):
                if datetime.strptime(v[i][0], "%H:%M") < datetime.strptime(v[i - 1][0], "%H:%M"):
                    errors["a_time"][0] += 1
                    buses_incorrect[k].append(v[i][1])


def main():
    """ The input string is converted to json and each dictionary (the data of the dictionary values)...
        ... is checked with the function check_dictionary() """

    # take the input string and convert it to json
    file = input()
    json_file = json.loads(file)

    # each dictionary in json is checked with check_dictionary
    for j in json_file:
        check_data_types(j)

    check_arrival_times()

    '''
    # print for checking - not required in the project
    # print the list of errors and the list of all values for each key in the input dictionaries
    for key, value in errors.items():
        print(errors[key], all_values[key])
    print(buses)
    '''

    '''
    # stage 1 and 2
    # print the errors dictionary with the result of the data types check
    total_err = sum([value[0] for value in errors.values()])
    print(f"\nFormat validation: {total_err} errors")
    
    # stage 1 and 2
    # print the number of errors for each key (in stage 1) or required key (in stage 2) in the dictionary
    for key, value in errors.items():
        if key in ["stop_name", "stop_type", "a_time"]:
            print(f"{key}: {value[0]}")
    '''

    '''
    # stage 3
    # for each bus line in the input dictionary ...
    # ... print the bu line name (bus_id) and the numbers of stops
    print("\nLines names and number of stops")
    for k, v in buses.items():
        print(f"bus_id: {k}, stops: {len(v)}")
    '''

    '''
    # stage 4
    # print(buses_stops)
    # check_stop_names_and_types()
    '''

    '''
    # stage 5
    incorrect_arrival = 0
    print("Arrival time test:")
    for k, v in buses_incorrect.items():
        if len(v) > 0:
            incorrect_arrival += 1
            print(f"bus_id line {k}: wrong time on station {v[0]}")
    if incorrect_arrival == 0:
        print("OK")

    # print(f"buses {buses}")
    # print(f"buses_correct {buses_correct}")
    # print(f"buses_incorrect {buses_incorrect}")
    # print("incorrect arrival =", incorrect_arrival)
    '''

    # stage 6
    check_stop_names_and_types()
    print("On demand stops test:")
    # create a list of start, transfer and final stops ...
    # .. that have an incorrect on-demand tag "O"
    incorrect_stop_types = []

    # print("transfer stops", transfer_stops)
    # print("buses_stops")

    for k, v in buses_stops.items():
        # print(k, ":", v)
        # check for each bus line if the start or final point have the incorrect tag "O"
        # ... and append the stop name to the incorrect_stop_types_list
        if v["stop_types"][0] == "O":
            incorrect_stop_types.append(v["stop_names"][0])
        if v["stop_types"][-1] == "O":
            incorrect_stop_types.append(v["stop_names"][-1])

        # check for each bus line if has a transfer stop with the incorrect tag "O"
        # ... and append the stop name to the incorrect_stop_types_list
        for idx in range(1, len(v["stop_names"]) - 1):
            if v["stop_types"][idx] == "O" \
                    and v["stop_names"][idx] in transfer_stops \
                    and v["stop_names"][idx] not in incorrect_stop_types:
                incorrect_stop_types.append(v["stop_names"][idx])

    if len(incorrect_stop_types) > 0:
        incorrect_stop_types.sort()
        print(f"Wrong stop type: {incorrect_stop_types}")
    else:
        print("OK")


test_stage4_3 = '[{"bus_id" : 128, "stop_id" : 1, "stop_name" : "Prospekt Avenue", "next_stop" : 3, "stop_type" : "S", "a_time" : "08:12"}, {"bus_id" : 128, "stop_id" : 3, "stop_name" : "Elm Street", "next_stop" : 5, "stop_type" : "", "a_time" : "08:19"}, {"bus_id" : 128, "stop_id" : 5, "stop_name" : "Fifth Avenue", "next_stop" : 7, "stop_type" : "O", "a_time" : "08:25"},{"bus_id" : 128, "stop_id" : 7, "stop_name" : "Sesame Street", "next_stop" : 0, "stop_type" : "F", "a_time" : "08:37"}, {"bus_id" : 256, "stop_id" : 2, "stop_name" : "Pilotow Street", "next_stop" : 3, "stop_type" : "S", "a_time" : "09:20"}, {"bus_id" : 256, "stop_id" : 3, "stop_name" : "Elm Street", "next_stop" : 6, "stop_type" : "", "a_time" : "09:45"}, {"bus_id" : 256, "stop_id" : 6, "stop_name" : "Sunset Boulevard", "next_stop" : 7, "stop_type" : "", "a_time" : "09:59"}, {"bus_id" : 256, "stop_id" : 7, "stop_name" : "Sesame Street", "next_stop" : 0, "stop_type" : "F", "a_time" : "10:12"}, {"bus_id" : 512, "stop_id" : 4, "stop_name" : "Bourbon Street", "next_stop" : 6, "stop_type" : "S", "a_time" : "08:13"}, {"bus_id" : 512, "stop_id" : 6, "stop_name" : "Sunset Boulevard", "next_stop" : 0, "stop_type" : "F", "a_time" : "08:16"}]'
test_stage6_2 = '[{"bus_id" : 128, "stop_id" : 1, "stop_name" : "Prospekt Avenue", "next_stop" : 3, "stop_type" : "S", "a_time" : "08:12"}, {"bus_id" : 128, "stop_id" : 3, "stop_name" : "Elm Street", "next_stop" : 5, "stop_type" : "O", "a_time" : "08:19"}, {"bus_id" : 128, "stop_id" : 5, "stop_name" : "Fifth Avenue", "next_stop" : 7, "stop_type" : "O", "a_time" : "08:25"}, {"bus_id" : 128, "stop_id" : 7, "stop_name" : "Sesame Street", "next_stop" : 0, "stop_type" : "F", "a_time" : "08:37"}, {"bus_id" : 256, "stop_id" : 2, "stop_name" : "Pilotow Street", "next_stop" : 3, "stop_type" : "S", "a_time" : "09:20"}, {"bus_id" : 256, "stop_id" : 3, "stop_name" : "Elm Street", "next_stop" : 6, "stop_type" : "", "a_time" : "09:45"}, {"bus_id" : 256, "stop_id" : 6, "stop_name" : "Abbey Road", "next_stop" : 7, "stop_type" : "O", "a_time" : "09:59"}, {"bus_id" : 256, "stop_id" : 7, "stop_name" : "Sesame Street", "next_stop" : 0, "stop_type" : "F", "a_time" : "10:12"}, {"bus_id" : 512, "stop_id" : 4, "stop_name" : "Bourbon Street", "next_stop" : 6, "stop_type" : "S", "a_time" : "08:13"}, {"bus_id" : 512, "stop_id" : 6, "stop_name" : "Abbey Road", "next_stop" : 0, "stop_type" : "F", "a_time" : "08:16"}]'

if __name__ == '__main__':
    main()
