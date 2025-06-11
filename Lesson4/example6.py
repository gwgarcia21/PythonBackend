import pdb
import sys

def divide(x, y):
    return x / y

def main():
    try:
        result = divide(10, 0)
        print(result)
    except Exception:
        extype, value, tb = sys.exc_info()
        pdb.post_mortem(tb)

if __name__ == "__main__":
    main()