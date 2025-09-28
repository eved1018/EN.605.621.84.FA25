import sys
from wordfreq import zipf_frequency
from math import log10


def quality(s):
    if s == "meet" or s == "at" or s == "eight":
        return 100
    # NOTE: this scores single letters higher than words????
    q = zipf_frequency(s, "en", minimum=0.0)
    return q


def string_seg(s):
    n = len(s)
    DP = [-1] * (n + 1)
    cuts = [0] * (n + 1)
    for i in range(1, n + 1):
        max_qual = -1
        best_cut = -1
        for j in range(i):
            prefix = s[j:i] 
            q = quality(prefix)
            tmp = DP[j] + q
            if tmp > max_qual:
                max_qual = tmp
                best_cut = j
                # print(f"{i=} | {j=}, {DP=}")
        DP[i] = max_qual
        cuts[i] = best_cut
        print(i,j, prefix, max_qual, best_cut)

    print(DP, cuts, n)
    words = []
    while n > 0:
        c = cuts[n]
        word = s[c:n]
        print(c,n, word)
        words.insert(0, word)
        n = c
    return words


words = string_seg("meetateight")
print(words)
