'''
Created on Feb 21, 2016

@author: xuyi
'''
def triangles():
    yield [1]
    old_list = [1,1]
    while True:
        yield old_list
        new_list = [1]
        for i in range(len(old_list)-1):
            new_list.append(old_list[i] + old_list[i+1])
        new_list.append(1)
        old_list = new_list

if __name__ == '__main__':
    n = 0
    for t in triangles():
        print(t)
        n = n + 1
        if n == 10:
            break