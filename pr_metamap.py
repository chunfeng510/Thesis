from pymetamap import MetaMap
from mytool import mmiparser as mmip
mm = MetaMap.get_instance('/home/feng/public_mm/bin/metamap20')

sents2 = ['John had a huge heart attack and fever']
# sents = ['cold', "John had huge heart attack and fever"]
txt_file = "clinical_txt/1.txt"


def read_line(txt_file):
    sentences = list()
    with open(txt_file, 'r') as f:
        for i, l in enumerate(f):
            sentences.append(l)
        lines = i + 1
        return sentences, lines


sents, lines = read_line(txt_file)
index_list = range(1, lines+1)
concepts, error = mm.extract_concepts(
    sents, index_list, word_sense_disambiguation=True)

str = []
n = 0
for concept in concepts:
    # if n != int(concept.index):
    '''
    Concept : 
    Index 儲存行的資訊
    semtype 儲存 semantic type 的資訊
    '''
    if n != int(concept.index):
        print("Index:"+concept.index)
        n += 1
    if concept.semtypes == "[clnd]" or concept.semtypes == "[dsyn]" :
        print("CUI:"+concept.cui, "SMT:"+concept.semtypes, "POS:"+concept.pos_info, 
        "PREFER_N:"+concept.preferred_name, "NEGATED:"+mmip.trigger_parser(concept.trigger)[5], "TRIGGER:"+concept.trigger)
    
    
# Output format is : index, mm, score, preferred_name, cui, semtype, trigger, location, pos_info, tree_nodes
