from paraphraser import Rephraser
import pickle as pkl
# rephraser = Rephraser()
# sentences = [
#     "My mother never liked Sherlock Holmes.",
#     "My dad wasn't a big fan of Sherlock Holmes either."
# ]
# object with docID as key and value as {
 #doc path, variations: variationslist   
#}
with open('docvars.pkl','rb') as f:
    pkl.dump({},f)