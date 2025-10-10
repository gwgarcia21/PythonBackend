import cProfile
import pstats

def slow_function():
    """A function that takes a long time to execute."""
    result = 0
    for i in range(10000000):
        result += i
    return result

def fast_function():
    """A function that executes quickly."""
    return sum(range(1000))

def main():
    slow_function()
    fast_function()

# Profile the main function and save the results to a file
cProfile.run('main()', 'profile_output')

# Analyze the profiling results
p = pstats.Stats('profile_output')
p.sort_stats('cumulative').print_stats(10) # Sort by cumulative time and print top 10 functions