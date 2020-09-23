from pymetamap import MetaMap
from mytool import mmi_parser as mmip
mm = MetaMap.get_instance('/home/feng/public_mm/bin/metamap20')

txt_file = "clinical_txt/2.txt"

concepts, error = mm.extract_concepts(
    filename = txt_file, word_sense_disambiguation=True
)
counter = 0
for concept in concepts:
    '''
    Concept : 
    Index 儲存行的資訊
    semtype 儲存 semantic type 的資訊
    '''    
    
    if concept.semtypes == "[clnd]" or concept.semtypes == "[dsyn]" :
        print("Index:"+concept.index)
        
        print("CUI:"+concept.cui, "SMT:"+concept.semtypes, "POS:"+concept.pos_info, 
        "PREFER_N:"+concept.preferred_name, "NEGATED:"+mmip.trigger_parser(concept.trigger)[5], "TRIGGER:"+concept.trigger)
        counter = counter + 1
print(counter)