"""Debugging: Use pdb or your IDE's debugger to step 
through the following code and identify the error:"""
import pdb

def calculate_average(numbers):
    pdb.set_trace()
    sum = 0
    for number in numbers:
        sum += number
    average = sum / len(numbers)
    return average

data = [10, 20, 30, 40, 50]
average = calculate_average(data)
print(f"The average is: {average}")

# n (next): Execute the next line of code.
# s (step): Step into a function call.
# c (continue): Continue execution until the next breakpoint.
# p <variable> (print): Print the value of a variable.
# q (quit): Exit the debugger.