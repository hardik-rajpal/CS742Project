from paraphraser import Rephraser
import pickle as pkl
import inspect
import uuid
import random
from docx2pdf import convert
from docx import Document
import math
SERVER_KEY = 'howard_roark'
DEFAULT_DOC_VARS = [
  ["Test Document"],
  [
    "Online Education; it's a curse for some students and a blessing for others.",
    "Online education can be challenging for some students, while it offers convenience and flexibility for others.",
    "Some students find online education to be a burden, while others appreciate its benefits such as flexibility and convenience.",
    "For some students, online education is a curse, while for others, it is a blessing that provides flexibility and convenience."
  ],
  [
    "The part that pleases me the most is the ease with which we can switch classrooms.",
    "The part that I enjoy the most about online education is the ease with which I can switch classrooms, without having to physically move from one location to another.",
    "One of the things that I appreciate the most about online education is the ability to easily switch between classrooms, without having to physically move from one location to another.",
    "The part of online education that I find the most enjoyable is the ease with which I can switch classrooms, without having to physically move from one location to another."
  ],
  [
    "The only way I am gonna be happy if the campus reopens is if the lecture halls are a Chrome tab away.",
    "The only way I will be happy if the campus reopens is if the lecture halls are accessible through a Chrome tab, without having to physically move from one location to another.",
    "If the campus reopens, I will be happiest if the lecture halls are accessible through a Chrome tab, without having to physically move from one location to another.",
    "The only way I can be happy if the campus reopens is if the lecture halls are accessible through a Chrome tab, without having to physically move from one location to another."
  ],
  [
    "The idea of a \"flipped-classroom\" model, where the students watch the pre-recorded lectures before having a live class, really relaxes the time constraints faced in traditional schooling.",
    "The idea of a \"flipped-classroom\" model, where the students watch the pre-recorded lectures before having a live class, really helps to reduce the pressure on students and teachers alike.",
    "The concept of a \"flipped-classroom\" model, where the students watch the pre-recorded lectures before having a live class, is an effective way to manage time constraints in traditional schooling.",
    "The idea of a \"flipped-classroom\" model, where the students watch the pre-recorded lectures before having a live class, really helps to alleviate the pressure on both students and teachers."
  ],
  [
    "As advocated by Sal Khan from Khan Academy, the whole process can become perfection-centred rather than the usual complete-the-syllabus-on-time-centred.",
    "As advocated by Sal Khan from Khan Academy, the whole process of online education can be transformed into a perfection-centered approach, rather than the traditional focus on completing the syllabus within a specific time frame.",
    "The idea of perfection-centered online education, as advocated by Sal Khan from Khan Academy, is an effective way to manage time constraints and promote student engagement in the learning process.",
    "The concept of perfection-centered online education, as advocated by Sal Khan from Khan Academy, is a promising approach that can help students to develop their skills and abilities more effectively."
  ],
  [
    "This fluidity of the schedule permits one to partition their time to maximise their efficiency and clarity in a concept; a point sadly overlooked in the conventional and offline teaching methods.",
    "The fluidity of the online education schedule allows students to partition their time effectively, maximizing their efficiency and clarity in understanding complex concepts.",
    "The flexibility of the online education schedule enables students to manage their time more efficiently and clearly understand complex concepts.",
    "The fluidity of the online education schedule permits students to allocate their time effectively, maximizing their efficiency and clarity in understanding complex concepts."
  ],
  [
    "These ideas being the bright side of the issue; there are screen-sharing mishaps, an absurd absence of a schedule in the lives of the undisciplined students, and loosely proctored quizzes to restore the balance.",
    "The bright side of online education is that it allows for screen-sharing mishaps, an absence of a schedule in the lives of undisciplined students, and loosely proctored quizzes to restore the balance.",
    "The positive aspects of online education include screen-sharing mishaps, an absence of a schedule in the lives of undisciplined students, and loosely proctored quizzes to restore the balance.",
    "The benefits of online education include screen-sharing mishaps, an absence of a schedule in the lives of undisciplined students, and loosely proctored quizzes to restore the balance."
  ],
  [
    "There's no stringent bus driver who's gonna leave you behind if you're not at the stop on time; no way for the teacher to genuinely threaten you for your disrespectful actions."
  ],
  [
    "Teachers have gone from the magicians in their five-star, one-person shows to street performers, begging for the least possible glance of interest at a medieval caf\u00e9."
  ],
  [
    "There's no way they can suspend you, the only useful arrow in their otherwise hollow quavers, for being late to the zoom meeting; why of course, you had connectivity issues, who doesn't when there's a biology class at 8:30 in the morning? Another problem is the access to anonymity on specific platforms (Zoom, at least, when you don't know how to secure a meeting)."
  ]
]
DELIMS = ('.','?','!')
class Doc:
    def __init__(self,path,id=None) -> None:
        self.path = path
        self.docdb = None #TODO connect to a sqlite storage of doc path, uuids.
        if(id is None):
            #TODOfetch uuid from sqlite or make entry in sqlite on new uuid.
            id = uuid.UUID(int=random.getrandbits(128)).hex
        self.id = id
class ParaData:
    def __init__(self,sentCount,style) -> None:
        self.sentCount = sentCount
        self.style = style
def getDataMembers(object):
    members = inspect.getmembers(object)
    members = filter(lambda member:not member[0].startswith('_'),members)
    members = filter(lambda member:not inspect.ismethod(member[1]),members)
    return list(members)
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
        paraSentCount:list[ParaData] = []
        for para in paras:
            paraSentCount.append(ParaData(0,para.style))
            para.text = para.text.strip()
            
            sents = para.text.split('. ')
            if(len(sents[-1].strip())==0):
                sents.pop()
            for index in range(len(sents)-1):# -1 to ignore blank end.
                sents[index] = sents[index]+'.'
            paraSentCount[-1].sentCount = len(sents)
            result.extend(sents)
        return result,paraSentCount
    def injectSentences(self,doc:Doc,sentences,paraSentCount:list[ParaData]):
        msDoc = Document()
        pos = 0
        for paraData in paraSentCount:
            print('sentcount: ',paraData.sentCount,'style: ',paraData.style.name)
            print(getDataMembers(paraData.style.font))
            count = paraData.sentCount
            sents = sentences[pos:pos+count]
            paraText = ''
            if(len(sents)>0):
                paraText = ' '.join(sents)          
            msDoc.add_paragraph(paraText,paraData.style)
            pos += count
        msDoc.save(doc.path)
    def getCapacity(self,variations):
        capacity = 1
        for sentOptions in variations:
            capacity *= len(sentOptions)
        capacity = math.log2(capacity)
        return capacity#bits storeable in variations.
    def generateVariations(self, sentences,useDefaultVars=False):
        if(useDefaultVars):
            return DEFAULT_DOC_VARS
        if(self.rephraser is None):
            self.rephraser = Rephraser()
        variations = self.rephraser.paraphraseSentences(sentences,self.numphrases,minLength=5)
        return variations
    def pruneVariations(self,variations:list[list[str]]):
        for options in variations:
            if(len(options)>1):
                for i in range(1,len(options)):
                    delim = options[0][-1]
                    if(options[i][-1]!=delim):
                        if(options[i][-1] in DELIMS):
                            options[i][-1] = delim
                        else:
                            options[i]+=delim
        #TODO discard sentences that are too far.
        return variations
    def getFullDocVariations(self,doc:Doc):
        sentences,paraSentCount = self.extractSentences(doc)
        variations = self.generateVariations(sentences,True) # set to true to bypass GPT running locally.
        cleanVariations = self.pruneVariations(variations)
        return cleanVariations,paraSentCount
    
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
            if(message==0):
                break
        return ans
    def multibaseDecode(self,bases,indices):
        ans = 0
        for (index,base) in zip(indices,bases):
            ans += base*index
        return ans
    def getOffsets(self,cleanVars):
        offsets = [1]
        for sentenceOptions in cleanVars:
            offsets.append(len(sentenceOptions)*offsets[-1])
        return offsets
    def encodeIntoDoc(self,doc,message,outputFname='output.docx'):
        cleanVariations,paraSentCount = self.getFullDocVariations(doc)
        response = {
            "success":False
        }
        offsets = self.getOffsets(cleanVariations)
        capacity = offsets[-1] # last offset.
        if(message > capacity):
            response["error"] = f"Message (${message}) exceeds capacity (${capacity})."
            return response
        #message <= capacity
        indices = self.multibaseEncode(offsets,message)
        outputSentences=[]
        for index,sentenceOptions in zip(indices,cleanVariations):
            outputSentences.append(sentenceOptions[index])
        outputDoc = Doc(outputFname)
        self.injectSentences(outputDoc,outputSentences,paraSentCount)
    def decodeFromDoc(self,doc,modContent:str):
        cleanVariations = self.getFullDocVariations(doc)
        sentences = list(map(lambda sent:sent+'.',modContent.split('. ')))
        sentences.pop()
        offsets = self.getOffsets(cleanVariations)
        indices = [0]*len(offsets)
        for i in range(0,len(sentences)):
            try:
                indices[i] = cleanVariations[i].index(sentences[i])
            except:
                # print(cleanVariations[i])
                # print(sentences[i])
                print(cleanVariations[0],cleanVariations[-1])
                print(sentences[0],sentences[-1])
                print(len(cleanVariations),len(sentences))
                return ''
        message = self.multibaseDecode(offsets,indices)
        return message
if __name__ == '__main__':
    # TODO: consider ?,! delimiters.
    random.seed(0) # reproducible UUIDs until db is setup.
    dvg = DocVariationsGenerator()
    outFname = 'output.docx'
    doc:Doc = Doc('test.docx')
    ##Writer: 
    message = 23
    ciphertext = dvg.encodeIntoDoc(doc,message,outFname)

    ## Reader:
    # with open(fname,'r+',encoding='utf-8') as f:
    #     cipher = f.read()
    #     message = dvg.decodeFromDoc(doc,cipher)
    #     print('retrieved message: ',message)