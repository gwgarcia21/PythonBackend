"""2. Set Operations: Write a program that takes 
two lists as input and uses sets to find the common 
elements, the unique elements in each list, and the 
union of the two lists."""
def set_operations(list1: list[int], list2: list[int]):
    print("Unique Elements in List1:", set(list1))
    print("Unique Elements in List2:", set(list2))
    union = list1 + list2
    print("Union of List1 and List2: ", union)
    unique = []
    for val in set(union):
        if val in list1 and val in list2:
            unique.append(val)
    print("Common elements of List1 and List2: ", unique)
    return

list1 = [1, 2, 3, 3, 4, 5, 6]
list2 = [2, 5, 6, 6, 8, 9]
set_operations(list1, list2)