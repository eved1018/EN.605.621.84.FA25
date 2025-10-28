

k = ("c", frozenset(["a", "b"]) )

d =  {k: "1"}


if ("c", frozenset(["b", "a"])) in d:
    print("hit")
else:
    print("miss")

