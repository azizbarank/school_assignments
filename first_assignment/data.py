import csv
import json

# change to your file 
file = "dev_nl.tsv"
MAX = 100 

def filterNERD(tag) :
    try:
        neclass = tag.split('-')[1]
    except:
        neclass = 'MISSING'
    # print(neclass)
    return neclass not in ['ANIM', 'FOOD', 'DIS', 'PLANT','TIME']  # ignore lower-case concepts and years 

def detokenize(tokens) :
    string = ' '.join(tokens)
    string = string.replace(' - ','-') # Engels - Nederlandse 
    string = string.replace(' e ','e ') # 19 e eeuw
    return string

annotations = []

with open(file) as nd:
    nerd = csv.reader(nd, delimiter="\t", quoting=csv.QUOTE_NONE)
    tokens = []
    annotation = []  # Fix: initialize annotation list
    count = 0 
    for row in nerd:
        if len(row) >= 3 :
            tokens.append(row[1])
            if len(row) > 4 :
                if row[6] and filterNERD(row[2]):
                   annotation.append(row[6])
        else :
            if annotation and count <= MAX :
                string = detokenize(tokens)
                annotations.append({"string":string,"annotation":annotation})
                count+=1
            annotation = []
            tokens = []
    for a in annotations :
        print(a['string'],a['annotation'])

import random

def get_random_sample(annotations, sample_size=100, seed=42):
    """
    Get a random sample of sentences with named entities.
    
    Args:
        annotations: List of annotation dictionaries
        sample_size: Number of sentences to sample
        seed: Random seed for reproducibility
    
    Returns:
        List of sampled annotations
    """
    random.seed(seed)  # For reproducible results
    
    # Filter sentences that have at least one named entity
    sentences_with_entities = [ann for ann in annotations if ann['annotation']]
    
    # If we have fewer sentences than requested, return all
    if len(sentences_with_entities) <= sample_size:
        return sentences_with_entities
    
    # Random sample
    return random.sample(sentences_with_entities, sample_size)

# Get random sample
sample_annotations = get_random_sample(annotations, sample_size=100)

print(f"Total sentences with entities: {len([a for a in annotations if a['annotation']])}")
print(f"Sample size: {len(sample_annotations)}")
print("\nFirst 5 samples:")
for i, ann in enumerate(sample_annotations[:5]):
    print(f"{i+1}. {ann['string']}")
    print(f"   Entities: {ann['annotation']}\n")