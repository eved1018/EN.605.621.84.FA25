from math import inf
from pprint import pprint

def list_minus(L, x):
    # Returns a list of L that does not have x in it
    return list(set(L) - set([x,]))


def get_travel_time(x, y, TRAVEL_TIME):
    # Looks up x and y in TRAVEL_TIME in a way that order does not matter, returns a time
    tm = TRAVEL_TIME.get((x, y), TRAVEL_TIME.get((y, x)))
    if tm is None:
        raise ValueError(f"{x, y} not in TRAVEL_TIME. {TRAVEL_TIME=}")
    return tm


def fastest_tour_wrapper(L, TRAVEL_TIME):
    best_tour = []
    best_time = inf
    best_steps = 0
    best_start = None
    for start_light in L:
    # for start_light in ["A"]:
    # for start_light in ["Choptank River"]:
        L_minus = list_minus(L, start_light)
        curr_tour, curr_time, steps, _ = fastest_tour_memo(start_light, L_minus, TRAVEL_TIME)
        # break
        # curr_tour, curr_time, steps = fastest_tour_bf(start_light, L_minus, TRAVEL_TIME)
        if curr_time < best_time:
            best_tour = curr_tour
            best_time = curr_time
            best_steps = steps
            best_start = start_light

    return best_tour, best_time, best_steps, best_start


def fastest_tour_memo(start_light: str, L: list[str], TRAVEL_TIME: dict[tuple[str, str], float]) -> tuple[list[str], float, int, dict]:
    def fastest_tour_memo_inner(start_light: str, L: list[str], TRAVEL_TIME: dict[tuple[str, str], float], memo: dict[tuple, tuple[list[str], float]]):
        best_tour = []  # used to store the running best overall tour that starts at start_light
        best_time = inf  # used to store the time for the best_tour sequence
        all_steps = 0
        L = list_minus(L, start_light)  # remove start_light from list

        if len(L) == 1:
            second_light = L[0]
            best_tour, best_time = [start_light, second_light], get_travel_time(start_light, second_light, TRAVEL_TIME)
            memo[tuple([start_light] + L)] = (best_tour, best_time)
            return best_tour, best_time, 1, memo


        m = memo.get(tuple([start_light] + L))
        if m is not None:
            best_tour, best_time = m 
            # best_time += get_travel_time(start_light, best_tour[0], TRAVEL_TIME)
            all_steps = 1
            # print(f"MEMO HIT: {T}")
        else:
            # RECURSIVE CASE
            # print(f"MEMO MISS: {T}")
            for second_light in L:
                L_prime = list_minus(L, second_light)  # remove start_light from list
                if tuple(L_prime) in memo:
                    curr_tour, curr_time = memo[tuple(L_prime)]
                    all_steps+=1
                else:
                    curr_tour, curr_time, steps, memo = fastest_tour_memo_inner(second_light, L_prime, TRAVEL_TIME, memo)
                    all_steps += steps
                curr_time += get_travel_time(start_light, second_light, TRAVEL_TIME)
                if curr_time < best_time:  # update best_tour and best_time with new candidate
                    best_tour = curr_tour
                    best_time = curr_time
            best_tour = [start_light] + best_tour
            memo[tuple([start_light] + L)] = (best_tour, best_time)
        return best_tour, best_time, all_steps, memo
        

    memo = {}
    return fastest_tour_memo_inner(start_light, L, TRAVEL_TIME, memo)


# def fastest_tour_memo(start_light: str, L: list[str], TRAVEL_TIME: dict[tuple[str, str], float]) -> tuple[list[str], float, int, dict]:
#     def fastest_tour_memo_inner(start_light: str, L: list[str], TRAVEL_TIME: dict[tuple[str, str], float], memo: dict[tuple, tuple[list[str], float]]):
#         best_tour = []  # used to store the running best overall tour that starts at start_light
#         best_time = inf  # used to store the time for the best_tour sequence
#         all_steps = 0
#         # L = list_minus(L, start_light)  # remove start_light from list
#         T = (start_light, frozenset(L))
#         m = memo.get(T)

#         if len(L) == 1:
#             second_light = L[0]
#             best_tour, best_time = [start_light, second_light], get_travel_time(start_light, second_light, TRAVEL_TIME)
#             memo[T] = (best_tour, best_time)
#             return best_tour, best_time, 1, memo


#         if m is not None:
#             best_tour, best_time = m # best time already includes start light!!!
#             all_steps = 1
#             # print(f"MEMO HIT: {T}")
#         else:
#             # RECURSIVE CASE
#             # print(f"MEMO MISS: {T}")
#             for second_light in L:
#                 L_prime = list_minus(L, second_light)  # remove start_light from list
#                 curr_tour, curr_time, steps, memo = fastest_tour_memo_inner(second_light, L_prime, TRAVEL_TIME, memo)
#                 all_steps += steps
#                 curr_time += get_travel_time(start_light, second_light, TRAVEL_TIME)
#                 if curr_time < best_time:  # update best_tour and best_time with new candidate
#                     best_tour = curr_tour
#                     best_time = curr_time
#             best_tour = [start_light] + best_tour
#             memo[T] = (best_tour, best_time)
#         return best_tour, best_time, all_steps, memo
        

#     memo = {}
#     return fastest_tour_memo_inner(start_light, L, TRAVEL_TIME, memo)

def fastest_tour_bf(start_light: str, L: list[str], TRAVEL_TIME: dict[tuple[str, str], float]) -> tuple[list[str], float, int]:
    """
    Brute force graph traversal.

    ASSUMES a global variable TRAVEL_TIME exists which maps a tuple of start, end lighthouses to travel times and can be accessed with travel_time(start, stop)
    ASSUMES a function list_minus(L, x), which removes an element x from the list L

    Args:
        start_light (str): starting point of tour
        L (list[str]): light of lighthouses to visit

    Returns:
        best_tour (list[str]): list of lighthouses to tour with fastest time
        best_time (float): time to traverse lighthouse tour
        steps (int): number of recursive steps executed by the algorithm
    """

    best_tour = []  # used to store the running best overall tour that starts at start_light
    best_time = inf  # used to store the time for the best_tour sequence
    all_steps = 0
    L = list_minus(L, start_light)  # remove start_light from list

    if len(L) == 0:
        return [start_light], 0.0, 1

    # RECURSIVE CASE
    for second_light in L:
        curr_tour, curr_time, steps = fastest_tour_bf(second_light, L, TRAVEL_TIME)
        all_steps += steps
        y_time = get_travel_time(start_light, second_light, TRAVEL_TIME)
        if (curr_time + y_time) < best_time:  # update best_tour and best_time with new candidate
            best_tour = curr_tour
            best_time = curr_time + y_time

    # insert start_light at the front of best tour
    best_tour = [start_light] + best_tour
    return best_tour, best_time, all_steps


def run_tests(travel_times, answer_tour, answer_time):
    L = list(set([item for k in travel_times.keys() for item in k]))
    # L = ['G', 'A', 'H', 'C', 'I', 'E', 'J', 'B', 'F', 'D']
    print("\n----------")
    print(f"Running test on input: {L}")
    print(len(L))
    best_tour, best_time, steps, best_start  = fastest_tour_wrapper(L, travel_times)
    print(f"Result:\n\t{best_tour=}\n\t{best_time=}\n\t{steps=}\n\t{best_start=}")
    assert best_tour == answer_tour or best_tour[::-1] == answer_tour, f"Expected {answer_tour} got {best_tour}"
    assert best_time == answer_time, f"Expected {answer_time} got {best_time}"
    print("TEST PASSED")
    print("----------\n")


def test1():
    # Test #1
    TRAVEL_TIME = {
        ("D", "E"): 9.8874546134365,
        ("D", "B"): 8.650955785569098,
        ("D", "C"): 4.527990409960845,
        ("D", "A"): 9.817667809230786,
        ("E", "B"): 10.931854306263975,
        ("E", "C"): 7.255251488484818,
        ("E", "A"): 12.917982527478712,
        ("B", "C"): 4.113565483054365,
        ("B", "A"): 9.560863383439097,
        ("C", "A"): 7.854345573910511,
    }
    # Expected output
    # The best tour is:  A, B, C, D, E
    # The best time is:  28.089873889890804
    answer = ["A", "B", "C", "D", "E"]
    time = 28.089873889890804
    run_tests(TRAVEL_TIME, answer, time)


def test2():
    # Test #2
    TRAVEL_TIME = {
        ("B", "C"): 6.429795406216918,
        ("B", "A"): 11.629846115160516,
        ("B", "D"): 7.679251919404714,
        ("B", "E"): 9.347706263090837,
        ("C", "A"): 12.280646160363432,
        ("C", "D"): 7.746192483295421,
        ("C", "E"): 9.90681627370574,
        ("A", "D"): 12.227183481562683,
        ("A", "E"): 16.655823285647106,
        ("D", "E"): 8.25715774835559,
    }
    # Expected output
    # The best tour is:  A, B, C, D, E
    # The best time is:  34.06299175302845
    answer = ["A", "B", "C", "D", "E"]
    time = 34.06299175302845
    run_tests(TRAVEL_TIME, answer, time)


def test3():
    # Test #3
    TRAVEL_TIME = {
        ("F", "E"): 7.453320453415392,
        ("F", "D"): 6.170569410345761,
        ("F", "I"): 10.448429302986911,
        ("F", "G"): 6.187750187309644,
        ("F", "C"): 12.090422838563583,
        ("F", "H"): 11.539119418380032,
        ("F", "A"): 13.23865323724485,
        ("F", "J"): 14.209616157057711,
        ("F", "B"): 12.029520235766265,
        ("E", "D"): 4.594971038617467,
        ("E", "I"): 9.488857351897519,
        ("E", "G"): 4.661282508675182,
        ("E", "C"): 10.705763401441896,
        ("E", "H"): 10.12354365573923,
        ("E", "A"): 12.05863087182219,
        ("E", "J"): 12.857918364285274,
        ("E", "B"): 10.915808926216425,
        ("D", "I"): 8.773798408565863,
        ("D", "G"): 3.549820998388679,
        ("D", "C"): 9.084763991756446,
        ("D", "H"): 8.47244200438249,
        ("D", "A"): 10.768085646027655,
        ("D", "J"): 11.205467989446557,
        ("D", "B"): 9.811703475051996,
        ("I", "G"): 4.856711290250502,
        ("I", "C"): 10.303247633652786,
        ("I", "H"): 9.72873923304563,
        ("I", "A"): 11.752971702744057,
        ("I", "J"): 12.386140947772116,
        ("I", "B"): 10.715926552978804,
        ("G", "C"): 8.939922836985131,
        ("G", "H"): 8.325372714362043,
        ("G", "A"): 10.658709470483634,
        ("G", "J"): 11.05300320168352,
        ("G", "B"): 9.726036954632448,
        ("C", "H"): 14.85107596522508,
        ("C", "A"): 16.127909792272288,
        ("C", "J"): 17.54748278310382,
        ("C", "B"): 14.699070399680458,
        ("H", "A"): 15.723529687188293,
        ("H", "J"): 17.10791004081554,
        ("H", "B"): 14.306778662449995,
        ("A", "J"): 16.949188359233272,
        ("A", "B"): 14.239542023142393,
        ("J", "B"): 16.6207970728817,
    }
    # Expected output
    # The best tour is:  A, B, C, D, E, F, G, H, I, J
    # The best time is:  86.69967098910159

    answer = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
    time = 86.69967098910159
    run_tests(TRAVEL_TIME, answer, time)


def test4():
    # Test 4 - test against the actual lighthouses used in the challenge, so
    # you can see the original motivation for this assignment.  Times are from
    # maps.google.com and reflect best possible driving times between two
    # lighthouses subject to current traffic conditions.

    # If you want to visualize this tour, it's here:
    # https://goo.gl/maps/h9NbbQT5kS3S6kZ98

    # Note that in the real world, travel times are highly dependent on time of
    # day and are often not symmetrical-- that's part of why the TSP problem is
    # so interesting!

    TRAVEL_TIME = {
        ("Concord Point", "Seven Foot Knoll"): 0.88,
        ("Concord Point", "Lightship Chesapeake"): 0.87,
        ("Concord Point", "Hooper Strait"): 1.92,
        ("Concord Point", "Choptank River"): 2.02,
        ("Concord Point", "Drum Point"): 2.12,
        ("Concord Point", "Cove Point"): 2.15,
        ("Concord Point", "Piney Point"): 2.60,
        ("Concord Point", "Point Lookout"): 2.73,
        ("Concord Point", "Fort Washington"): 1.73,
        ("Concord Point", "Sandy Point"): 1.28,
        ("Seven Foot Knoll", "Lightship Chesapeake"): 0.07,
        ("Seven Foot Knoll", "Hooper Strait"): 1.52,
        ("Seven Foot Knoll", "Choptank River"): 1.62,
        ("Seven Foot Knoll", "Drum Point"): 1.58,
        ("Seven Foot Knoll", "Cove Point"): 1.62,
        ("Seven Foot Knoll", "Piney Point"): 2.05,
        ("Seven Foot Knoll", "Point Lookout"): 2.22,
        ("Seven Foot Knoll", "Fort Washington"): 1.17,
        ("Seven Foot Knoll", "Sandy Point"): 0.78,
        ("Lightship Chesapeake", "Hooper Strait"): 1.47,
        ("Lightship Chesapeake", "Choptank River"): 1.57,
        ("Lightship Chesapeake", "Drum Point"): 1.53,
        ("Lightship Chesapeake", "Cove Point"): 1.57,
        ("Lightship Chesapeake", "Piney Point"): 1.98,
        ("Lightship Chesapeake", "Point Lookout"): 2.17,
        ("Lightship Chesapeake", "Fort Washington"): 1.12,
        ("Lightship Chesapeake", "Sandy Point"): 0.73,
        ("Hooper Strait", "Choptank River"): 0.60,
        ("Hooper Strait", "Drum Point"): 2.03,
        ("Hooper Strait", "Cove Point"): 2.08,
        ("Hooper Strait", "Piney Point"): 2.50,
        ("Hooper Strait", "Point Lookout"): 2.67,
        ("Hooper Strait", "Fort Washington"): 1.77,
        ("Hooper Strait", "Sandy Point"): 0.93,
        ("Choptank River", "Drum Point"): 2.13,
        ("Choptank River", "Cove Point"): 2.17,
        ("Choptank River", "Piney Point"): 2.60,
        ("Choptank River", "Point Lookout"): 2.77,
        ("Choptank River", "Fort Washington"): 1.85,
        ("Choptank River", "Sandy Point"): 1.03,
        ("Drum Point", "Cove Point"): 0.23,
        ("Drum Point", "Piney Point"): 0.48,
        ("Drum Point", "Point Lookout"): 0.63,
        ("Drum Point", "Fort Washington"): 1.18,
        ("Drum Point", "Sandy Point"): 1.32,
        ("Cove Point", "Piney Point"): 0.70,
        ("Cove Point", "Point Lookout"): 0.83,
        ("Cove Point", "Fort Washington"): 1.28,
        ("Cove Point", "Sandy Point"): 1.35,
        ("Piney Point", "Point Lookout"): 0.72,
        ("Piney Point", "Fort Washington"): 1.42,
        ("Piney Point", "Sandy Point"): 1.78,
        ("Point Lookout", "Fort Washington"): 1.67,
        ("Point Lookout", "Sandy Point"): 1.97,
        ("Fort Washington", "Sandy Point"): 1.05,
    }

    # Expected output
    # The best tour is:  Choptank River, Hooper Strait, Sandy Point, Concord Point, Seven Foot Knoll, Lightship Chesapeake,
    #       Fort Washington, Cove Point, Drum Point, Piney Point, Point Lookout
    # The best time is:  7.59
    answer = [
        "Choptank River",
        "Hooper Strait",
        "Sandy Point",
        "Concord Point",
        "Seven Foot Knoll",
        "Lightship Chesapeake",
        "Fort Washington",
        "Cove Point",
        "Drum Point",
        "Piney Point",
        "Point Lookout",
    ]
    time = 7.59
    run_tests(TRAVEL_TIME, answer, time)



# test1()
# for i in range(4):
    # test2()
    # test3()
test2()
# test3()
# test4()


# 17855 HIT:
#  5116 MISS:
# 17947 STEPS: