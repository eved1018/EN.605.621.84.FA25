from math import inf



def mergeSort(inputList):
    # takes a list of values and returns a sorted list
    # if you use this, be sure to count the workload steps here
    #      consistent with the way you count them in your algorithm
    steps = 0
    if len(inputList) > 1:
        mid = len(inputList) // 2
        left = inputList[:mid]
        right = inputList[mid:]

        # Recursive call on each half
        _, lsteps = mergeSort(left)
        _, rsteps = mergeSort(right)
        steps += lsteps + rsteps
        
        # Two iterators for traversing the two halves
        i = 0
        j = 0
        
        # Iterator for the main list
        k = 0
        
        while i < len(left) and j < len(right):
            if left[i][1] <= right[j][1]:
              # The value from the left half has been used
              inputList[k] = left[i]
              # Move the iterator forward
              i += 1
            else:
                inputList[k] = right[j]
                j += 1
            steps +=1
            # Move to the next slot
            k += 1

        # For all the remaining values
        while i < len(left):
            inputList[k] = left[i]
            i += 1
            k += 1
            steps +=1

        while j < len(right):
            inputList[k]=right[j]
            j += 1
            k += 1
            steps +=1
            
    return (inputList), steps

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

L = list(set([item for k in TRAVEL_TIME.keys() for item in k]))

def list_minus(L, x):
    # Returns a list of L that does not have x in it
    return list(set(L) - set([x,]))

def get_travel_time(x, y, travel_time):
    # Looks up x and y in travel_time in a way that order does not matter, returns a time
    tm = travel_time.get((x, y), travel_time.get((y, x)))
    if tm is None:
        raise ValueError(f"{x, y} not in travel_time. {travel_time=}")
    return tm

def fastest_tour_nn(start_light, L, travel_times):
    best_tour = [start_light]  # used to store the running best overall tour that starts at start_light
    best_time = 0  # used to store the time for the best_tour sequence
    all_steps = 0
    L = list_minus(L, start_light)  # remove start_light from list

    while len(L):
        # find nn
        distances, steps = mergeSort([(second_light, get_travel_time(start_light, second_light, travel_times)) for second_light in L])
        all_steps += steps + len(L)
        # update output
        nn, dist = distances[0]
        best_time += dist
        best_tour.append(nn)
        # next itr
        L = list_minus(L, nn)
        start_light = nn
    return best_tour, best_time, all_steps

tour, time, steps = fastest_tour_nn("A", L, TRAVEL_TIME)
print(tour, time, steps)


# line: steps bf, memo, nn 
# many hists: distr of error (mean, std, perc) for each size
# hist: mean error by size
# hit:  normalzied error by size 
# whisker plot 
# mean_errors = []
    # median_errors = []
    # above_std = []
    # below_std = []

    # print("{:^10}|{:^10}|{:^10}|{:^10}|{:^10}|{:^10}|{:^10}|{:^10}|{:^10}".format("X", "Memo", "Aprox",  "Mean", "Median", "Best", "Worst", "Std", "Var"))
    # print("-"*100)
    # for i in memo_times: 
    #     memos = sum(memo_times[i]) / len(memo_times[i])
    #     nns = sum(nn_times[i]) / len(nn_times[i])
    #     errors = [((n-m)/m)*100 for m, n in zip (memo_times[i], nn_times[i])]
    #     mean = sum(errors) / len(errors)
    #     mean_errors.append(mean)
    #     errors.sort()
    #     median = errors[len(errors)//2]
    #     median_errors.append(median)
    #     best = errors[0]
    #     worst = errors[-1]
    #     var  = sum([(x-mean)**2 for x in errors]) / len(errors)
    #     stddev  = sqrt(var)
    #     above_std.append(mean + stddev)
    #     below_std.append(mean - stddev)

    #     print(f"{i:^10.2f}|{memos:^10.2f}|{nns:^10.2f}|{mean:^10.2f}|{median:^10.2f}|{best:^10.2f}|{worst:^10.2f}|{stddev:^10.2f}|{var:^10.2f}")

    # plt.figure()
    # plt.title("Error Comparison", size="xx-large")
    # plt.ylabel("%Error", size="x-large")
    # plt.xlabel("Input Size", size="x-large")
    # plt.plot(xvals, mean_errors, "b^-", markersize=10, linewidth=2, label="Mean %Error",  alpha=0.25)
    # plt.plot(xvals, median_errors, "r^-", markersize=10, linewidth=2, label="Median %Error",  alpha=0.25)
    # plt.fill_between(xvals, below_std, above_std, alpha=0.4, label="+/- stddev")
    # plt.tick_params(axis="both", which="major", labelsize=14)
    # plt.legend()
    # plt.show()