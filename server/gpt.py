# import g4f
# response = g4f.ChatCompletion.create(model="gpt-3.5-turbo",messages=[{"role":"user","content":"Hello"}],stream=True)
# for message in response:
#     print(message,flush=True,end='')
# Too slow to function across sentences.
import torch
from transformers import pipeline

# generateText = pipeline(model='databricks/dolly-v2-12b',torch_dtype=torch.bfloat16,trust_remote_code=True,device_map='auto')
# res = generateText('Explain death to me.')
# print(res[0]['generated_text'])

#crashed my system twice.
from gpt4all import GPT4All
def new_text_callback(text):
    print(text, end="")


model = GPT4All("orca-mini-3b.ggmlv3.q4_0.bin")
output = model.generate("Paraphrase this sentence into 5 different sentences, retaining the meaning: My mother once told me she never liked Sherlock Holmes.")
print(output)