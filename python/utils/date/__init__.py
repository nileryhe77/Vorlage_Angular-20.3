def date_nice_1(d0):
    d1 = d0.split(' ')
    month = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    for i in range(0,12):
        if month[i] == d1[1]:
            j = i
    mm = str(101 + j)[1:3]
    dd = str(100 + int(d1[2]))[1:3]
    return d1[3] + '-' + mm + '-' + dd

