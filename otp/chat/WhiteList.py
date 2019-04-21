from bisect import bisect_left
import string
import sys
import os

class WhiteList:

    def __init__(self, wordlist):
        self.words = []
        for line in wordlist:
            self.words.append(line.strip('\n\r').lower())

        self.words.sort()
        self.numWords = len(self.words)

    def cleanText(self, text):
        text = text.strip('.,?!')
        text = text.lower()
        return text

    def isWord(self, text):
        try:
            text = self.cleanText(text)
            i = bisect_left(self.words, text)
            if i == self.numWords:
                return False
            return self.words[i] == text
        except UnicodeDecodeError:
            return False  # Lets not open ourselves up to obscure keyboards...
      

    def isPrefix(self, text):
        text = self.cleanText(text)
        i = bisect_left(self.words, text)
        if i == self.numWords:
            return False
        return self.words[i].startswith(text)

    def prefixCount(self, text):
        text = self.cleanText(text)
        i = bisect_left(self.words, text)
        j = i
        while j < self.numWords and self.words[j].startswith(text):
            j += 1

        return j - i

    def prefixList(self, text):
        text = self.cleanText(text)
        i = bisect_left(self.words, text)
        j = i
        while j < self.numWords and self.words[j].startswith(text):
            j += 1

        return self.words[i:j]
