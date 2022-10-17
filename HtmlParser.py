import re

class Token:
    def __init__(self, value, tag, indentLevel):
        self.value = value
        self.tag = tag
        self.indentLevel = indentLevel

class Analyzer:
    tokenStarts = ("<body>", "<b>", "<i>", "<ul>", "<li>")
    possibleList = False
    def error():
        raise Exception("Syntax error: expecting expected-token-category; saw token")
        return Token("Invalid", "Invalid", 0)
    def anymoreTokens(self, text):
        result = re.search(r"<[^/]", text)
        result2 = re.search(r"[\s>][^<\s]", text)
        if(result == None and result2 == None):
            return False
        return True
    def nextToken(self, token, text):
        # Shrinks text and defines a new search area
        if(token.tag == "text"):
            text = text[len(token.value): ]
        else:
            text = text[len(token.tag): ]
        # Finds the next non whitespace character
        result = re.search(r"(?=[^\s])", text)
        if(result != None):
            if(result.string[0:1] == " "):
                firstChar = result.string[1:2]
            else:
                firstChar = result.string[0:1]
            # Checks if the next input is a tag
            if(firstChar == "<"):
                # Creates a string of the tag
                end = re.search(">", text)
                if(end == None):
                    Analyzer.error()
                else:
                    tag = text[result.span()[0]: end.span()[0] + 1]
                # Compares the tag to all legalTags to make sure input is legal
                for i in Analyzer.tokenStarts:
                    endTag = ("</" + i[1: ])
                    if(tag == i):
                        if(tag == "<li>" and (token.tag == "<ul>" or Analyzer.possibleList)):
                            Analyzer.possibleList = True
                        elif(tag == "<li>"):
                            Analyzer.error()
                        return( (Token(tag, tag, token.indentLevel + 1), text) )
                    elif(tag == endTag):
                        if(result == "</ul>"):
                            Analyzer.possibleList = False
                        if(Analyzer.anymoreTokens(self, text)):
                            Analyzer.nextToken(self, Token(tag, "text", token.indentLevel), text)
                        else:
                            return ( (Token("EOI", "EOI", 0), text) )
                # Raises exception if not legal tag
            # Handles if next input is text
            else:
                end = re.search("<", text)
                if(end == None):
                    Analyzer.error()
                else:
                    value = text[result.span()[0]: end.span()[0]]
                    return( (Token(value, "text", token.indentLevel), text) ) 
        else:
            return ( (Token("EOI", "EOI", 0), text) )
        return ( (Token("EOI", "EOI", 0), text) )
        
class Parser:
    def __init__(self, text):
        self.text = text
        self.analyzer = Analyzer
    def printHtmlTree(self, token):
        # Makes sure the initial text fits the starting token and converts it into one
        if(token == None):
            openingTag = re.search("<body>", self.text)
            if(openingTag != None):
                closingTag = re.search("</body>", self.text[openingTag.span()[1] + 1:])
                if(closingTag != None):
                    # Checks if there's anything before or after the body tags as that is illegal
                    if(re.search(r"[^\s]", self.text[0:openingTag.span()[0]]) == None and re.search(r"[^\s]", self.text[closingTag.span()[1] + 7:]) == None):
                        self.text = self.text[openingTag.span()[0]:closingTag.span()[1] + 7]
                        bodyToken = Token("<body>", "<body>", 1)
                        print(bodyToken.tag)
                        nextTok = Analyzer.nextToken(self, bodyToken, self.text)
                        if(nextTok != None):
                            self.text = nextTok[1]
                            self.printHtmlTree(nextTok[0])
                        print("</" + bodyToken.tag[1: ])
                    else:
                        self.error()
                else:
                    self.error()
            else:
                self.error()
        else:
            indent = ""
            indentLevel = 0
            if(token.tag == "text"):
                indentLevel = token.indentLevel
            else:
                indentLevel = token.indentLevel - 1
            for i in range(indentLevel):
                indent = indent + "  "
            nextTok = Analyzer.nextToken(self, token, self.text)
            if(nextTok[0].tag == "Invalid" or nextTok[0].tag == "EOI"):
                return 0
            else:
                self.text = nextTok[1]
                nextTok = nextTok[0]
                if(token.tag == "text"):
                    if(token.value != ">"):
                        print(indent + token.value)
                    self.printHtmlTree(nextTok)
                else:
                    print(indent + token.tag)
                    self.printHtmlTree(nextTok)
                    print(indent + "</" + token.tag[1: ])
    def run(self):
        self.printHtmlTree(None)

parser = Parser("<body> google <b><i><b> yahoo</b></i></b></body>")
parser.run()
                
            

        
