import sys
from .classmodule import MyClass
from .funcmodule import my_function
import requests
import pandas as pd
import sys

def main():
    args = sys.argv[1:]    
    print(args)    
    my_function(args)
if __name__ == '__main__':
    main()

