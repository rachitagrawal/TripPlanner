import argparse
import pandas as pd
import numpy as np

def find_best_itinerary(attractions, slot):
    print("find best itinerary")

    #0. Get the current start time
    start_time = 1700
    #1. Pick the attraction with earliest finish time
    #2. Remove x, and all intervals intersecting x, from the set of candidate intervals
    #3. Repeat until the set of candidate interval is empty
    #4. Update the start time

def get_possible_attractions(attractions, slot):
    print("Attractions possible in the slot:", slot)
    poss_df = pd.DataFrame(columns=attractions.columns)
    #print(poss_df)
    poss_ind = 0

    for index, row in attractions.iterrows():
        delta_time = (min(slot['EndTime'], row['EndTime']) - 
            max(slot['StartTime'], row['StartTime'])) / 100

        #print("==================================================")
        #print("Attraction:", row['Place'], " Delta:", delta_time)
        #print("==================================================")

        if(delta_time >= row['MinReqTime']):
            row['StartTime'] = max(slot['StartTime'], row['StartTime'])
            row['EndTime'] = min(slot['EndTime'], row['EndTime'])
            poss_df.loc[poss_ind] = row
            poss_ind += 1
            #print(row)

    #Sort the attractions by decreasing order of 'Rating' and increasing order of 'FinishTime'
    poss_df.sort_values(by='Rating', ascending=False, inplace=True)
    poss_df.sort_values(by='EndTime', ascending=True, inplace=True)
    print("############################################")
    print(poss_df)
    print("############################################")

    return poss_df

def get_possible_slots(attractions, free_slots):

    for index, row in free_slots.head().iterrows():
        #print(index, row['Date'], row['StartTime'], row['EndTime'])
        filtered_attractions = get_possible_attractions(attractions, row)
        find_best_itinerary(filtered_attractions, row)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Process the input')

    parser.add_argument('--dest', dest='destination')
    parser.add_argument('--avail', dest='availability')

    args = parser.parse_args()

    print(args.destination)
    print(args.availability)

    attractions = pd.read_csv(args.destination)
    free_slots = pd.read_csv(args.availability)

    print(attractions)
    print(free_slots)

    get_possible_slots(attractions, free_slots)
