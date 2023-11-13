from gpt4all import GPT4All
DEFAULT_MODEL = "orca-mini-3b.ggmlv3.q4_0.bin"
GPT4FAICON_MODEL = "mistral-7b-openorca.Q4_0.gguf"
"""
Prompt that works with GPT
Give me 3 sentences with the same meaning as "Grant the class-clown a Guy-Fawkes curtain and suddenly, his jokes aren't gonna be quite PG13." Write nothing else in your response.
"""

class Rephraser:
    def __init__(self,modelName=DEFAULT_MODEL):
        self.model = GPT4All(modelName)
    def getParaphrases(self,sentence,numPhrases):
        ans = [sentence]
        queryStr = f"Give me {numPhrases} sentences which have exactly the same meaning as '{sentence}'"
        print(queryStr)
        output = self.model.generate(queryStr,temp=0)#temp = 0 for predictable output.
        print(output)
        if(len(output)>0):
            phrases = output.splitlines()
            if(len(phrases)==numPhrases+1):
                for phrase in phrases:
                    if(len(phrase)>0):
                        phrase = phrase.split('. ')[1]# removing enumeration
                        ans.append(phrase)
        return ans
    def paraphraseSentences(self,sentences,numPhrases,minLength=1):
        ans = []
        for sentence in sentences:
            if((len(sentence.split(' '))>minLength)):
                ans.append(self.getParaphrases(sentence,numPhrases))
            else:
                ans.append([sentence])
        return ans
if __name__=='__main__':
    rephraser = Rephraser(modelName=GPT4FAICON_MODEL)
    phrases = rephraser.getParaphrases("Grant the class-clown a Guy-Fawkes curtain and suddenly, his jokes aren't gonna be quite PG13.",3)
    
    print(*phrases,sep='\n')