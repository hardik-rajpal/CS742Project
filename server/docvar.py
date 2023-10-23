from paraphraser import Rephraser
import pickle as pkl
import uuid
import random
from docx import Document
SERVER_KEY = 'howard_roark'
class Doc:
    def __init__(self,path,id=None) -> None:
        self.path = path
        self.docdb = None #TODO connect to a sqlite storage of doc path, uuids.
        if(id is None):
            #TODOfetch uuid from sqlite or make entry in sqlite on new uuid.
            id = uuid.UUID(int=random.getrandbits(128)).hex
        self.id = id
class DocVariationsGenerator:
    def __init__(self):
        self.picklepath = 'docvars.pkl'
        self.numphrases = 3
        self.rephraser = None #initialized only if rephrasing function is called
    def loadVariations(self):
        with open(self.picklepath,'rb') as f:
            self.variations = pkl.load(f)
        print('loaded variations:\n',self.variations)
        return self.variations
    def extractSentences(self,doc:Doc):
        msDoc = Document(doc.path)
        paras = msDoc.paragraphs
        result = []
        for para in paras:
            para.text = para.text.strip()
            sents = para.text.split('. ')
            for index in range(len(sents)-1):# -1 to ignore blank end.
                sents[index] = sents[index]+'.'
            result.extend(sents)
        return result
    def generateVariations(self, sentences):
        if(self.rephraser is None):
            self.rephraser = Rephraser()
        return self.rephraser.paraphraseSentences(sentences,self.numphrases,minLength=5)
    def pruneVariations(self,variations):
        #TODO discard sentences that are too far.
        return variations
    def getFullDocVariations(self,doc:Doc):
        sentences = self.extractSentences(doc)
        variations = self.generateVariations(sentences)
        cleanVariations = self.pruneVariations(variations)
        return cleanVariations
    def saveVariations(self,variations,doc:Doc):
        self.loadVariations()
        if(doc.id in self.variations):
            self.variations[doc.id]['variations'] = variations
        else:
            self.variations[doc.id] = {
                'path':doc.path,
                'variations':variations
            }
        with open(self.picklepath,'wb') as f:
            pkl.dump(self.variations,f)
    def hashVariation(self,sentences):
        hashString = ''
        for sentence in sentences:
            hashString += hash(sentence)
        return hash(hashString+SERVER_KEY) # hmac because....
    def writePDF(self,sentences,name):
        pass
if __name__ == '__main__':
    random.seed(0) # reproducible UUIDs until db is setup.
    dvg = DocVariationsGenerator()
    doc:Doc = Doc('test.docx')
    # cleanVariations = dvg.getFullDocVariations(doc)
    # dvg.saveVariations(cleanVariations,doc)
    dvg.loadVariations()