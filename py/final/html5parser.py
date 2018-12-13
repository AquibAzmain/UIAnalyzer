from html5lib.tokenizer import HTMLTokenizer
from html5lib.constants import tokenTypes, voidElements
from io import StringIO


all = ['HTML5Parser']


class HTML5Parser(object):
    def __init__(self):
        self.reset()

    def reset(self):
        self.src = StringIO()
        self.tokenizer = HTMLTokenizer(self.src)

    def feed(self, txt):
        pos = self.src.tell()
        self.src.write(txt)
        self.src.seek(pos)
        self._handle_tokens()

    def getpos(self):
        return self.tokenizer.stream.position() 

    def close(self):
        self._handle_tokens()
        self.src.close()

    def _handle_tokens(self):
        for token in self.tokenizer:
            if token['type'] == tokenTypes['EndTag']:
                self.handle_endtag(token['name'])
            elif token['type'] == tokenTypes['StartTag']:
                if token['name'] in voidElements:
                    self.handle_startendtag(token['name'], token['data'])
                else:
                    self.handle_starttag(token['name'], token['data'])
            elif token['type'] == tokenTypes['EmptyTag']:
                self.handle_startendtag(token['name'], token['data'])
            elif token['type'] == tokenTypes['Characters']:
                self.handle_data(token['data'])
            elif token['type'] == tokenTypes['Comment']:
                self.handle_comment(token['data'])
            elif token['type'] == tokenTypes['Doctype']:
                self.handle_decl(token['name'])
            elif token['type'] == tokenTypes['ParseError']:
                self.unknown_decl(token['data'])

    def handle_starttag(self, tag, attrs):
        pass

    def handle_endtag(self, tag):
        pass

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        self.handle_endtag(tag)

    def handle_data(self, data):
        pass

    def handle_comment(self, data):
        pass

    def handle_decl(self, decl):
        pass

    def unknown_decl(self, data):
        pass