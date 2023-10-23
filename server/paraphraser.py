from gpt4all import GPT4All
DEFAULT_MODEL = "orca-mini-3b.ggmlv3.q4_0.bin"
class Paraphrase:
    def __init__(self,modelName=DEFAULT_MODEL):
        self.model = GPT4All(modelName)
    def getParaphrases(self,sentence,numPhrases):
        ans = [sentence]
        output = self.model.generate(f"Paraphrase this sentence into {numPhrases} different sentences, retaining the meaning: {sentence}")
        if(len(output)>0):
            print("***",output,"***",sep='\n')
        return ans
    def paraphraseSentences(self,sentences,numPhrases):
        ans = []
        for sentence in sentences:
            ans.append(self.getParaphrases(sentence,numPhrases))
        return ans