


def t(i):
    d = (i)
    print(d)
    print(id(d))


def e():
    for i in range(4):
        t(i)


e()
print()
t(1)
t(2)
t(3)
t(4)
t(5)