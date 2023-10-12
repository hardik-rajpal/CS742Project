import nltk
from nltk import word_tokenize
from nltk import StanfordTagger, RegexpParser

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

chunker = RegexpParser("""
                    NP: {<DT>?<JJ>*<NN>} #To extract Noun Phrases
                    P: {<IN>}            #To extract Prepositions
                    V: {<V.*>}           #To extract Verbs
                    PP: {<p> <NP>}       #To extract Prepositional Phrases
                    VP: {<V> <NP|PP>*}   #To extract Verb Phrases
                    """)

# Print all parts of speech in above sentence
output = chunker.parse(posTags)
output.draw()