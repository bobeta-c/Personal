# -*- coding: utf-8 -*-
"""
Created on Mon Mar  7 12:37:28 2022

@author: Bobeta
"""

def PrimeFactors(n):
    factors = []
    i = 2
    while not  i > n:
        if not n%i:
            factors.append(i)
            n //= i
        i += 1
    return factors
primes = []
def SmartPrimeFactors(n):
    factors = []
    for x in primes:
        while n%x == 0:
            factors.append(x)
            n //= x
        continue
    for x in PrimeFactors(n):
        primes.append(x)
        factors.append(x)
    return factors
def nthPrime(n):
    primes = []
    a = 2
    lenPrimes = 0
    while lenPrimes < n:
        if len(SmartPrimeFactors(a)) == 1:
            primes.append(a)
            lenPrimes += 1
            if lenPrimes%1000 == 0:
                print(a)
        a += 1
    return primes

def fib(n, fibs = {1: 1, 2: 1}):
    if n in fibs:
        return fibs[n]
    fibs[n] = fib(n-1) + fib(n-2)
    return fibs[n]

bigNum = 7316717653133062491922511967442657474235534919493496983520312774506326239578318016984801869478851843858615607891129494954595017379583319528532088055111254069874715852386305071569329096329522744304355766896648950445244523161731856403098711121722383113622298934233803081353362766142828064444866452387493035890729629049156044077239071381051585930796086670172427121883998797908792274921901699720888093776657273330010533678812202354218097512545405947522435258490771167055601360483958644670632441572215539753697817977846174064955149290862569321978468622482839722413756570560574902614079729686524145351004748216637048440319989000889524345065854122758866688116427171479924442928230863465674813919123162824586178664583591245665294765456828489128831426076900422421902267105562632111110937054421750694165896040807198403850962455444362981230987879927244284909188845801561660979191338754992005240636899125607176060588611646710940507754100225698315520005593572972571636269561882670428252483600823257530420752963450
def biggestCombo(number, length):
    wordNumber = str(number)
    largest = 0
    largestCombo = []
    for x in range(len(wordNumber)-length):
        product = 1
        for y in wordNumber[x:x+length]:
            product = product * int(y)
        if product > largest:
            largest = product
            largestCombo =int(wordNumber[x:x+length])
    return largest, largestCombo
    
def specialPythagoreanTriplet():
    for a in range(1, 1000):
        for b in range(1, 1000):
            for c in range(1, 1000):
                if a+b+c == 1000:
                    if a**2 + b**2 == c**2:
                        return a, b, c

def LargestProductOnGrid():
    stringGrid = "08 02 22 97 38 15 00 40 00 75 04 05 07 78 52 12 50 77 91 08\n\
49 49 99 40 17 81 18 57 60 87 17 40 98 43 69 48 04 56 62 00\n\
81 49 31 73 55 79 14 29 93 71 40 67 53 88 30 03 49 13 36 65\n\
52 70 95 23 04 60 11 42 69 24 68 56 01 32 56 71 37 02 36 91\n\
22 31 16 71 51 67 63 89 41 92 36 54 22 40 40 28 66 33 13 80\n\
24 47 32 60 99 03 45 02 44 75 33 53 78 36 84 20 35 17 12 50\n\
32 98 81 28 64 23 67 10 26 38 40 67 59 54 70 66 18 38 64 70\n\
67 26 20 68 02 62 12 20 95 63 94 39 63 08 40 91 66 49 94 21\n\
24 55 58 05 66 73 99 26 97 17 78 78 96 83 14 88 34 89 63 72\n\
21 36 23 09 75 00 76 44 20 45 35 14 00 61 33 97 34 31 33 95\n\
78 17 53 28 22 75 31 67 15 94 03 80 04 62 16 14 09 53 56 92\n\
16 39 05 42 96 35 31 47 55 58 88 24 00 17 54 24 36 29 85 57\n\
86 56 00 48 35 71 89 07 05 44 44 37 44 60 21 58 51 54 17 58\n\
19 80 81 68 05 94 47 69 28 73 92 13 86 52 17 77 04 89 55 40\n\
04 52 08 83 97 35 99 16 07 97 57 32 16 26 26 79 33 27 98 66\n\
88 36 68 87 57 62 20 72 03 46 33 67 46 55 12 32 63 93 53 69\n\
04 42 16 73 38 25 39 11 24 94 72 18 08 46 29 32 40 62 76 36\n\
20 69 36 41 72 30 23 88 34 62 99 69 82 67 59 85 74 04 36 16\n\
20 73 35 29 78 31 90 01 74 31 49 71 48 86 81 16 23 57 05 54\n\
01 70 54 71 83 51 54 69 16 92 33 48 61 43 52 01 89 19 67 48"

    stringGrid = stringGrid.split('\n')
    for x in range(len(stringGrid)):
        listofNums = stringGrid[x].split(' ')
        for y in range(len(listofNums)):
            
            listofNums[y] = int(listofNums[y])
        stringGrid[x] = listofNums
    #print(stringGrid)
    #left --> right
    largest = 0
    for x in stringGrid:
        for y in range(len(x) - 3):
            biggest = x[y]*x[y+1]*x[y+2]*x[y+3]
            if biggest > largest:
                largest = biggest
    #print(largest)
    #up --> down
    for x in range(len(stringGrid[0])):
        for y in range(len(stringGrid)-3):
            biggest = stringGrid[y][x] * stringGrid[y+1][x] * stringGrid[y+2][x] * stringGrid[y+3][x]
            if biggest > largest:
                largest = biggest
    #diagonally - right
    for x in range(len(stringGrid[0])-3):
        for y in range(len(stringGrid)-3):
            biggest = stringGrid[y][x] * stringGrid[y+1][x+1] * stringGrid[y+2][x+2] * stringGrid[y+3][x+3]
            if biggest > largest:
                largest = biggest    
    #diagonally - left
    for x in range(len(stringGrid[0])-3):
        for y in range(len(stringGrid)-3):
            biggest = stringGrid[y+3][x] * stringGrid[y+2][x+1] * stringGrid[y+1][x+2] * stringGrid[y][x+3]
            if biggest > largest:
                largest = biggest
    return largest