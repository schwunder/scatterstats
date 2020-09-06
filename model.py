import spacy

try:
    nlp = spacy.load("en_core_web_md")
except:
    nlp = spacy.load("en")
