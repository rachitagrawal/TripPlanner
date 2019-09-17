import argparse
import pandas as pd
import numpy as np
import datetime as tm

def int_to_time(input_time):
    return tm.datetime(2019, 6, 6, int(input_time/100), input_time%100, 00)

def time_to_int(input_time):
    return input_time.hour * 100 + input_time.minute

def get_updated_time(start_time, delta_time):
    #print("start_time:", start_time, " delta:", delta_time)

    hour = int(start_time/100) + int(delta_time/60)
    mins = int(start_time%100) + int(delta_time%60)
    end_time = time_to_int(tm.datetime(2019, 6, 6, hour, mins, 00))

    return end_time

def find_best_itinerary(attractions, slot):
    #print("find best itinerary")

    itinerary = pd.DataFrame(columns=['Place', 'StartTime', 'EndTime'])

    #0. Get the current start time
    start_time = slot['StartTime']
    end_time = slot['EndTime']

    while attractions.shape[0] > 0:
        #1. Pick the attraction with earliest finish time
        attractions = filter_attractions(attractions, start_time, end_time)

        #2. Remove x, and all intervals intersecting x, from the set of candidate intervals
        row = attractions.iloc[0]
        new_start_time = get_updated_time(row['StartTime'],row['MinReqTime'])
        entry = {'Place':row['Place'], 'StartTime':row['StartTime'], 'EndTime':new_start_time}
        itinerary.loc[len(itinerary)] = entry
        attractions = attractions.drop(attractions.index[0])

        #3. Update the start time
        start_time = new_start_time

        #4. Repeat until the set of candidate interval is empty
        attractions = attractions.reset_index(drop=True)

    print("#################",slot['Date'],"##################")
    print(itinerary)
    print("#############################################")
    return itinerary

def filter_attractions(attractions, start_time, end_time):
    #print("Start Time = ", start_time, " End Time = ", end_time)
    #Create an empty data frame with column names
    filtered_df = pd.DataFrame(columns=attractions.columns)
    poss_ind = 0

    for index, place in attractions.iterrows():
        delta_time = int_to_time(min(place['EndTime'], end_time)) - int_to_time(max(place['StartTime'], start_time))

        if(delta_time.seconds/60 >= place['MinReqTime']):
            place['StartTime'] = max(place['StartTime'], start_time)
            place['EndTime'] = min(place['EndTime'], end_time)
            filtered_df.loc[poss_ind] = place
            poss_ind += 1

    #Sort the attractions by decreasing order of 'Rating' and increasing order of 'FinishTime'
    filtered_df.sort_values(by='Rating', ascending=False, inplace=True)
    filtered_df.sort_values(by='EndTime', ascending=True, inplace=True)

    return filtered_df

def get_possible_slots(attractions, free_slots):

    for index, row in free_slots.head().iterrows():
        #print(index, row['Date'], row['StartTime'], row['EndTime'])
        filtered_attractions = filter_attractions(attractions, row['StartTime'], row['EndTime'])
        itinerary = find_best_itinerary(filtered_attractions, row)

        cond = attractions['Place'].isin(itinerary['Place']) == True
        attractions.drop(attractions[cond].index, inplace=True)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Process the input')

    parser.add_argument('--dest', dest='destination')
    parser.add_argument('--avail', dest='availability')

    args = parser.parse_args()

    print(args.destination)
    print(args.availability)

    attractions = pd.read_csv(args.destination)
    free_slots = pd.read_csv(args.availability)

    get_possible_slots(attractions, free_slots)
