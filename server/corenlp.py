from nltk.parse.corenlp import CoreNLPServer,CoreNLPParser
import os
# CORENLP_JAR = "C:/CODE/nlp/stanford-corenlp-4.5.5/stanford-corenlp-4.5.5.jar"
# CORENLPMODEL_JAR = "C:/CODE/nlp/stanford-corenlp-4.4.0-models-english.jar"
# Start server using startcnlp.ps1
CORENLP_URL = "http://localhost:9000"
parser = CoreNLPParser(url=CORENLP_URL)
parse = next(parser.raw_parse("I want some time to myself."))

# parse.chomsky_normal_form()
parse.pretty_print()

