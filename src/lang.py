from sys import *

development_mode = False

tokens = []

def open_file(filename):
    data = open(filename, "r").read()
    data+="<EOF>"
    return data

def lex(data):
    tok = ""
    state = 0
    string = ""
    isexpr = 0
    expr = ""
    n = ""
    data = list(data)
    for char in data:
        tok += char
        if tok == " ":
            if state == 0:
                tok = ""
            else:
                tok = " "
        elif tok == "\n" or tok == "<EOF>":
            if expr != "" and isexpr == 1:
                tokens.append("EXPR:" + expr)
                expr=""
            elif expr != "" and isexpr == 0:
                tokens.append("NUM:" + expr)
                expr = ""
            tok = ""
        elif tok == "Print" or tok == "print":
            tokens.append("PRINT")
            tok = ""
        
        # NUMBERS
        elif tok == "0" or tok == "1" or tok == "2" or tok == "3" or tok == "4" or tok == "5" or tok == "6" or tok == "7" or tok == "8" or tok == "9":
            expr += tok
            tok = ""
        elif tok == "+" or tok == "-" or tok == "*" or tok == "/" or tok == "(" or tok == ")":
            isexpr = 1
            expr += tok
            tok = ""
        elif tok == "\"":
            if state == 0:
                state = 1
            elif state == 1:
                tokens.append("STRING:"+string+"\"")
                string = ""
                state = 0
                tok = ""
        elif state == 1:
            string += tok
            tok = ""
    if development_mode == True:
        print(tokens)

    return tokens

def doPrint(topr):
    if(topr[0:6] == "STRING"):
        topr = topr[8:]
        topr = topr[:-1]
    elif(topr[0:3] == "NUM"):
        topr = topr[4:]
    elif(topr[0:4] == "EXPR"):
        topr = topr[5:]
    print(topr)

def parse(tox):
    i = 0
    while i < len(tox):
        
        if tox[i] + " " + tox[i+1][0:6] == "PRINT STRING" or tox[i] + " " + tox[i+1][0:3] == "PRINT NUM" or tox[i] + " " + tox[i+1][0:4] == "PRINT EXPR":
            if tox[i+1][0:6] == "STRING":
                doPrint(tox[i+1])
            elif tox[i+1][0:3] == "NUM":
                doPrint(tox[i+1])
            elif tox[i+1][0:4] == "EXPR":
                doPrint(tox[i+1])
            i+=2

def run():
    data = open_file(argv[1])
    tox = lex(data)
    parse(tox)

run()