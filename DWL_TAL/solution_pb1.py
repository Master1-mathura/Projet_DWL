import nltk
from nltk.corpus import wordnet as wn
synsets = wn.synsets("snake")
synonymes = []
for syn in synsets:
    for lemme in syn.lemmas():
        synonymes.append(lemme.name())

print(set(synonymes))