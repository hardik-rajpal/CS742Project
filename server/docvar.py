from paraphraser import Rephraser
import zlib
import re
import inspect
import uuid
import random
from docx2pdf import convert
from docx import Document
import math
import spacy
import argparse
SIMILARITY_THRESHOLD=0.8
SERVER_KEY = 'howard_roark'
DEFAULT_DOC_VARS = [
  ["Test Document"],
  [
    "Online Education; it\u2019s a curse for some students and a blessing for others.",
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
    "The flexibility of the schedule allows for efficient and clear time management, which is often overlooked in traditional classroom settings.",
    "The ability to manage time effectively and clearly is crucial for success in any learning environment, including online courses.",
    "The ability to allocate time efficiently and clearly is a valuable skill that can be applied across various areas of life, not just in the context of education."
  ],
  [
    "These ideas being the bright side of the issue; there are screen-sharing mishaps, an absurd absence of a schedule in the lives of the undisciplined students, and loosely proctored quizzes to restore the balance.",
    "The positive aspects of the situation include the ability to share ideas through screen-sharing technology, the lack of a structured schedule for some students, and the occasional use of unscheduled quizzes to maintain academic integrity.",
    "The benefits of the situation include the ability to collaborate with others through screen-sharing technology, the absence of a rigid schedule for some students, and the occasional use of unscheduled quizzes to ensure academic honesty.",
    "The advantages of the situation include the ability to work together with others through screen-sharing technology, the lack of a structured schedule for some students, and the occasional use of unscheduled quizzes to maintain academic integrity."
  ],
  [
    "There's no stringent bus driver who's gonna leave you behind if you're not at the stop on time; no way for the teacher to genuinely threaten you for your disrespectful actions.",
    "There is no strict adherence to a schedule or timetable, allowing students to arrive and depart at their own pace without fear of punishment or consequences.",
    "The lack of a rigid bus schedule or a stern teacher who enforces rules allows students to have more freedom in their daily routines and make their own decisions about when they arrive and leave.",
    "There is no pressure to adhere to a strict timetable or schedule, allowing students to come and go as they please without fear of punishment or consequences."
  ],
  [
    "Teachers have gone from the magicians in their five-star, one-person shows to street performers, begging for the least possible glance of interest at a medieval caf\u00e9.",
    "Teachers are no longer revered as masters of knowledge and authority, but rather seen as struggling performers who must work hard to gain even the slightest attention from their students.",
    "The once-glamorous role of the teacher has been reduced to that of a street performer, begging for any possible glance of interest from their students.",
    "Teachers are no longer seen as the all-knowing and powerful masters of knowledge and authority, but rather as struggling performers who must work hard to gain even the slightest attention from their students."
  ],
  [
    "There's no way they can suspend you, the only useful arrow in their otherwise hollow quavers, for being late to the zoom meeting; why of course, you had connectivity issues, who doesn't when there's a biology class at 8:30 in the morning? Another problem is the access to anonymity on specific platforms (Zoom, at least, when you don't know how to secure a meeting).",
    "There is no way for teachers to punish or discipline students for being late to a zoom meeting, as there are no strict attendance policies or consequences for missing class.",
    "The lack of strict attendance policies and consequences for missing class allows students to have more freedom in their daily routines and make their own decisions about when they attend classes.",
    "There is no way for teachers to punish or discipline students for being late to a zoom meeting, as there are no strict attendance policies or consequences for missing class."
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
        self.nlp = None
        self.rephraser = None #initialized only if rephrasing function is called
        self.messageCharSet = []
        for i in range(0,10):
            self.messageCharSet.append(str(i))
        for i in range(0,26):
            self.messageCharSet.append(chr(ord('a')+i))
        print(self.messageCharSet)
    def extractSentences(self,doc:Doc):
        msDoc = Document(doc.path)
        paras = msDoc.paragraphs
        result = []
        paraSentCount:list[ParaData] = []
        for para in paras:
            paraSentCount.append(ParaData(0,para.style))
            para.text = para.text.strip()
            # print(para.text)
            sents = self.delimSplit(para.text)            
            paraSentCount[-1].sentCount = len(sents)
            result.extend(sents)
        return result,paraSentCount
    def injectSentences(self,doc:Doc,sentences,paraSentCount:list[ParaData]):
        msDoc = Document()
        pos = 0
        for paraData in paraSentCount:
            # print('sentcount: ',paraData.sentCount,'style: ',paraData.style.name)
            # print(getDataMembers(paraData.style.font))
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
                        if(not (options[i][-1] in DELIMS)):
                            options[i]+=delim
        #TODO discard sentences that are too far.
        if(self.nlp is None):
            self.nlp = spacy.load('en_core_web_lg')
        simils = []
        for j in range(len(variations)):
            options = variations[j]
            similarities = [1]
            filteredOptions = [options[0]]
            if(len(options)>1):
                truth = self.nlp(options[0])
                for i in range(1,len(options)):
                    option = self.nlp(options[i])
                    if(truth.similarity(option)>SIMILARITY_THRESHOLD):
                        filteredOptions.append(options[i])
            variations[j] = filteredOptions
        # print(simils)
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
    def delimSplit(self,bulktext:str):
        regex = '|'.join('(?<={})'.format(re.escape(delim)) for delim in DELIMS)
        # print(regex)
        output = re.split(regex,bulktext)
        ans = []
        for i in range(len(output)):
            if(len(output[i])>0):
                ans.append(output[i].strip())
        return ans
    def decodeFromDoc(self,doc,outputDoc):
        cleanVariations,_ = self.getFullDocVariations(doc)
        sentences,_ = self.extractSentences(outputDoc)
        offsets = self.getOffsets(cleanVariations)
        indices = [0]*len(offsets)
        for i in range(0,len(sentences)):
            # try:/
                print(cleanVariations[i],sentences[i])
                indices[i] = cleanVariations[i].index(sentences[i])
            # except:
            #     # print(cleanVariations[i])
            #     # print(sentences[i])
            #     # print(cleanVariations[0],cleanVariations[-1])
            #     # print(sentences[0],sentences[-1])
            #     # print(len(cleanVariations),len(sentences))
            #     return ''
        message = self.multibaseDecode(offsets,indices)
        return message
    def messageToNum(self,message:str):
        # allows for lowercase alphanum, spaced messages.
        ans = 0
        for i in range(0,len(message)):
            c = message[i]
            ans *= len(self.messageCharSet)
            ans += self.messageCharSet.index(c)
        return ans
    def numToMessage(self,num:int):
        message = ''
        l = len(self.messageCharSet)
        while(num>0):
            message += self.messageCharSet[num % l]
            num = math.floor(num/l)
        message = message[::-1]
        return message
    def customEncode(self,message:str)->bytearray:
        ans = []
        for i in range(0,len(message)):
            c = message[i]
            ans.append(self.messageCharSet.index(c))
        return bytearray(ans)
    def customDecode(self,message:bytearray)->str:
        ans = ''
        for b in message:
            ans += self.messageCharSet[b]
        return ans
    # def messageToNum2(self,message:str):
    #     num = 0
    #     compressedMessage = zlib.compress(self.customEncode(message))
    #     print(compressedMessage,len(compressedMessage))
    #     decompressed = zlib.decompress(compressedMessage) 
    #     print(self.customDecode(decompressed))
    #     return num
    # def numToMessage2(self,num:int):
    #     message = ''
    #     return message
def safeAttachExtension(filename:str,ext:str):
    if(not filename.endswith(ext)):
        # if(filename.endswith('.doc')):
        #     filename+='x'
        # else:
        filename+=ext
    return filename
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--plain',type=str,help='Path to input .docx file.',required=True)
    parser.add_argument('--output',type=str,help='Path to output .docx file.',required=True)
    parser.add_argument('--message',type=str,help='Message to encode into input to produce output.')
    parser.add_argument('--decode',type=bool,help='Use this (--decode True) to decode output document using plain document',default=False)
    args = parser.parse_args()
    dvg = DocVariationsGenerator()
    outFname:str = args.output
    doc:Doc = Doc(args.plain)
    
    if(args.decode):
        outputDoc:Doc = Doc(args.output)
        numMsg = dvg.decodeFromDoc(doc,outputDoc)
        message = dvg.numToMessage(numMsg)
        print(message)
    else:
        if(args.message is None):
            print('No message passed for encoding.')
            parser.print_help()
            exit()
        message = dvg.messageToNum(args.message)
        dvg.encodeIntoDoc(doc,message,outFname)
        print('Encoded doc saved to: ',outFname)