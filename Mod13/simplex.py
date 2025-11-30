def print_tab(tab):
    for row in tab:
        print(row)
    print()


def find_pivot_col(tab):
    col, val = min(enumerate(tab[-1]), key=lambda x: x[1])
    if val >= 0:
        return None
    return col


def find_pivot_row(tab, pc):
    row, val = min(
        [
            (r, tab[r][-1] / tab[r][pc])
            for r, _ in enumerate(tab)
            if tab[r][pc] > 0 and tab[r][-1] / tab[r][pc] >= 0
        ],
        key=lambda x: x[1],
    )
    return row


def pivot(tab, pr, pc):
    p = tab[pr][pc]

    print(p)
    for c, i in enumerate(tab[pr]):
        tab[pr][c] = i / p 
    for i, _ in enumerate(tab):
        mult = tab[i][pc]
        if i == pr:
            continue
        for j, _ in enumerate(tab[i]):
            tab[i][j] -= mult * tab[pr][j]

    return tab


def simplex(tab):
    print_tab(tab)
    while True:
        pc = find_pivot_col(tab)
        if pc is None:
            return tab[-1]
        pr = find_pivot_row(tab, pc)
        print(pr, pc)
        tab = pivot(tab, pr, pc)


tab = [
    [0, 1, 1, 0, 0, 0, 0, 2],
    [1, 0, 0, 1, 0, 0, 0, 1],
    [1, 0, 0, 0, 1, 0, 0, 2],
    [1, 1, 0, 0, 0, 1, 0, 2.5],
    [-1, -1, 0, 0, 0, 0, 1, 0],
]

r = simplex(tab)
print(r)
