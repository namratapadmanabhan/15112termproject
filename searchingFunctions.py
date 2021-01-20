#The main purpose of this file is to act as helper functions which we will 
#call when we need them in the other classes. We are just doing a binary search 
#and checking to make sure that a character is a letter.

import string

def isPossibleChar(characters):
    for char in characters:
        if len(char) != 1 and (letter not in string.ascii_lowercase):
            return False
    return True

#next 2 functions are from the code I wrote in homework 10
def binarySearch(L, item):
    return finder(L, item, 0, len(L) - 1)

def finder(L, item, lo, hi):
    mid = (lo + hi)//2
    if lo > hi:
        return []
    if L[mid] == item:
        return [(mid, L[mid])]
    elif L[mid] > item:
        return [(mid, L[mid])] + finder(L, item, lo, mid - 1)
    else: 
        return [(mid, L[mid])] + finder(L, item, mid + 1, hi)

def canPlaceInCell(cells):
    for cell in cells:
        try:
            location = int(cell)
        except ValueError:
            return False
    return True
