#!/usr/bin/env python3

import sys, os
from pprint import pprint

def greeting(name: str) -> str:
    return 'Hello ' + name

def main():
    """
    this is main function of this silly script
    """
    
    lst = []

    greeting(lst)

    print('main function')  # test comment

if __name__ == "__main__":
    param1, param2 = sys.argv[1], sys.argv[2]
    main()

