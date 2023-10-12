import nltk
from nltk import word_tokenize
from nltk import StanfordTagger, RegexpParser, RecursiveDescentParser

class SyntaxTree:
    def getTree(self,text:str):
        #returns tree.
        pass
    def encodeMessageInTree(self,tree,message):
        # returns tree with message encoded in it.
        pass
    def getText(self,tree)->str:
        #returns text from tree.
        pass
textTok = nltk.word_tokenize('The man looks for the fox.')
posTags = nltk.pos_tag(textTok)
nltk.parse.CoreNLPParser()
grammar = nltk.CFG.fromstring()
rdParser = RecursiveDescentParser(grammar)

# Print all parts of speech in above sentence