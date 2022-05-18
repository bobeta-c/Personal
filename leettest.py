class Solution:
    def intToRoman(self, num: int) -> str:
        data = {1:'I', 4:'IV', 5:'V', 9:'IX', 10: 'X', 40:'XL', 50:'L', 90:'XC', 100:'C', 400:'CD', 500:'D', 900:'CM', 1000 : 'M'}
        string = ""
        while num > 0:
            for x in list(data.keys())[::-1]:
                if num - x >= 0:
                    string = string + data[x]
                    num = num -x
                    break
        return string
    def numberToWords(self, num: int) -> str:
        if not num:
            return 'Zero'
        num = str(num)
        string = ''
        words = ['','','One', 'Two','Three','Four','Five','Six','Seven','Eight','Nine','Ten','Eleven','Twelve','Thirteen','Fourteen','Fifteen','Sixteen', 'Seventeen','Eighteen','Nineteen','Twenty','Thirty','Forty','Fifty','Sixty','Seventy','Eighty','Ninety']
        nums = [0,'00',1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,30,40,50,60,70,80,90]
        dictionary = {str(nums[i]): words[i] for i in range(len(nums))}
        places = {1:'',2:'Thousand',3:'Million',4:'Billion'}
        sectioned = []
        sectioned.append(num[:len(num)%3] if len(num)%3 > 0 else num[:3])
        num = num[len(num)%3 if len(num)%3 > 0 else 3:]
        while len(num) > 0:
            sectioned.append(num[:3])
            num = num[3:]
        index = 0
        for chunk in sectioned[::-1]:
            if len(chunk) < 2:
                chunk = ['0','0',chunk[0]]
            elif len(chunk) < 3:
                chunk = ['0', chunk[0], chunk[1]]
            index += 1
            chunkStr = ''
            tens = False
            for num in range(len(chunk)):
                if num == 0 and int(chunk[num]) >= 1:
                    chunkStr += dictionary[chunk[num]] + ' Hundred'
                elif num == 1 and int(chunk[num]) == 1:
                    chunkStr += dictionary[chunk[num] + chunk[num+1]] + ' '
                    tens = True
                elif num == 1:
                    chunkStr += dictionary[chunk[num]+'0']
                elif num == 2 and not tens:
                    chunkStr += dictionary[chunk[num]]
                if chunk[num] != '0' and not tens:
                    chunkStr += ' '
                
                #print(chunkStr)
            string = chunkStr+places[index]+ " " +string if chunkStr else string
        return string.strip()
    def criticalConnections(self, n: int, connections):
        workingNums = []
        criticals = []
        for x in range(n):
            if not isPath(x,x,connections):
                criticals.append()
        return criticals
def isPath(start, stop, connections):
    for x in range(len(connections)):
        if start in connections[x]:
            index = connections[x].index(start)
            other = 1 if index == 0 else 0
            if stop == connections[other]:
                return True
            options = isPath(connections[x][other], stop, connections[0:x]+connections[x+1:])
            if options:
                return True
    return False
#print(isPath(0,5,[[0,1],[1,2],[2,1],[2,3],[3,1],[3,4],[2,5]]))
print(Solution.criticalConnections(None, n = 1000, connections = [[0,1]]))


