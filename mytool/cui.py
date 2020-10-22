'''
將 txt 讀入後 呼叫 metamap 做 mapping 
回傳 sematic type, CUI, position, negation
可以使用sldi, sldiID兩種格式檔案
'''
from pymetamap import MetaMap
from . import mmi_parser as mmip
mm = MetaMap.get_instance('/home/feng/public_mm/bin/metamap20')

# txt_file = "clinical_txt/1.txt"

# read a file line by line to a List
def read_line(txt_file):
    sentences = list()
    with open(txt_file, 'r') as f:
        # i = index number, l = 讀出的某一行內容
        for i, l in enumerate(f):
            sentences.append(l)
        lines = i + 1
        return sentences, lines

def extract_sldi(txt_file, output=True):
    concepts, error = mm.extract_concepts(
    filename = txt_file, word_sense_disambiguation =True
)
    cui_list = list()
    for concept in concepts:
        '''
        Concept : 
        Index 儲存行的資訊
        semtype 儲存 semantic type 的資訊
        '''    
        
        if concept.semtypes == "[clnd]" or concept.semtypes == "[dsyn]" :
            if output:
                print("Index:"+concept.index)
            
            
            if output:
                print("CUI:"+concept.cui, "SMT:"+concept.semtypes, "POS:"+concept.pos_info, 
                "PREFER_N:"+concept.preferred_name, "NEGATED:"+mmip.trigger_parser(concept.trigger)[5], "TRIGGER:"+concept.trigger)
            cui_list.append(concept.cui)
    return cui_list


def extract_sldiID(txt_file, output=True):
    
    sents, lines = read_line(txt_file)
    index_list = range(1, lines+1)
    # 將剛剛讀出的行內容List, 傳給 mm.extract_concepts 取出概念
    concepts, error = mm.extract_concepts(
        sents, index_list, word_sense_disambiguation=True, derivational_variants=True, user_define_acronyms=True, file_format= 'sldiID')

    number_for_everyone = 0
    # 每個 concept 都有的數值, 紀錄現在印到了哪個 index
    # 每個 index 只會印一次
    whether_print = True
    # 如果印出了 index 就不要印了 設為否
    cui_list = list()
    for concept in concepts:
        '''
        Concept : 
        Index 儲存行的資訊
        semtype 儲存 semantic type 的資訊
        '''    
        if hasattr(concept, 'mm'):
            if number_for_everyone != int(concept.index) :
                whether_print = True
                number_for_everyone += 1 
            if (concept.semtypes == "[clnd]" or concept.semtypes == "[dsyn]" or concept.semtypes == "[acab]"
                or concept.semtypes == "[anab]" or concept.semtypes == "[fndg]" or concept.semtypes == "[inpo]"
                or concept.semtypes == "[mobd]" or concept.semtypes == "[neop]" or concept.semtypes == "[patf]"
                or concept.semtypes == "[sosy]" or concept.semtypes == "[aapp]" or concept.semtypes == "[antb]"
                or concept.semtypes == "[bacs]" or concept.semtypes == "[chem]" or concept.semtypes == "[enzy]"
                or concept.semtypes == "[hops]" or concept.semtypes == "[horm]" or concept.semtypes == "[imft]"
                or concept.semtypes == "[inch]" or concept.semtypes == "[lbpr]" or concept.semtypes == "[medd]"
                or concept.semtypes == "[nnon]" or concept.semtypes == "[orch]" or concept.semtypes == "[phsu]"
                or concept.semtypes == "[topp]" or concept.semtypes == "[vita]") :
            # if True :
                if whether_print:
                    if output:
                        print("Index:"+concept.index)
                    whether_print =False
                
                if output:
                    print("CUI:"+concept.cui, "SMT:"+concept.semtypes, "POS:"+concept.pos_info, 
                    "PREFER_N:"+concept.preferred_name, "NEGATED:"+mmip.trigger_parser(concept.trigger)[5], "TRIGGER:"+concept.trigger)
                cui_list.append(concept.cui)
        elif hasattr(concept, 'ua'):
            print("This is UDA !")
    return cui_list
    # Output format is : index, mm, score, preferred_name, cui, semtype, trigger, location, pos_info, tree_nodes
