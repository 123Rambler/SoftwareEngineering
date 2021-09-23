import re
class Stack(object):
    def __init__(self):
        self.items = []
    def isEmpty(self):
        return self.items == []
    def push(self, item):
        self.items.append(item)
    def pop(self):
        return self.items.pop()
    def peek(self):
        return self.items[len(self.items)-1]
    def size(self):
        return len(self.items)
    def value(self,num):
        return self.items[num]

def readFile(file_name):
    result = []
    if file_name.endswith('.cpp') or file_name.endswith('.c'):
        fr = open(file_name, 'r')
        for line in fr:
            result.append(line)
        fr.close()
    text = "".join(result)
    reg = r"(\/\*([^\*^\/]*|[\*^\/*]*|[^\**\/]*)*\*\/|\/\/.*|'.*'|\"([^\"]*)\")" #Replace the comment
    com = re.finditer(reg,text)
    for key in com:
        text = text.replace(key.group(),' ')
    return text

def countKeyWords(kwList, text):
    reg = r'\b[a-zA-Z]+\b'
    line = re.findall(reg, text)
    res = {}
    for word in kwList:
        num = line.count(word)
        if num != 0:
            res[word] = num
    items = list(res.items())
    sum = 0
    for i in range(len(items)):
        kw, num = items[i]
        # print(kw, 'num : ', num)
        sum += num
    print("total num :", sum)

def countSwitch(text):
    reg = r'\b[a-zA-Z]+\b' 
    line = re.findall(reg, text)
    switch_num = 0
    flag = 0  
    case_num = []
    if line.count('switch') == 0:
        print("There is no switch keyword in the keywords list")
        return 0
    for kw in line:
        if kw == 'switch':
            switch_num += 1
            flag = 1
            case_num.append(0)
        if flag == 1 and kw == 'case':
            case_num[switch_num-1] += 1
    print("switch num: ", switch_num)
    for i in range(len(case_num)):
        print("Case num for No.{} switch: {}".format(i+1, case_num[i]))

def countIfElseIf(text, level):
    reg = r"\be.*?f\b"
    reg1 = r'\b[a-zA-Z]+\b'
    newText = replaceElseIf(text, reg)
    newkwList = re.findall(reg1, newText)
    ifelse_num = 0
    ifelifelse_num = 0
    ifelifelse_flag = 0
    stack = Stack()
    for kw in newkwList:
        if kw == 'if':
            stack.push('if')
        if stack.size() >= 1:
            if kw == 'elseif': 
                if stack.value(-1) == 'if':
                    stack.push('elseif')
            elif kw == 'else':
                if stack.value(-1) == 'if':
                    ifelse_num += 1
                else:
                    while (stack.value(-1) != 'if'):
                        ifelifelse_flag = 1
                        stack.pop()
                    stack.pop()
                    if ifelifelse_flag:
                        ifelifelse_num += 1
                        ifelifelse_flag = 0
    if level == 3:
        print("if-else num: {}".format(ifelse_num))
    if level == 4:
        print("if-elif-else num: {}".format(ifelifelse_num))

def replaceElseIf(text, reg):
    elseIf = re.finditer(reg, text)
    for key in elseIf:
       text = text.replace(key.group(), 'elseif')
    return text
    
if __name__ == "__main__":
    kwList = ["auto", "break", "case", "char", "const", "continue", "default", "do", "double", "else", "enum",
				"extern", "float", "for", "goto", "if", "int", "long", "register", "return", "short", "signed",
				"sizeof", "static", "struct", "switch", "typedef", "union", "unsigned", "void", "volatile", "while"]
    file_name = input("Please enter the path of your file: ")
    level = int(input("Please enter the level you want(1-4): "))
    text = readFile(file_name)
    if level == 1:
        countKeyWords(kwList, text)
    elif level == 2:
        countSwitch(text)
    else:
        countIfElseIf(text, level)


