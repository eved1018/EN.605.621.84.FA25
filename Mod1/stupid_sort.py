import random

def swap(arr, x, y):
    tmp = arr[x]
    arr[x] = arr[y]
    arr[y] = tmp
    return arr

def print_with_arrows(arr, indices):
    """
    Prints an array with ASCII arrows under specific indices.

    Args:
        arr (list): The list to print.
        indices (list): The indices to place arrows under.
    """
    # Print the array.
    print(arr)

    # Convert array elements to strings to find their lengths.
    str_arr = [str(item) for item in arr]

    # Calculate padding for each element based on its string length.
    padding = [len(s) for s in str_arr]

    # Build the arrow line.
    arrow_line = ""
    for i in range(len(arr)):
        # Add spacing before the element. The number of spaces is determined by
        # the comma and space in the list representation.
        if i > 0:
            arrow_line += "  "

        if i in indices:
            # Add spaces to center the arrow under the element.
            # `int(padding[i]/2)` is used for centered alignment.
            arrow_line += " " * int(padding[i] / 2) + "^" + " " * (padding[i] - int(padding[i] / 2) - 1)
        else:
            # If no arrow, add spaces for padding.
            arrow_line += " " * padding[i]
    
    # Print the arrow line.
    # Note: `[ ]` is 2 characters, so `2` is added to the start padding.
    print(" " + arrow_line)

def sprint(arr, x):
    s = []
    i = 0
    while i < len(arr):
        if i == x:
            s.append(f"{{{arr[i]}, {arr[i+1]}}}")
            i +=2
        else:
            s.append(arr[i])
            i +=1 
    return s
        

def main(arr, n):
    i = 0
    l = 0
    while i < n-1:
        print(i)
        if arr[i] > arr[i+1]:
            print(f"i={i} {sprint(arr, i)}")
            arr = swap(arr, i, i+1)
            l+=1
            if i > 0:
                i = i-1
        else:
            i  = i + 1
    # print(l)

# arr = [2, 1, 3, 4, 5]
# arr = random.sample(range(100), 5)
# arr = [5, 4, 3, 2, 1]
arr = [1,2,3,4,5]
print(arr)
print('--------------')

main(arr, len(arr))
print(arr)


