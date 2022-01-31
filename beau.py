# import sys
from tags import *

def save_file(name, content):
    f = open(name, "w")
    f.write(content)
    f.close()
            
def main():
    tokens = []

    tokens.append(Token(Tag(TagType.Div, 0)))
    tokens.append(Token(Tag(TagType.Paragraph, 0)))
    tokens.append(Token(Value("Hello", ValueType.String)))
    tokens.append(Token(Tag(TagType.Paragraph, 1)))
    tokens.append(Token(Tag(TagType.Break, 2)))
    tokens.append(Token(Tag(TagType.HeaderFour, 0)))
    tokens.append(Token(VariableAssign("Bonjour", "Hoeraa")))
    tokens.append(Token(VariableIndex("Bonjour")))
    tokens.append(Token(Tag(TagType.HeaderFour, 1)))
    tokens.append(Token(Tag(TagType.Div, 1)))

    variables = {}
    depth = 0
    tab = "    "
    html = ""
    for token in tokens:
        if type(token.tag) == Tag:
            t = token.tag

            if t.type == 1 and depth > 0:
                depth -= 1

            html += tab*depth
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
                case TagType.HeaderFive:
                    if t.type == 0: html += "<h5>"
                    else: html += "</h5>"   
                case TagType.Div:
                    if t.type == 0: html += "<div>"
                    else: html += "</div>"
                case TagType.Break:
                    html += "</br>"
            html += "\n"
            
            if t.type == 0:
                depth += 1

        elif type(token.tag) == Value:
            html += tab*depth
            html += token.tag.value + '\n'
        elif type(token.tag) == VariableAssign:
            html += tab*depth
            variables[token.tag.identifier] = token.tag.value + '\n'
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