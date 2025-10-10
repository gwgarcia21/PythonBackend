"""1. Mutability Challenge: Create a function that takes a list 
as input and modifies it in-place. Then, create another function 
that takes a tuple as input and returns a new tuple with the 
modified values (without modifying the original tuple)."""
def modify_list(my_list: list[int]):
    my_list.append(4)
    return my_list

def create_new_tuple(my_tuple):
    new_tuple = my_tuple + (4,)
    return new_tuple

list1 = [1, 2, 3]
print("Original List: ", list1)
print("Modified List: ", modify_list(list1))
print("Original List after modifying: ", list1)

tuple1 = (1, 2, 3)
print("Original Tuple: ", tuple1)
print("New Tuple: ", create_new_tuple(tuple1))

