def longSum():
    path = "C://Users//Bobeta//Desktop//bigNum.txt"
    #path = "C://Users//Bobeta//Desktop//lilNum.txt"
    with open(path) as file:
        num = file.read()
        nums = num.split('\n')
        summation = 0
        for x in nums:
            summation += int(x)
        summation = str(summation)
        return (summation[:10])

def longestCollatzSequence():
    longestSequence = 0
    for x in range(1000000):
        lenChain = 0
        while x > 1:
            lenChain += 1
            if not x%2:
                x = x/2
                continue
            x = 3*x + 1
        print(lenChain)
        if lenChain > longestSequence:
            longestSequence = lenChain
    return longestSequence
def winningHand(hand1, hand2):
    
    return 1
def pokerWins():
    path = "C://Users//Bobeta//Desktop//p054_poker.txt"
    with open(path) as file:
        text = file.read()
        games = text.split('\n')
        games = games[:-1]
        #games[x][:14] = hand1, games[x][16:] = hand2
        wonByOne = 0
        print(games[-1])
        for x in games:
            if winningHand(x[:14],x[16:]):
                wonByOne += 1
        
    return wonByOne

def bouncyNumber(percent = .99):
    bouncyNumbers = 0
    totalNumbers = 100
    index = 100
    while bouncyNumbers/totalNumbers < percent:
        index += 1
        totalNumbers += 1
        string = str(index)
        inc = True
        dec = True
        for num in range(len(string)-1):
            if int(string[num]) > int(string[num+1]):
                inc = False
            if int(string[num]) < int(string[num+1]):
                dec = False
            if not inc and not dec:
                bouncyNumbers += 1
                break
    return index


def isPalindromic(num):
    num = str(num)
    if num == num[::-1]:
        return True
    return False
def PalindromicSums(max = 10**8):
    index = max**(1/2)
    while index:



            