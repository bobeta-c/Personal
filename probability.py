import matplotlib.pyplot as plt

letters = "AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz"
letters_l = letters[1::2]
letters_L = letters[::2]
mydict = {}
"""
with open("C://Users//Bobeta//Desktop//words.txt", "r") as file:
    text = file.read()
    all_words = text.split('\n')
    words = []
    for x in all_words:
        if len(x)==5:
            words.append(x)
    for x in words:
        mydict[x] = [x, 0, 0]
        for y in words:
            for z in range(len(y)):
                if y[z] in x:
                    for index in range(len(x)):
                        if (y[z] == x[index] and z==index):
                            # if letters are in the same spot as another word add 1
                            mydict[x][2] = mydict[x][2] + 1
                    # if letter in the same word add 1
                    mydict[x][1] = mydict[x][1] + 1
        print(mydict[x])
"""
import pickle
a_file = open("data.pkl", "rb")
mydict = pickle.load(a_file)
top1 = 0
top2 = 0
for x in mydict:
    if mydict[x][1] > top1:
        top1 = mydict[x][1]
    if mydict[x][2] > top2:
        top2 = mydict[x][2]
    
for x in mydict:
    mydict[x][1] = mydict[x][1]/top1
    mydict[x][2] = mydict[x][2]/top2


order1 = sorted(list(mydict.values()), key = lambda x: x[1])
xvals = []
yvals = []
for x in order1:
    xvals.append(x[1])
    yvals.append(x[2])

plt.plot(xvals, yvals)




a_file.close()