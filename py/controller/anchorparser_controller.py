from __future__ import unicode_literals
from html5parser import HTML5Parser
import requests
from bs4 import BeautifulSoup
import json

class AnchorparserController(HTML5Parser):
    tags = []
    def _printpos(self):
        (line, column) = self.getpos()
        return line

    def _printtag(self, tagtype, tag):
        if tag=="a":
            self._printpos()
            return self._printpos()

    def _printattrs(self, attrs):
        if attrs:
            for k, v in attrs:
                if k=="href":
                    return v       

    def handle_starttag(self, tag, attrs):
        if tag=="a":
            self._printtag('StartTag', tag)
            self._printattrs(attrs)
            self.tags.append(self._printtag('StartTag', tag))
            self.tags.append(self._printattrs(attrs))
            return (self._printtag('StartTag', tag), self._printattrs(attrs))

    def handle_endtag(self, tag):
        if tag=="a":
            self._printtag('EndTag', tag)
            self.tags.append(self._printtag('EndTag', tag))
            return self._printtag('EndTag', tag)