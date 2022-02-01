import re
import sys
from dataclasses import dataclass
from enum import Enum, auto
from tkinter import Variable
from typing import Literal
import webbrowser

# class ValueType(Enum):
#     String = auto()
#     Integer = auto()

# @dataclass
# class NativeTag:
#     tag: str
#     type: int # 0 = Start, 1 = End, 2 = Void
#     props: list[(str, str)]

# @dataclass
# class Prop:
#     name: str

# @dataclass
# class Value:
#     value: str
#     type: ValueType

# @dataclass
# class VariableIndex:
#     identifier: str

# @dataclass
# class VariableAssign:
#     identifier: str   
#     value: str 

# @dataclass
# class Token:
#     tag: any

# def compile_to_html(tokens):
#     variables = {}
#     html = ""
#     for token in tokens:
#         if type(token.tag) == NativeTag:
#             t = token.tag
#             if t.type == 0:
#                 if len(t.props) == 0: 
#                     html += "<{}>".format(t.tag)
#                 else:
#                     props = ""
#                     for p in t.props:
#                         props += " " + p[0] + "=\""+ p[1] + "\""
#                     html += "<{}".format(t.tag) + props + ">"
#             else: html += "</{}>".format(t.tag)
#         elif type(token.tag) == Value:
#             html += token.tag.value
#         elif type(token.tag) == VariableAssign:
#             if token.tag.identifier in variables:
#                 print("[WARNING] Variable with the same name has already been created")
#             variables[token.tag.identifier] = token.tag.value
#         elif type(token.tag == VariableIndex):
#             if not token.tag.identifier in variables:
#                 print("[ERROR] Variable named: '{}', does not exist yet".format(token.tag.identifier))
#                 quit()
#             html += variables[token.tag.identifier]
#     return html

# class SyntaxTokenTypes(Enum):
#     AngleBracketLeft = '<'
#     AngleBracketRight = '>'
#     ClosingSymbol = '</'
#     Slash = '/'
#     Dash = '-'
#     Dot = '.'
#     Colon = ':' 
#     SemiColon = ';'
#     Assign = '='
#     DoubleQuote = '"'
#     SquareBracketLeft = '['
#     SquareBracketRight = ']'
#     Var = "let"
#     Word = "value" # This can be a tag or a piece of text

# @dataclass
# class SyntaxToken:
#     type: SyntaxTokenTypes
#     literal: str

# def parse_props(syntax_tokens, index):
#     props = []
#     while index < len(syntax_tokens):
#         prop_name = syntax_tokens[index]
#         if prop_name.type is not SyntaxTokenTypes.Word:
#             return props, index 
#         index += 1
#         if syntax_tokens[index].type is not SyntaxTokenTypes.Assign:
#             print("[ERROR] Expected a '=' at name")
#             quit()
#         index += 1
#         if syntax_tokens[index].type is not SyntaxTokenTypes.DoubleQuote:
#             print("[ERROR] Expected a '\"' at name")
#             quit()
#         index += 1
#         value = ""
#         while syntax_tokens[index].type is SyntaxTokenTypes.Word or syntax_tokens[index].type is SyntaxTokenTypes.Colon or syntax_tokens[index].type is SyntaxTokenTypes.Slash or syntax_tokens[index].type is SyntaxTokenTypes.Dot or syntax_tokens[index].type is SyntaxTokenTypes.SemiColon or syntax_tokens[index].type is SyntaxTokenTypes.Dash:
#             value += syntax_tokens[index].literal
#             index += 1
#         if syntax_tokens[index].type is not SyntaxTokenTypes.DoubleQuote:
#             print("[ERROR] Expected a '\"', got: {}".format(syntax_tokens[index].literal))
#             quit()
#         props.append((prop_name.literal, value))
#         index += 1
            
#     return props, index

# def parse_beau(syntax_tokens):
#     tokens = []
#     i = 0
#     while i < len(syntax_tokens):
#         current = syntax_tokens[i]
#         match current.type:
#             case SyntaxTokenTypes.AngleBracketLeft:
#                 i += 1
#                 tag = syntax_tokens[i]
#                 is_closing = tag.type == SyntaxTokenTypes.Slash;
#                 if is_closing:
#                     i += 1
#                     tag = syntax_tokens[i]
#                 if tag.type != SyntaxTokenTypes.Var and tag.type != SyntaxTokenTypes.Word:
#                     print("[ERROR] Next type should be a tag")
#                     quit()
#                 if tag.type == SyntaxTokenTypes.Var:
#                     i += 1
#                     if is_closing:
#                         print("[ERROR] Variable declaration tag cannot be a closing one")
#                         quit()
#                     x = syntax_tokens[i]
#                     if x.type is not SyntaxTokenTypes.Word and x.literal != "name":
#                         print("[ERROR] Next token should be name")
#                         quit()
#                     i += 1
#                     if syntax_tokens[i].type is not SyntaxTokenTypes.Assign:
#                         print("[ERROR] Expected a '=' at name")
#                         quit()
#                     i += 1
#                     if syntax_tokens[i].type is not SyntaxTokenTypes.DoubleQuote:
#                         print("[ERROR] Expected a '\"' at name")
#                         quit()
#                     i += 1
#                     name = syntax_tokens[i]
#                     if name.type is not SyntaxTokenTypes.Word:
#                         print("[ERROR] Expected a identifier for the variable")
#                         quit() 
#                     i += 1
#                     if syntax_tokens[i].type is not SyntaxTokenTypes.DoubleQuote:
#                         print("[ERROR] Expected a '\"' at value")
#                         quit()
#                     i += 1
#                     x = syntax_tokens[i]
#                     if x.type is not SyntaxTokenTypes.Word and x.literal != "value":
#                         print("[ERROR] Next token should be \"value\"")
#                         quit()
#                     i += 1    
#                     if syntax_tokens[i].type is not SyntaxTokenTypes.Assign:
#                         print("[ERROR] Expected a '=' at name")
#                         quit()
#                     i += 1                
#                     if syntax_tokens[i].type is not SyntaxTokenTypes.DoubleQuote:
#                         print("[ERROR] Expected a '\"'")
#                         quit()
#                     i += 1
#                     value = syntax_tokens[i]
#                     if value.type is not SyntaxTokenTypes.Word:
#                         print("[ERROR] Expected a value for the variable")
#                         quit() 
#                     i += 1
#                     if syntax_tokens[i].type is not SyntaxTokenTypes.DoubleQuote:
#                         print("[ERROR] Expected a '\"'")
#                         quit()
#                     i += 1 
#                     if syntax_tokens[i].type is not SyntaxTokenTypes.Slash:
#                         print("[ERROR] Expected a '/'")
#                         quit()
#                     i += 1     
#                     if syntax_tokens[i].type is not SyntaxTokenTypes.AngleBracketRight:
#                         print("[ERROR] Expected a '>'")
#                         quit()
#                     tokens.append(Token(VariableAssign(name.literal, value.literal))) 
#                 else:
#                     tag = syntax_tokens[i]
#                     i += 1
#                     props, i = parse_props(syntax_tokens, i) 
#                     if syntax_tokens[i].type is not SyntaxTokenTypes.AngleBracketRight:
#                         print("[ERROR] Expected a '>', got: '{}'".format(tag.literal))
#                         quit()
#                     if is_closing:
#                         tokens.append(Token(NativeTag(tag.literal, 1, props)))
#                     else:
#                         tokens.append(Token(NativeTag(tag.literal, 0, props)))
#             case SyntaxTokenTypes.Word:
#                 tokens.append(Token(Value(syntax_tokens[i].literal, ValueType.String)))
#             case SyntaxTokenTypes.SquareBracketLeft:
#                 i += 1
#                 if syntax_tokens[i].type is not SyntaxTokenTypes.Word:
#                     print("[ERROR] Expected a variable name")
#                     quit()
#                 name = syntax_tokens[i].literal
#                 i += 1
#                 if syntax_tokens[i].type is not SyntaxTokenTypes.SquareBracketRight:
#                     print("[ERROR] Expected a square right bracket")
#                     quit()
#                 tokens.append(Token(VariableIndex(name)))
#             case _:
#                 print("[ERROR] Character: '{}', is not supported in this context".format(current.literal))
#                 quit()
#         i += 1
#     return tokens

CUSTOM_TAGS = ["let"]

class TokenType(Enum):
    Native = auto()             # HTML Tokens: h1, p, iframe, ul
    Value = auto()              # Just a piece of text
    Let = auto()                # Custom Token: declaring variable
    Read = auto()               # Custom Token: Reading a variable

@dataclass          
class Attr:            
    name: any                   # Either a hardcoded string or Value 
    value: any                  # Either a hardcoded string or Value 
    Op: str                     # Operator is the thing in between the name and the value (class="test")

@dataclass          
class Native:           
    Literal: str            
    Type: bool                  # false=end-tag, true=has-props (Beginning or void tag)
    Attributes: list[Attr]      

@dataclass
class Value:
    Value: str 

@dataclass
class Let:                      # For creating and reading a variable, depends on the props
    Literal: str
    props: list[Attr]          

@dataclass
class Token:
    Type: TokenType
    Tag: any

class Parser:
    def __init__(self, input: str):
        self.input: str = input
        self.index: int = 0
        self.current_char = self.input[self.index]
        self.prev_char: str = ""

    def next_character(self):
        self.prev_char = self.current_char
        self.index += 1
        if self.index >= len(self.input): self.current_char = None
        else: self.current_char = self.input[self.index]

    def rewind_character(self):
        if self.index > 0: self.index -= 1
        self.prev_char = self.input[self.index - 1]
        self.current_char = self.input[self.index]
        
    def parse(self):
        syntax_tokens: list[Token] = []
        current_literal: str = ""
        while self.index < len(self.input):
            current_literal += self.current_char
            match self.current_char:
                case '<':
                    self.next_character()
                    if self.current_char == '\\':                                                  
                        current_literal += self.get_until(['<'])
                        syntax_tokens.append(Token(TokenType.Value, Value(current_literal)))
                    elif self.current_char == '/':                                                  
                        current_literal = self.get_until(['>'])
                        syntax_tokens.append(Token(TokenType.Native, Native(current_literal[0:-1], False, [])))
                    else:                                                                            
                        current_literal = self.current_char + self.get_until(['>', '/']) 
                        tag, index = self.get_tag(current_literal)
                        attributes = self.get_attributes(current_literal[index:].strip())
                        if tag in CUSTOM_TAGS:
                            syntax_tokens.append(Token(TokenType.Let, Let(tag, attributes)))
                        else:
                            syntax_tokens.append(Token(TokenType.Native, Native(tag, True, attributes)))
                case _:
                    syntax_tokens.append(Token(TokenType.Value, Value(self.current_char + self.get_until(['<']))))       
            self.next_character() 
        return syntax_tokens
    
    def get_attributes(self, prop_text):
        props: list[Attr] = []
        i = 0
        while i < len(prop_text):
            name = ""
            while prop_text[i].isalnum():
                name += prop_text[i]
                i += 1
            op = prop_text[i]
            i += 1
            value = ""
            while i < len(prop_text):
                value += prop_text[i]
                i += 1
            n = None
            v = None
            if name.isupper(): n = Let("let", [("name", "=", name)])
            else: n = name
            if value.isupper(): v = Let("let", [("name", "=", value)])
            else: v = value
            props.append(Attr(n, v, op))
            if not i >= len(prop_text):
                while prop_text[i] == ' ': 
                    print(i)
                    i += 1
        return props

    def get_until(self, chars: list[str]) -> str:
        self.next_character()
        string = ""
        while not self.current_char in chars and self.current_char is not None:
            string += self.current_char
            self.next_character()
        self.next_character()
        return string

    def get_tag(self, literal: str):
        word = ""
        for index, char in enumerate(literal):
            if char == ' ':
                return word, index
            else: word += char

def save_file(name, content):
    f = open(name, "w")
    f.write(content)
    f.close()

def main(filename: str):
    with open(filename, 'r') as file:
        input = file.read().rstrip()

    p = Parser(input)
    result = p.parse()
    for r in result:
        print(r)

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