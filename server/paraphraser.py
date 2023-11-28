from gpt4all import GPT4All
DEFAULT_MODEL = "orca-mini-3b.ggmlv3.q4_0.bin"
GPT4FAICON_MODEL = "mistral-7b-openorca.Q4_0.gguf"

class Rephraser:
    def __init__(self,modelName=DEFAULT_MODEL):
        self.model = GPT4All(modelName)
    def setUpModel(self,numPhrases):
        queryStr = f"For each sentence I give you next, give me {numPhrases} sentences which have exactly the same meaning as my sentence."
        output = self.model.generate(queryStr,temp=0)
        print("Setup output: ",output)
    def getParaphrases(self,sentence,numPhrases):
        ans = [sentence]
        # print(queryStr)
        queryStr = f"Give me {numPhrases} sentences which have exactly the same meaning as '{sentence}'"
        output = self.model.generate(queryStr,temp=0)
        phrases = output.splitlines()
        if(len(phrases)==numPhrases+1):
            for phrase in phrases:
                if(len(phrase)>0):
                    phrase = phrase.split('. ')[1]# removing enumeration
                    ans.append(phrase)
                else:
                    print("unexpected phrase: ",phrase)
        else:
            print('unexpected output: ',output)
        return ans
    def responseToList(self,response):
        phrases = response.splitlines()
        ans = []
        phrases = list(filter(lambda phrase:len(phrase)>0,phrases))
        for phrase in phrases:
            phrase = phrase.split('. ')[1] # removing enumeration.
            ans.append(phrase)
        return ans
    def paraphraseSentences(self,sentences,numPhrases,minLength=1):
        ans = []
        i = 0
        l = len(sentences)
        BATCH_SIZE = 4
        SYSTEM_TEMPLATE=f"You are used to paraphrase sentences"
        PROMPT_TEMPLATE=f"Give me {numPhrases} sentences which have exactly the same meaning as " + "'{0}'"
        for batchIndex in range(0,l,BATCH_SIZE):
            with self.model.chat_session(SYSTEM_TEMPLATE,PROMPT_TEMPLATE):
                for sentence in sentences[batchIndex:batchIndex+BATCH_SIZE]:
                    i+=1
                    options = [sentence]
                    if((len(sentence.split(' '))>minLength)):
                        response = self.model.generate(sentence,temp=0);
                        phrases = self.responseToList(response)
                        if(len(phrases)==numPhrases):
                            options.extend(phrases)
                        else:
                            print('For sentence: ',sentence,' got ',len(phrases),' phrases.')
                            print('unexpected phrases at: ',response)
                        # ans.append(self.getParaphrases(sentence,numPhrases,True))
                    ans.append(options)
                    print(i," of ", l," sentences done")
        return ans
if __name__=='__main__':
    print('main function empty')