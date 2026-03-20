import nltk
from nltk.corpus import wordnet as wn
synsets = wn.synsets("snake")[0]
print(synsets.hyponyms())