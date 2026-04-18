def shellSort(alist):
    sublistcount = len(alist) // 2
    while sublistcount > 0:
        for startposition in range(sublistcount):
            gapInsertionSort(alist, startposition, sublistcount)
        print("After increments of size", sublistcount,
              "The list is", alist)
        sublistcount = sublistcount // 2

def gapInsertionSort(alist, start, gap):
    for i in range(start+gap, len(alist), gap):
        currentvalue = alist[i]
        position = i
        while position >= gap and alist[position-gap] > currentvalue:
            alist[position] = alist[position-gap]
            position = position-gap
        alist[position] = currentvalue

# 测试代码
if __name__ == "__main__":
    test_list = [54, 26, 93, 17, 77, 31, 44, 55, 20]
    print("Original list:", test_list)
    shellSort(test_list)
    print("Sorted list:", test_list)
