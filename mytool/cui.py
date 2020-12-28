'''
將 txt 讀入後 呼叫 metamap 做 mapping 
回傳 sematic type, CUI, position, negation
可以使用sldi, sldiID兩種格式檔案
'''
from pymetamap import MetaMap
from . import mmi_parser as mmip
mm = MetaMap.get_instance('/home/feng/public_mm/bin/metamap20')
import csv
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
                "PREFER_N:"+concept.preferred_name, "NEGATED:"+mmip.trigger_parser(concept.trigger), "TRIGGER:"+concept.trigger)
            cui_list.append(concept.cui)
    return cui_list
def handle_index(original_index):
    original_index.split()
def debug_extract_cui(patient_id, target_date):
    input_txt_path = 'Clinical_Note/'+str(patient_id)+'/output/'+str(target_date)+'_o.txt'
    print("-----Processing file : "+ input_txt_path+"-----")
    sents, lines = read_line(input_txt_path)
    index_list = range(1, lines+1)
    # 將剛剛讀出的行內容List, 傳給 mm.extract_concepts 取出概念
    # concepts, error = mm.extract_concepts(
    #     sents, index_list, word_sense_disambiguation=True, user_define_acronyms=False, file_format= 'sldiID', )
    concepts, error = mm.extract_concepts(
        filename= input_txt_path, word_sense_disambiguation=True, user_define_acronyms=False, file_format= 'sldiID', )
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
            if number_for_everyone != int(concept.index[3:6]):
                whether_print = True
                number_for_everyone += 1 
            if True: #is_target_smt(concept) :
            # if True :
                if whether_print:
                    if True:
                        print("Index:"+str(int(concept.index[3:6])))
                    whether_print =False
                
                if True:
                    print("CUI:"+concept.cui, "SMT:"+concept.semtypes, "POS:"+concept.pos_info, 
                    "PREFER_N:"+concept.preferred_name, "NEGATED:"+mmip.trigger_parser(concept.trigger), "TRIGGER:"+concept.trigger)
                cui_list.append(concept.cui)

        elif hasattr(concept, 'ua'):
            print("----UDA----")
            print(" index :"+concept.index, "short_form :"+concept.short_form, "long_form :"+concept.long_form,
            "POS :"+concept.pos_info)
            print("-----------")
    
    return cui_list


def extract_sldiID(patient_id, number_of_note, output=True):
    '''
    update !!
    負責解析(mapping) txt 檔案中的每一個句子中的每一個term 到 一個 concept
    輸入檔案為 sldiID 模式
    會將所有資訊輸出成csv 到 output 資料夾中
    patient_id : 欲做 mapping 的病人ID
    number_of_note : 這個病人有幾個病例
    此 function 會回傳mapping 到的concpet 所有資訊
    （ 如：cui, position, negation, smt_type...)
    '''
    for cnt in range(1, number_of_note+1):
        txt_file = 'Clinical_Note/'+str(patient_id)+'/output/'+str(cnt)+'_o.txt'
        # 80001/80001-1_o.txt
        output_file_path = 'Clinical_Note/'+str(patient_id)+'/csv/'+str(cnt)+'.csv'
        csvfile = open(output_file_path, 'w', newline='')
        writer = csv.writer(csvfile)
        writer.writerow(['CUI', 'ROW', 'POSITION', 'NEGATION', 'SMT', 'TRIGGER'])
        print("-----Processing file : "+ txt_file+"-----")
        # sents, lines = read_line(txt_file)
        # index_list = range(1, lines+1)
        # 將剛剛讀出的行內容List, 傳給 mm.extract_concepts 取出概念
        concepts, error = mm.extract_concepts(
            filename=txt_file, word_sense_disambiguation=True, no_derivational_variants=True ,derivational_variants=False, user_define_acronyms=True, file_format= 'sldiID',  )
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
                if number_for_everyone != int(concept.index[3:6]) :
                    whether_print = True
                    number_for_everyone += 1 
                if is_target_smt(concept) :
                # if True :
                    if whether_print:
                        if output:
                            print("Index:"+str(int(concept.index[3:6])))
                        whether_print =False
                    
                    if output:
                        print("CUI:"+concept.cui, "SMT:"+concept.semtypes, "POS:"+concept.pos_info, 
                        "PREFER_N:"+concept.preferred_name, "NEGATED:"+mmip.trigger_parser(concept.trigger), "TRIGGER:"+concept.trigger)
                        writer.writerow([concept.cui, int(concept.index[3:6]), concept.pos_info, mmip.trigger_parser(concept.trigger), concept.semtypes, concept.trigger])
                    cui_list.append(concept.cui)

            elif hasattr(concept, 'ua'):
                print("----UDA----")
                print(" Index :"+concept.index, "short_form :"+concept.short_form, "long_form :"+concept.long_form,
                "POS :"+concept.pos_info)
                print("-----------")
        csvfile.close()
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

def is_target_smt(concept_obj):
    if (concept_obj.semtypes == "[clnd]" or concept_obj.semtypes == "[dsyn]" or concept_obj.semtypes == "[acab]"
                    or concept_obj.semtypes == "[anab]" or concept_obj.semtypes == "[fndg]" or concept_obj.semtypes == "[inpo]"
                    or concept_obj.semtypes == "[mobd]" or concept_obj.semtypes == "[neop]" or concept_obj.semtypes == "[patf]"
                    or concept_obj.semtypes == "[sosy]" or concept_obj.semtypes == "[aapp]" or concept_obj.semtypes == "[antb]"
                    or concept_obj.semtypes == "[bacs]" or concept_obj.semtypes == "[chem]" or concept_obj.semtypes == "[enzy]"
                    or concept_obj.semtypes == "[hops]" or concept_obj.semtypes == "[horm]" or concept_obj.semtypes == "[imft]"
                    or concept_obj.semtypes == "[inch]" or concept_obj.semtypes == "[lbpr]" or concept_obj.semtypes == "[medd]"
                    or concept_obj.semtypes == "[nnon]" or concept_obj.semtypes == "[orch]" or concept_obj.semtypes == "[phsu]"
                    or concept_obj.semtypes == "[topp]" or concept_obj.semtypes == "[vita]") :
        return True
    else: 
        return False


def cui_compare(patient_id, ndays, startday, method="smt", mode="and"):
    '''
    patient_id :輸入要比較的病人ID
    method :使用的方法 semtaic type or similarity
    ndays :往前比較幾天
    startday :從第幾天開始
    mode :比較的模式 and/or

    '''
    sm_type={"[clnd]":0, "[dsyn]":0, "[acab]":0,"[anab]":0, "[fndg]":0, "[inpo]":0, "[mobd]":0, "[neop]":0, "[patf]":0, "[sosy]":0, "[aapp]":0, "[antb]":0,
                "[bacs]":0, "[chem]":0, "[enzy]":0, "[hops]":0, "[horm]":0, "[imft]":0, "[inch]":0, "[lbpr]":0, "[medd]":0, "[nnon]":0, "[orch]":0, "[phsu]":0,
                "[topp]":0, "[vita]":0,}
    # how to access use : sm_typpe['[clnd]']
    smt_appeared_cur = list()
    smt_appeared_before_ndays = list()
    smt_appeared_all = list()
    
    # ----------------------------------------------------------
    date = ndays+1
    # cnt = today, ndays = n天前
    for cnt in range(date, 0,-1):
        print("***** 這是第", cnt, "天*****")
        txt_file =  str(patient_id)+'/'+str(patient_id)+'-'+str(cnt)+'_o.txt'
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
                if is_target_smt(concept):
                    # 如果是目標內的smt 才做以下事情
                # if True :
                
                    print("Index:"+concept.index)
                    if cnt == date:
                        pass
                        # smt_appeared_all = smt_appeared_cur
                    else:
                        pass
                        # is_appeared(concept.semtypes, smt_appeared_before_ndays)
                    print("CUI:"+concept.cui, "SMT:"+concept.semtypes, "POS:"+concept.pos_info, 
                    "NEGATED:"+mmip.trigger_parser(concept.trigger)[5], "TRIGGER:"+concept.trigger)
                    cui_list.append(concept.cui)
            elif hasattr(concept, 'ua'):
                print("----UDA----")
                print(" index :"+concept.index, "short_form :"+concept.short_form, "long_form :"+concept.long_form,
                "POS :"+concept.pos_info)
                print("-----------")
        if cnt == date:
            # print("第",cnt,"天的semantic type：",smt_appeared_cur)
            sm_type = dict.fromkeys(sm_type, 0)
            print("dict rest.")
    
    smt_appeared_all = list(set(smt_appeared_cur) | set(smt_appeared_before_ndays))
    print("比較：第", date, "天 往前追朔", ndays, "天的Semantic type")
    print("全部出現的 semantic type：", smt_appeared_all)
    print("第",date,"天的semantic type：",smt_appeared_cur)
    print(ndays,"天之間出現的 semantic type：", smt_appeared_before_ndays)
    print("第", date,"天 跟前", ndays, "天相比，沒出現過的 SMT (新資訊) : ", list(set(smt_appeared_cur)-set(smt_appeared_before_ndays)))
    print("第", date,"天 跟前", ndays, "天相比，已出現過的 SMT (舊資訊) : ", list(set(smt_appeared_cur)-(set(smt_appeared_cur)-set(smt_appeared_before_ndays))))
    