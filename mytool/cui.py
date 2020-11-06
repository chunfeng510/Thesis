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
    '''
    沒有修改部份內容，使用須注意
    負責解析(mapping) txt 檔案中的 term 到 CUI
    輸入檔案為 sldi 模式
    '''
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
    '''
    負責解析(mapping) txt 檔案中的 term 到 CUI
    輸入檔案為 sldiID 模式
    txt_file : 欲 mapping 出 CUI 及其他資訊的 txt檔案
    output : 決定是否要輸出訊息，或是直接產生結果
    此 function 會回傳 List 包含所有CUI 資訊
    '''
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
            print("----UDA----")
            print(" index :"+concept.index, "short_form :"+concept.short_form, "long_form :"+concept.long_form,
            "POS :"+concept.pos_info)
            print("-----------")
    return cui_list
    # Output format is : index, mm, score, preferred_name, cui, semtype, trigger, location, pos_info, tree_nodes

def get_all_cui_list(patient_id, date, output = True):
    '''
    回傳 某病人 某幾天病例中的所有 CUI 及 部份資訊：第幾句、位置、否定詞 \n
    patient_id (str) : 指定某病人 \n
    date (int) : 指定取回CUI 病例天數範圍\n
    output (bool): 是否印出執行結果 訊息，預設為 是\n
    '''

    file_out = str(patient_id)+'/'+str(patient_id)+'_all_'+str(date)+'_cui.txt'
    for cnt in range(1, date+1):
        txt_file =  str(patient_id)+'/'+str(patient_id)+'-'+str(cnt)+'_o.txt'
        
        print("-----Processing file : "+ txt_file+"-----")
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
                        print(concept.cui, "POS:"+concept.pos_info, 
                        "NEGATED:"+mmip.trigger_parser(concept.trigger)[5])
                    f = open(file_out, 'a')
                    f.write(concept.cui+", "+concept.index+", "+concept.pos_info+", "+mmip.trigger_parser(concept.trigger)[5]+'\n')
                    
                    cui_list.append(concept.cui)
                    
            elif hasattr(concept, 'ua'):
                print("----UDA----")
                print(" index :"+concept.index, "short_form :"+concept.short_form, "long_form :"+concept.long_form,
                "POS :"+concept.pos_info)
                print("-----------")
                f = open(file_out, 'a')
                f.write(concept.long_form+", "+concept.index+", "+concept.pos_info+'\n')
                
    f.close()       


def get_all_cui_list_unique(patient_id, date, output = True):
    '''
    回傳 某病人 某幾天病例中的所有 CUI（只有CUI） \n
    且 去除重複的 CUI 
    patient_id (str) : 指定某病人 \n
    date (int) : 指定取回CUI 病例天數範圍\n
    output (bool): 是否印出執行結果 訊息，預設為 是\n
    '''
    seen = set()
    file_out = str(patient_id)+'/'+str(patient_id)+'_all_'+str(date)+'_cui_unique.txt'
    f = open(file_out, 'w')
    for cnt in range(1, date+1):
        txt_file =  str(patient_id)+'/'+str(patient_id)+'-'+str(cnt)+'_o.txt'
        
        print("-----Processing file : "+ txt_file+"-----")
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
                            # print("Index:"+concept.index)
                            pass
                        whether_print =False
                    
                    if output:
                        # print(concept.cui, "POS:"+concept.pos_info, 
                        # "NEGATED:"+mmip.trigger_parser(concept.trigger)[5])
                        pass
                    f = open(file_out, 'a')
                    if concept.cui in seen:
                        pass
                    else:
                        f.write(concept.cui+'\n')
                        seen.add(concept.cui)
                       
                    
                            
                    
                    
            elif hasattr(concept, 'ua'):
                # print("----UDA----")
                # print(" index :"+concept.index, "short_form :"+concept.short_form, "long_form :"+concept.long_form,
                # "POS :"+concept.pos_info)
                # print("-----------")
                f = open(file_out, 'a')
                f.write(concept.long_form+'\n') #寫入縮寫詞到檔案
                f.close()
                
    f.close()
    print("\n"+"Success processed "+ str(date) +" days txt files. !!")        