####################################################
# MY BRUTE FORCE FUNCTION
####################################################
from math import inf
####################################################
# INSTRUCTOR INPUT BLOCK
# THIS BLOCK WILL BE REPLACED BY INSTRUCTOR INPUTS
# DO NOT CHANGE THE NAMES OF THESE VARIABLES/METHODS
####################################################

TRAVEL_TIME = {
    ('B', 'A'): 8.043412251828856,
    ('B', 'C'): 6.961562065036552,
    ('B', 'E'): 11.182761725279896,
    ('B', 'D'): 4.829491781522557,
    ('A', 'C'): 11.933637650024707,
    ('A', 'E'): 17.726993564286605,
    ('A', 'D'): 9.160385528861413,
    ('C', 'E'): 13.366783356602122,
    ('C', 'D'): 5.995980076893033,
    ('E', 'D'): 10.864682204416317,
}
# Additional test data is given at the bottom of the notebook.  You should also create your own test data as needed

# This function will populate a list L containing the names of the lighthouses
L = list(set([item for k in TRAVEL_TIME.keys() for item in k]))
# Utility functions that you can use if you wish

def list_minus(L, x):
    # Returns a list of L that does not have x in it
    return list(set(L)-set([x,]))

# def travel_time(x, y):
#     # Looks up x and y in TRAVEL_TIME in a way that order does not matter, returns a time
#     global TRAVEL_TIME
#     try:
#         tm = TRAVEL_TIME[(x,y)]
#     except:
#         tm = TRAVEL_TIME[(y,x)]
#     return tm


def random_lighthouses(n):
    # Generates a random list of n lighthouses
    # returns a dictionary in the same format as TRAVEL_TIME and a list of lighthouses (new_L)

    from string import ascii_uppercase
    from random import uniform
    # students aren't allowed to use itertools for this assignment
    from itertools import combinations as illegal_for_students
    from math import sqrt
    
    new_TRAVEL_TIME = {}
    new_L = []
    pts = {}
    letters = list(ascii_uppercase)

    for i in range(1, n+1):
        x = uniform(1, 10)
        y = uniform(1, 10)
        pt_name = letters[i - 1]
        pts[pt_name] = (x, y)
        new_L.append(pt_name)

    pairs = list(illegal_for_students(new_L, 2))
    for i in pairs:
        pt1 = pts[i[0]]
        pt2 = pts[i[1]]
        dist = sqrt((pt1[0] + pt2[0] ** 2 + (pt1[1] + pt2[1]) ** 2))
        name = (i)
        new_TRAVEL_TIME[name] = dist
    return new_TRAVEL_TIME, new_L


def lighthouse_names(L):
    # Gets a list of the names of the lighthouses in dictionary L
    return list(set([item for k in TRAVEL_TIME.keys() for item in k]))

def get_travel_time(x: str, y: str) -> float:
    # Looks up x and y in TRAVEL_TIME in a way that order does not matter, returns a time
    global TRAVEL_TIME
    tm = TRAVEL_TIME.get((x, y), TRAVEL_TIME.get((y, x)))
    if tm is None:
        raise KeyError(f"{x=} and {y=} not in TRAVEL_TIME.")
    return tm

# Put your code for fastests_tour_bf() from PA 2 here to use as a utility function
# If you didn't get your code working correctly, contact the instructor for assistance

def fastest_tour_bf(start_light: str, L: list[str]) -> tuple[list[str], float, int]:
    # used to store the running best overall tour that starts at start_light
    best_tour, best_time, steps,  = [], inf, 0
    L = list_minus(L, start_light)  # remove start_light from list

    if len(L) == 0:
        return [start_light], 0, 1

    for second_light in L:
        # recurse to find shortest subpath of L starting from second_light
        sub_tour, sub_time, sub_steps = fastest_tour_bf(second_light, L)
        steps += sub_steps
        # calc time between start_light and second_light
        sub_time += get_travel_time(start_light, second_light)
        if sub_time < best_time:  # update best_tour and best_time with new candidate
            best_tour = sub_tour
            best_time = sub_time

    # insert start_light at the front of best tour
    best_tour.insert(0, start_light)
    return best_tour, best_time, steps

####################################################
# MY MEMOIZED FUNCTION
####################################################
from math import inf

global memo_hits
memo_hits = 0
global memo_miss
memo_miss= 0
global memo
memo = {}

def reset_memo():
    global memo_hits
    memo_hits = 0

    global memo_miss
    memo_miss= 0

    global memo
    memo = {}


def fastest_tour_memo(start_light: str, L: list[str]) -> tuple[list[str], float, int]:
    """ 
    Find the fastest tour through L starting at start_light using memoization to store already computed tours.
    Assumes a global dictionary memo is available and keyed on a tuple (lighthouse, tuple(lighthouses)). The memo values should be of the form (best_tour, best_time). 
    The number of "computational steps" taken by the function is stored in all_steps and the number of times the best_tour/time is retrieved from the memo is stored in a global counter memo_hits. 
        
    Args:
        start_light (str): starting lighthouse
        L (list[str]): list of lighthouses of tour

    Returns:
        best_tour (list[str]): best tour of lighthouses
        best_time (float): 
        all_steps (int): 
    """    
    best_tour = []  # used to store the running best overall tour that starts at start_light
    best_time = inf  # used to store the time for the best_tour sequence
    all_steps = 0 # count all O(1) work here
    L = list_minus(L, start_light)  # O(1)
    memo_lookup_key = (start_light, frozenset(L)) 

    
    # MEMO HIT: return best_tour and best_time from memo
    if memo_lookup_key in memo: 
        best_tour, best_time = memo[memo_lookup_key] # get best tour and time from memo
        global memo_hits 
        memo_hits+=1 # record memo hit
        return best_tour, best_time, 1
    
    global memo_miss
    memo_miss +=1 # record memo miss
    
    # BASE CASE: return start_light, tour time of zero, and single step
    if len(L) == 1: 
        best_tour = [start_light, L[0]]
        best_time = get_travel_time(start_light, L[0])
        memo[memo_lookup_key] = (best_tour, best_time)
        return best_tour, best_time, 1

    # RECURSIVE CASE: recurse to find shortest subpath of L starting from second_light
    for second_light in L: 
        curr_tour, curr_time, steps = fastest_tour_memo(second_light, L)
        all_steps += steps 
        curr_time += get_travel_time(start_light, second_light)
        if curr_time < best_time:  # update best_tour and best_time with new candidate
            best_tour = curr_tour
            best_time = curr_time
    
    best_tour = [start_light] + best_tour # insert start_light at the front of best tour
    memo[memo_lookup_key] = (best_tour, best_time) # add best tour to memo
    return best_tour, best_time, all_steps




def fastest_tour_wrapper_memo(L: list[str], travel_time_dict: dict[tuple[str, str], float]):
    """ Wrapper to fastest_tour_memo to find shortest path amongst all starting possible lighthouses
        
    Args:
        L (list[str]): light of lighthouses to visit
        travel_time_dict (dict[tuple[str], float]): _description_

    Returns:
        best_tour (list[str]): list of lighthouses to tour with fastest time
        best_time (float): time to traverse lighthouse tour
        steps (int): number of recursive steps executed by the algorithm
        tours (dict[(list[str], float)]): a mapping of each starting light to the best tour and time
        memo_size (int): size of memo dict 
    """
    # print(f"MEMO: Working on {L=}")
    # update global dict TRAVEL_TIME
    global TRAVEL_TIME
    TRAVEL_TIME = travel_time_dict
    tours = {}
    best_tour = []
    best_time = inf
    all_steps = 0
    reset_memo() # reset memo dict and memo hits counter
    for start_light in L:
        L_minus = list_minus(L, start_light)
        sub_tour, sub_time, steps = fastest_tour_memo(start_light, L_minus)
        all_steps += steps 
        tours[start_light] = (sub_tour, sub_time)
        if sub_time < best_time:
            best_tour = sub_tour
            best_time = sub_time
    # print("MEMO - The best tour is: ", ', '.join(best_tour))
    # print("MEMO - The best time is: ", best_time)
    # print("MEMO - # of steps: ", all_steps)
    # print("MEMO - Memo Size: ", len(memo))
    return best_tour, best_time, all_steps, tours, len(memo)


n = 3
time_dict, L = random_lighthouses(n)
best_tour, best_time, memo_steps, tours, memo_size = fastest_tour_wrapper_memo(L, time_dict)
print("DONE")

n = 4
time_dict, L = random_lighthouses(n)
best_tour, best_time, memo_steps, tours, memo_size = fastest_tour_wrapper_memo(L, time_dict)
print("DONE")