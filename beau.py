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
    props: list[(str, str)]

@dataclass
class Prop:
    name: str

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
            if t.type == 0:
                if len(t.props) == 0: 
                    html += "<{}>".format(t.tag)
                else:
                    props = ""
                    for p in t.props:
                        props += " " + p[0] + "=\""+ p[1] + "\""
                    html += "<{}".format(t.tag) + props + ">"
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
    Dash = '-'
    Dot = '.'
    Colon = ':' 
    SemiColon = ';'
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

def parse_props(syntax_tokens, index):
    props = []
    while index < len(syntax_tokens):
        prop_name = syntax_tokens[index]
        if prop_name.type is not SyntaxTokenTypes.Word:
            return props, index 
        index += 1
        if syntax_tokens[index].type is not SyntaxTokenTypes.Assign:
            print("[ERROR] Expected a '=' at name")
            quit()
        index += 1
        if syntax_tokens[index].type is not SyntaxTokenTypes.DoubleQuote:
            print("[ERROR] Expected a '\"' at name")
            quit()
        index += 1
        value = ""
        while syntax_tokens[index].type is SyntaxTokenTypes.Word or syntax_tokens[index].type is SyntaxTokenTypes.Colon or syntax_tokens[index].type is SyntaxTokenTypes.Slash or syntax_tokens[index].type is SyntaxTokenTypes.Dot or syntax_tokens[index].type is SyntaxTokenTypes.SemiColon or syntax_tokens[index].type is SyntaxTokenTypes.Dash:
            value += syntax_tokens[index].literal
            index += 1
        if syntax_tokens[index].type is not SyntaxTokenTypes.DoubleQuote:
            print("[ERROR] Expected a '\"', got: {}".format(syntax_tokens[index].literal))
            quit()
        props.append((prop_name.literal, value))
        index += 1
            
    return props, index

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
                    print("[ERROR] Next type should be a tag")
                    quit()
                if tag.type == SyntaxTokenTypes.Var:
                    i += 1
                    if is_closing:
                        print("[ERROR] Variable declaration tag cannot be a closing one")
                        quit()
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
                    tag = syntax_tokens[i]
                    i += 1
                    props, i = parse_props(syntax_tokens, i) 
                    if syntax_tokens[i].type is not SyntaxTokenTypes.AngleBracketRight:
                        print("[ERROR] Expected a '>', got: '{}'".format(tag.literal))
                        quit()
                    if is_closing:
                        tokens.append(Token(NativeTag(tag.literal, 1, props)))
                    else:
                        tokens.append(Token(NativeTag(tag.literal, 0, props)))
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
                print("[ERROR] Character: '{}', is not supported in this context".format(current.literal))
                quit()
        i += 1
    return tokens

def tokenize_beau(input):
    syntax_tokens = []
    i = 0
    while i < len(input):
        char = input[i]
        #print(char)
        match char:
            case '<':
                syntax_tokens.append(SyntaxToken(SyntaxTokenTypes.AngleBracketLeft, char))
            case '>':
                syntax_tokens.append(SyntaxToken(SyntaxTokenTypes.AngleBracketRight, char))
            case '/':
                syntax_tokens.append(SyntaxToken(SyntaxTokenTypes.Slash, char))
            case '=':
                syntax_tokens.append(SyntaxToken(SyntaxTokenTypes.Assign, char))  
            case '-':
                syntax_tokens.append(SyntaxToken(SyntaxTokenTypes.Dash, char))                   
            case '"':
                syntax_tokens.append(SyntaxToken(SyntaxTokenTypes.DoubleQuote, char))    
            case '[':
                syntax_tokens.append(SyntaxToken(SyntaxTokenTypes.SquareBracketLeft, char))
            case ']':
                syntax_tokens.append(SyntaxToken(SyntaxTokenTypes.SquareBracketRight, char))
            case '.':
                syntax_tokens.append(SyntaxToken(SyntaxTokenTypes.Dot, char))
            case ':':
                syntax_tokens.append(SyntaxToken(SyntaxTokenTypes.Colon, char))
            case ';':
                syntax_tokens.append(SyntaxToken(SyntaxTokenTypes.SemiColon, char))
            case _:
                if input[i] != " ":
                    word = ""
                    while input[i].isalnum() or input[i] == '_':
                        word += input[i]
                        if not input[i + 1].isalnum() and input[i + 1] != '_':
                            break
                        else:
                            i += 1
                    if word == "var":
                        syntax_tokens.append(SyntaxToken(SyntaxTokenTypes.Var, word))
                    else:
                        syntax_tokens.append(SyntaxToken(SyntaxTokenTypes.Word, word))
        i += 1
    return syntax_tokens

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
        if filename.split('.')[-1] != " beau":
            print("[ERROR] File should end with '. beau'")
            quit()
        main(sys.argv[1])