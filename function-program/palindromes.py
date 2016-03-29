# -*- coding: utf-8 -*-
# 求回文数

'''
Created on Feb 20, 2016

@author: xuyi
'''
def is_palindrome(n):
    str_n = str(n)
    return str_n == str_n[::-1]

if __name__ == '__main__':
    output = filter(is_palindrome, range(1, 1000))
    print(list(output))
    pass