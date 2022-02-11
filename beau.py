import sys
from dataclasses import dataclass
from enum import Enum, auto

class TokenType(Enum):
    Native = auto()             # HTML Tokens: h1, p, iframe, ul
    Value = auto()              # Just a piece of text
    Let = auto()                # Custom Token: declaring variable
    If = auto()
    Else = auto()

@dataclass          
class Attr:            
    Name: any                   # Either a hardcoded string or Value 
    Value: any                  # Either a hardcoded string or Value 
    Op: str                     # Operator is the thing in between the name and the value (class="test")

@dataclass          
class Native:           
    Literal: str            
    attr_pos: bool              # false=end-tag, true=has-props (Beginning or void tag)
    Attributes: list[Attr]      

@dataclass
class Value:
    Value: str 

@dataclass
class Let:                      # For creating and reading a variable, depends on the props
    Literal: str        
    Attributes: list[Attr]          

@dataclass
class If:                       # If statement 
    Literal: str        
    attr_pos: bool
    Attributes: list[Attr] 

@dataclass
class Else:                     # Else block for if-statement
    Literal: str  
    attr_pos: bool      
    Attributes: list[Attr] 

@dataclass
class Token:
    Type: TokenType
    Tag: any

class Compiler:
    def __init__(self, tokens: list[Token]):
        self.tokens: list[Token] = tokens
        self.current: int = 0
        self.variables: dict

    def next_token(self):
        self.current += 1

    def current_token(self):
        return self.tokens[self.current]

    def compiler_to_html(self):
        html = ""
        while self.current < len(self.tokens):
            html += self.get_html_token()
            self.next_token()
        return html

    def get_html_token(self):
        html = ""
        match self.current_token().Type:
            case TokenType.Native:
                if not self.current_token().Tag.attr_pos:
                    html += "</{}>".format(self.current_token().Tag.Literal)
                else:
                    attr = " "
                    for a in self.current_token().Tag.Attributes:
                        attr += a.Name + a.Op + a.Value + " "
                    html += "<{} {}>".format(self.current_token().Tag.Literal, attr)
            case TokenType.Value:
                html += self.current_token().Tag.Value
            case TokenType.Let:
                attributes = self.current_token().Tag.Attributes
                allowed_attributes = ["name", "value"]
                for a in attributes:
                    if not a.Name in allowed_attributes:
                        self.throw_error("The attribute with the name: {}, is not known in this context".format(a.Name))
                if len(self.current_token().Tag.Attributes) == 2:
                    if attributes[0].Value in self.variables:
                        print("[ BEAU WARNING] Variable with the same name has already been created")
                    # if not attributes[0].Value.isupper():
                    #     self.throw_error("The variable name: {}, should be all uppercase".format(attributes[0].Value))
                    self.variables[attributes[0].Value] = attributes[1].Value[1:-1]
                elif len(attributes) == 1:
                    if not attributes[0].Name == "name" and attributes[0].Value == "": 
                        self.throw_error("You have a attribute without a name")
                    if attributes[0].Value == "":
                        self.throw_error("You called a variable with a name without any characters")
                    elif not attributes[0].Value in self.variables:
                        self.throw_error("You called '{}', but that does not exist".format(attributes[0].Value[1:-1]))
                    else:
                        html += self.variables[attributes[0].Value]
                else:
                    self.throw_error("You have supplied: {} attributes, but '{}' can only take a max of 2".format(len(attributes), self.current_token().Tag.Literal))
            case TokenType.If:
                if self.current_token().Tag.attr_pos:
                    attributes = self.current_token().Tag.Attributes
                    allowed_attributes = ["left", "right", "op"]
                    for a in attributes:
                        if not a.Name in allowed_attributes:
                            self.throw_error("The attribute with the name: {}, is not known in this context".format(a.Name))
                    if not self.eval_comparison(int(self.current_token().Tag.Attributes[0].Value[1:-1]), self.current_token().Tag.Attributes[1].Value[1:-1], int(self.current_token().Tag.Attributes[2].Value[1:-1])):
                        while True:
                            self.next_token()
                            if self.current_token().Type == TokenType.If:
                                if not self.current_token().Tag.attr_pos:
                                    self.current -= 1
                                    break
                    else:
                        while True:
                            self.next_token()
                            if self.current_token().Type == TokenType.If:
                                if not self.current_token().Tag.attr_pos:
                                    self.current -= 1
                                    break
                            html += self.get_html_token()    
        return html
        
    def eval_comparison(self, left: int, op: str, right: int):
        match op:
            case 'equals':
                return (left == right)
            case 'greater':
                return (left > right)
            case 'smaller':
                return (left < right)
            case _:
                self.throw_error("Operator chosen for comparison is not implemented")
    
    def throw_error(self, text):
        print("[ BEAU ERROR] {}".format(text))
        quit() 

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

    def prev_character(self):
        if self.index > 0: 
            self.index -= 1
        else: self.index = 0
        self.current_char = self.input[self.index - 1]
        self.prev_char = self.input[self.index - 2]

    def parse(self):
        syntax_tokens: list[Token] = []
        current_literal: str = ""
        while self.index < len(self.input):
            current_literal = self.current_char
            match self.current_char:
                case '<':
                    self.next_character()
                    if self.current_char == '\\':       
                        # ToDo: Fix this                                            
                        current_literal += self.get_until(['<'])
                        syntax_tokens.append(Token(TokenType.Value, Value(current_literal)))
                    elif self.current_char == '/':                                                  
                        current_literal = self.get_until(['>'])
                        match current_literal:
                            case "if": syntax_tokens.append(Token(TokenType.If, If(tag, False, [])))
                            case "else": syntax_tokens.append(Token(TokenType.Else, Else(tag, False, [])))
                            case _: syntax_tokens.append(Token(TokenType.Native, Native(current_literal[0:], False, [])))
                    else:                                                                            
                        current_literal = self.current_char + self.get_until(['/', '>']) 
                        tag, index = self.get_tag(current_literal)
                        attributes = self.get_attributes(current_literal[index:].strip())
                        match tag:
                            case "let": syntax_tokens.append(Token(TokenType.Let, Let(tag, attributes)))
                            case "if": syntax_tokens.append(Token(TokenType.If, If(tag, True, attributes)))
                            case "else": syntax_tokens.append(Token(TokenType.Else, Else(tag, True, attributes)))
                            case _ : syntax_tokens.append(Token(TokenType.Native, Native(tag, True, attributes)))
                case _:
                    text = self.input[self.index - 1] + self.current_char + self.get_until(['<'])
                    syntax_tokens.append(Token(TokenType.Value, Value(text)))  
                    self.prev_character()   
                    self.prev_character()      
            self.next_character() 
        return syntax_tokens

    def get_until(self, chars: list[str]) -> str:
        self.next_character()
        string = ""
        while not self.current_char in chars and self.current_char is not None:
            string += self.current_char
            self.next_character()
        self.next_character()
        return string

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
                if prop_text[i] == "\"" or prop_text[i] == "'" :
                    value += prop_text[i]
                    break
            n = None
            v = None
            if name.isupper(): n = Let("let", [("name", "=", name)])
            else: n = name
            if value.isupper(): v = Let("let", [("name", "=", value)])
            else: v = value
            props.append(Attr(n, v, op))
            i += 2 # Do not know exacly why plus two is the thing, but it works
        return props

    def get_tag(self, literal: str):
        word = ""
        for index, char in enumerate(literal):
            if char == ' ':
                return word, index
            else: word += char
        return word, len(literal)

def save_file(name, content):
    f = open(name, "w")
    f.write(content)
    f.close()

def main(filename: str):
    with open(filename, 'r') as file:
        input = file.read().rstrip()

    p = Parser(input)
    result = p.parse()
    # for r in result:
    #     print(r)
    c = Compiler(result)
    save_file('./{}.html'.format(filename.split('.')[1]), c.compiler_to_html())
    print("[SUCCES] Compiled to native html at: '.{}.html'".format(filename.split('.')[1]))

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("[ERROR] You did not supply enough arguments")
        print("[INFO] To execute type: 'py ./beau.py <FILENAME>. beau'")
    elif len(sys.argv) > 2:
        print("[ERROR] You supplied too many arguments")
        print("[INFO] To execute type: 'py ./beau.py <FILENAME>. beau'")
    else:
        filename = sys.argv[1]
        if filename.split('.')[-1] != " beau":
            print("[ERROR] File should end with '. beau'")
            quit()
        main(sys.argv[1])