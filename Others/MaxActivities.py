def printMaxActivities(s, f):
    n = len(f)
    print("The following activities are selected")

    # The first activity is always selected
    i = 0
    print(i)

    # Consider rest of the activities
    for j in range(n):

        # If this activity has start time greater than
        # or equal to the finish time of previously
        # selected activity, then select it
        if s[j] >= f[i]:
            print(j)
            i = j


if __name__ == '__main__':
    s = [1, 3, 0, 5, 8, 5]
    f = [2, 4, 6, 7, 9, 9]
    printMaxActivities(s, f)
