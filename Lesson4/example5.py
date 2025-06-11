import pdb

def add(x, y):
    pdb.set_trace()  # Set a breakpoint
    result = x + y
    return result

print(add(5, 3))

# n (next): Execute the next line of code.
# s (step): Step into a function call.
# c (continue): Continue execution until the next breakpoint.
# p <variable> (print): Print the value of a variable.
# q (quit): Exit the debugger.