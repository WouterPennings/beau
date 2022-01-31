import sys
from dataclasses import dataclass
from enum import Enum, auto
import webbrowser

class ValueType(Enum):
    String = auto()
    Integer = auto()

@dataclass
class NativeTag:
    tag: str
    type: int # 0 = Start, 1 = End, 2 = Void

@dataclass
class Value:
    value: str
    type: ValueType

@dataclass
class VariableIndex:
    identifier: str

@dataclass
class VariableAssign:
    identifier: str   
    value: str 

@dataclass
class Token:
    tag: any

def compile_to_html(tokens):
    variables = {}
    html = ""
    for token in tokens:
        if type(token.tag) == NativeTag:
            t = token.tag
            if t.type == 0: html += "<{}>".format(t.tag)
            else: html += "</{}>".format(t.tag)
        elif type(token.tag) == Value:
            html += token.tag.value
        elif type(token.tag) == VariableAssign:
            if token.tag.identifier in variables:
                print("[WARNING] Variable with the same name has already been created")
            variables[token.tag.identifier] = token.tag.value
        elif type(token.tag == VariableIndex):
            if not token.tag.identifier in variables:
                print("[ERROR] Variable named: '{}', does not exist yet".format(token.tag.identifier))
                quit()
            html += variables[token.tag.identifier]
    return html

class SyntaxTokenTypes(Enum):
    AngleBracketLeft = '<'
    AngleBracketRight = '>'
    Slash = '/'
    Assign = '='
    DoubleQuote = '"'
    SquareBracketLeft = '['
    SquareBracketRight = ']'
    Var = "var"
    Word = "value" # This can be a tag or a piece of text

@dataclass
class SyntaxToken:
    type: SyntaxTokenTypes
    literal: str

def tokenize_beau(input):
    syntax_tokens = []
    i = 0
    while i < len(input):
        char = input[i]
        match char:
            case '<':
                syntax_tokens.append(SyntaxToken(SyntaxTokenTypes.AngleBracketLeft, char))
            case '>':
                syntax_tokens.append(SyntaxToken(SyntaxTokenTypes.AngleBracketRight, char))
            case '/':
                syntax_tokens.append(SyntaxToken(SyntaxTokenTypes.Slash, char))
            case '=':
                syntax_tokens.append(SyntaxToken(SyntaxTokenTypes.Assign, char))                   
            case '"':
                syntax_tokens.append(SyntaxToken(SyntaxTokenTypes.DoubleQuote, char))    
            case '[':
                syntax_tokens.append(SyntaxToken(SyntaxTokenTypes.SquareBracketLeft, char))
            case ']':
                syntax_tokens.append(SyntaxToken(SyntaxTokenTypes.SquareBracketRight, char))
            case _:
                if input[i] != " ":
                    word = ""
                    while input[i].isalnum():
                        word += input[i]
                        if not input[i + 1].isalnum():
                            break
                        else:
                            i += 1
                    if word == "var":
                        syntax_tokens.append(SyntaxToken(SyntaxTokenTypes.Var, word))
                    else:
                        syntax_tokens.append(SyntaxToken(SyntaxTokenTypes.Word, word))
        i += 1

    return syntax_tokens

def parse_beau(syntax_tokens):
    tokens = []

    i = 0
    while i < len(syntax_tokens):
        current = syntax_tokens[i]
        match current.type:
            case SyntaxTokenTypes.AngleBracketLeft:
                i += 1
                tag = syntax_tokens[i]
                is_closing = tag.type == SyntaxTokenTypes.Slash;
                if is_closing:
                    i += 1
                    tag = syntax_tokens[i]
                if tag.type != SyntaxTokenTypes.Var and tag.type != SyntaxTokenTypes.Word:
                    print(tag.type)
                    print("[ERROR] Next type should be a tag")
                    quit()
                i += 1
                if tag.type == SyntaxTokenTypes.Var:
                    if is_closing:
                        print("[ERROR] Variable declaration tag cannot be a closing one")
                    x = syntax_tokens[i]
                    if x.type is not SyntaxTokenTypes.Word and x.literal != "name":
                        print("[ERROR] Next token should be name")
                        quit()
                    i += 1
                    if syntax_tokens[i].type is not SyntaxTokenTypes.Assign:
                        print("[ERROR] Expected a '=' at name")
                        quit()
                    i += 1
                    if syntax_tokens[i].type is not SyntaxTokenTypes.DoubleQuote:
                        print("[ERROR] Expected a '\"' at name")
                        quit()
                    i += 1
                    name = syntax_tokens[i]
                    if name.type is not SyntaxTokenTypes.Word:
                        print("[ERROR] Expected a identifier for the variable")
                        quit() 
                    i += 1
                    if syntax_tokens[i].type is not SyntaxTokenTypes.DoubleQuote:
                        print("[ERROR] Expected a '\"' at value")
                        quit()
                    i += 1
                    x = syntax_tokens[i]
                    if x.type is not SyntaxTokenTypes.Word and x.literal != "value":
                        print("[ERROR] Next token should be \"value\"")
                        quit()
                    i += 1    
                    if syntax_tokens[i].type is not SyntaxTokenTypes.Assign:
                        print("[ERROR] Expected a '=' at name")
                        quit()
                    i += 1                
                    if syntax_tokens[i].type is not SyntaxTokenTypes.DoubleQuote:
                        print("[ERROR] Expected a '\"'")
                        quit()
                    i += 1
                    value = syntax_tokens[i]
                    if value.type is not SyntaxTokenTypes.Word:
                        print("[ERROR] Expected a value for the variable")
                        quit() 
                    i += 1
                    if syntax_tokens[i].type is not SyntaxTokenTypes.DoubleQuote:
                        print("[ERROR] Expected a '\"'")
                        quit()
                    i += 1 
                    if syntax_tokens[i].type is not SyntaxTokenTypes.Slash:
                        print("[ERROR] Expected a '/'")
                        quit()
                    i += 1     
                    if syntax_tokens[i].type is not SyntaxTokenTypes.AngleBracketRight:
                        print("[ERROR] Expected a '>'")
                        quit()
                    tokens.append(Token(VariableAssign(name.literal, value.literal))) 
                else:
                    tag = syntax_tokens[i - 1].literal    
                    if syntax_tokens[i].type is not SyntaxTokenTypes.AngleBracketRight:
                        print("[ERROR] Expected a '>'")
                        quit()
                    if is_closing:
                        tokens.append(Token(NativeTag(tag, 1)))
                    else:
                        tokens.append(Token(NativeTag(tag, 0)))
            case SyntaxTokenTypes.Word:
                tokens.append(Token(Value(syntax_tokens[i].literal, ValueType.String)))
            case SyntaxTokenTypes.SquareBracketLeft:
                i += 1
                if syntax_tokens[i].type is not SyntaxTokenTypes.Word:
                    print("[ERROR] Expected a variable name")
                    quit()
                name = syntax_tokens[i].literal
                i += 1
                if syntax_tokens[i].type is not SyntaxTokenTypes.SquareBracketRight:
                    print("[ERROR] Expected a square right bracket")
                    quit()
                tokens.append(Token(VariableIndex(name)))
            case _:
                print("[ERROR] Got a character this is not supported in this context")
        i += 1
    
    return tokens

def save_file(name, content):
    f = open(name, "w")
    f.write(content)
    f.close()

def main(filename: str):
    with open(filename, 'r') as file:
        input = file.read().rstrip()

    syntax_tokens = tokenize_beau(input)
    tags = parse_beau(syntax_tokens)

    html = compile_to_html(tags)
    save_file("index.html", html)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("[ERROR] You did not supply enough arguments")
        print("[INFO] To execute type: 'py ./beau.py <FILENAME>. beau'")
    elif len(sys.argv) > 2:
        print("[ERROR] You supplied too many arguments")
        print("[INFO] To execute type: 'py ./beau.py <FILENAME>. beau'")
        webbrowser.open("https://stackoverflow.com/search?q=spaces+in+path&s=00765823-f25b-46bf-a749-53aed287d501")
    else:
        filename = sys.argv[1]
        if filename.split('.')[-1] != "beau script":
            print("[ERROR] File should end with '. beau'")
            quit()
        main(sys.argv[1])