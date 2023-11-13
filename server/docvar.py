from paraphraser import Rephraser
import pickle as pkl
import uuid
import random
from docx2pdf import convert
from docx import Document
import math
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
    # def loadVariations(self):
    #     with open(self.picklepath,'rb') as f:
    #         self.variations = pkl.load(f)
    #     print('loaded variations:\n',self.variations)
    #     return self.variations
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
    def getCapacity(self,variations):
        capacity = 1
        for sentOptions in variations:
            capacity *= len(sentOptions)
        capacity = math.log2(capacity)
        return capacity#bits storeable in variations.
    def generateVariations(self, sentences):
        if(self.rephraser is None):
            self.rephraser = Rephraser()
        variations = self.rephraser.paraphraseSentences(sentences,self.numphrases,minLength=5)
        return variations
    def pruneVariations(self,variations):
        #TODO discard sentences that are too far.
        return variations
    def getFullDocVariations(self,doc:Doc):
        sentences = self.extractSentences(doc)
        variations = self.generateVariations(sentences)
        cleanVariations = self.pruneVariations(variations)
        return cleanVariations
    
    def writePDF(self,sentences,name):
        # sents to docx.
        # try applying style.
        # to pdf.
        # use ghostscript
        pass
        # convert("input.docx")
        # convert("input.docx", "output.pdf")
        # convert("my_docx_folder/")
    def multibaseEncode(self,bases,message):
        ans = [0]*(len(bases)-1)
        for i in range(len(bases)-2,-1,-1):
            b = bases[i]
            ans[i] = math.floor(message/b)
            message = message - ans[i]*b
        return ans
    def encodeIntoDoc(self,doc,message):
        cleanVariations = dvg.getFullDocVariations(doc)
        response = {
            "success":False
        }
        offsets = [1]
        for sentenceOptions in cleanVariations:
            offsets.append(len(sentenceOptions)*offsets[-1])
        capacity = offsets[-1] # last offset.
        if(message > capacity):
            response["error"] = f"Message (${message}) exceeds capacity (${capacity})."
            return response
        #message <= capacity
        answer = ""
        indices = self.multibaseEncode(offsets,message)
        for index,sentenceOptions in zip(indices,cleanVariations):
            answer += sentenceOptions[index] + " "
        return answer
if __name__ == '__main__':
    random.seed(0) # reproducible UUIDs until db is setup.
    dvg = DocVariationsGenerator()
    doc:Doc = Doc('test.docx')
    message = 10
    # dvg.encodeIntoDoc(doc,10)

    
    # dvg.saveVariations(cleanVariations,doc)