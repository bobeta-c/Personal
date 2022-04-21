wierd = []
total = 0
equal5 = 0
equal5ls = []
rand = []
lettersIn = ['h','o','r']
lettersOut = ['p','u','c','s','e']
with open("C://Users//Bobeta//Desktop//words.txt", 'r') as file:
    text = file.read()
    words = text.split("\n")
    for x in words:
        word = x.lower()
        try:
            if (len(x) == 5 and x[0].lower() == 'h' and x[1].lower() == 'o' and x[2].lower() != 'r'):
                inside = True
                for y in lettersIn:
                    if not y in word:
                        inside = False
                for y in lettersOut:
                    if y in word:
                        inside = False
                if inside:
                    wierd.append(word)
                
        except:
            pass