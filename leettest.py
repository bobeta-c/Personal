class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next
    def __str__(self):
        str = ''
        str = str + f'[{self.val}]'
        temp = self
        while temp.next:
            temp = temp.next

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
    def mergeTwoLists(self, list1, list2):
        out_list = []
        el1 = list1.pop(0) if len(list1) else None
        el2 = list2.pop(0) if len(list2) else None
        while len(list1) or len(list2):
            if el1 and (el2 == None or el1 < el2):
                out_list.append(el1)
                el1 = list1.pop(0)
            else:
                out_list.append(el2)
                el2 = list2.pop(0)
        if el1 and el2:
            out_list = out_list + [el1,el2] if el1 < el2 else out_list + [el2, el1]
        else:
            out_list.append(el1 if el1 else el2)
        return out_list
    def mergeTwoLinkedLists(self, list1, list2):
        out_list = ListNode(None)
        current_node = out_list
        while list1.next or list2.next:
            if list1.val < list2.val:
                if not out_list.val:
                    out_list.val = list1.val
                else:
                    current_node.next = ListNode(list1.val)
                    current_node = current_node.next
                list1 = list1.next
            else:
                if not out_list.val:
                    out_list.val = list2.val
                else:
                    current_node.next = ListNode(list2.val)
                    current_node = current_node.next
                list2 = list2.next
        return out_list




lt1 = ListNode(0, ListNode(1, ListNode(2)))
lt2 = ListNode(0, ListNode(2, ListNode(5)))
solution = (Solution.mergeTwoLinkedLists(None, lt1, lt2))
print(solution.val, solution.next)

while solution.next:
    print(solution.val)
    solution = solution.next


