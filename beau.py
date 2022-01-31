# import sys
from tags import *

def save_file(name, content):
    f = open(name, "w")
    f.write(content)
    f.close()
            
def main():
    tokens = []

    tokens.append(Token(Tag(TagType.Paragraph, 0)))
    tokens.append(Token(Value("Hello", ValueType.String)))
    tokens.append(Token(Tag(TagType.Paragraph, 1)))
    tokens.append(Token(Tag(TagType.HeaderFour, 0)))
    tokens.append(Token(VariableAssign("Bonjour", "Hoeraa")))
    tokens.append(Token(VariableIndex("Bonjour")))
    tokens.append(Token(Tag(TagType.HeaderFour, 1)))

    variables = {}

    html = ""
    for token in tokens:
        if type(token.tag) == Tag:
            t = token.tag
            match t.tag:
                case TagType.Paragraph:
                    if t.type == 0: html += "<p>"
                    else: html += "</p>"
                case TagType.HeaderOne:
                    if t.type == 0: html += "<h1>"
                    else: html += "</h1>"
                case TagType.HeaderTwo:
                    if t.type == 0: html += "<h2>"
                    else: html += "</h2>"                    
                case TagType.HeaderThree:
                    if t.type == 0: html += "<h3>"
                    else: html += "</h3>"
                case TagType.HeaderFour:
                    if t.type == 0: html += "<h4>"
                    else: html += "</h4>"
                case TagType.HeaderF:
                    if t.type == 0: html += "<h5>"
                    else: html += "</h5>"                                                                
        elif type(token.tag) == Value:
            html += token.tag.value
        elif type(token.tag) == VariableAssign:
            variables[token.tag.identifier] = token.tag.value
        elif type(token.tag == VariableIndex):
            html += variables[token.tag.identifier]

    save_file("index.html", html)


if __name__ == "__main__":
    # if len(sys.argv) < 2:
    #     print("[ERROR] You did not supply enough arguments")
    #     print("[INFO] To execute type: 'py ./beau.py <FILENAME>'")
    # elif len(sys.argv) > 2:
    #     print("[ERROR] You supplied too many arguments")
    #     print("[INFO] To execute type: 'py ./beau.py <FILENAME>'")
    # else:
    #     main()
    main()