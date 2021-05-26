from mytool import cui, sentenizer, compare, annotation
from mytool.validation import validate

# ----executive switch-----
# 文本產生、整理，以送入mm
exe_step1 = 0 #句子加編號
exe_step1_1 = 0 # 處理句子，但不加入編號


exe_step2 = 1

# 產生計算清單，不須再執行了
exe_step3 = 0

# mapping CUI
# 要手動改command！！
# 比較 及 標注功能
# mapping 成 csv 快速存取
exe_step4 = 0

# step 5 適用於修改比較天數
exe_step5 = 0

# 直接使用6
exe_step6_0 = 0
exe_step6 = 0
# 評估
exe_step7 = 0


# ---------


'''
Step 1 :先處理 txt 檔案的句子，讓句子前面都有SID編號<< 這只是為了方便送進去 MM 所做的中間產物
'''
patient_date = {80001:12, 80002:9, 80003:9, 80004:10, 80005:10, 80006:14, 80007:18, 80008:13, 80009:8, 80010:10}
# patient_date = {80006:14, 80007:18, 80008:13, 80009:8, 80010:10}

if exe_step1:
    for patient, num_of_dates in patient_date.items():
        print("正在處理病人", patient, "共", num_of_dates, "天的病例.....")
        sentenizer.file_process(patient, num_of_dates)
    print("全部病人全部天數病例處理完畢！")

    
'''
Step 1_1 :產生去掉SID編號的檔案
'''
# patient_date = {80001:12, }
if exe_step1_1:
    for patient, num_of_dates in patient_date.items():
        print("正在處理病人", patient, "共", num_of_dates, "天的病例.....")
        sentenizer.file_process(patient, num_of_dates, False)
    print("全部病人全部天數病例處理完畢！ *Without SID*")



'''
Step 2 : mapping 出不重複的CUI
這個只需要做一次 每個病人都有一份 list 就好
產出計算清單
'''
if exe_step2:
    for patient, num_of_dates in patient_date.items():
        print("正在輸出病人", patient, "不重複的CUI List")
        cui.get_all_cui_list_unique(patient, num_of_dates)
    print("全部病人不重複的CUI List輸出完畢！")
    
# cui.get_all_cui_list_unique(80001, 12)
# cui.get_all_cui_list_unique(80002, 9)
# cui.get_all_cui_list_unique(80003, 9)
# cui.get_all_cui_list_unique(80004, 10)
# cui.get_all_cui_list_unique(80005, 10)
# cui.get_all_cui_list_unique(80006, 14)
# cui.get_all_cui_list_unique(80007, 18)
# cui.get_all_cui_list_unique(80008, 13)
# cui.get_all_cui_list_unique(80009, 8) 
# cui.get_all_cui_list_unique(80010, 10)

# Step 3 : 產生計算清單 (依照SMT分組，讓umls-similarity.pl計算)
if exe_step3 :
    for patient, num_of_dates in patient_date.items():
        cui.smt_grouping("Clinical_Note/"+str(patient)+"/"+str(patient)+"_all_"+str(num_of_dates)+"_cui_unique.csv", patient)
        print(patient,"的計算清單產生完畢！")
    print("所有計算清單產生完畢！")

# Step 4 : 輸出每個病人、每一天，mapping到的結果成csv 快速存取
# 這邊這個資料是給 compare 功能用的 每天會有該天的CUI
if exe_step4:
    for p, d in patient_date.items():
        
        cui.extract_sldiID(p, d, no_filterd= True)
    

# cui.extract_sldiID(80008, 13, no_filterd= True)

# Step 5 : 標注後輸出結果
patient_id = 80007
start_date = 1
num_of_day = 1


if exe_step5:
    
    a_list = compare.concept_id(patient_id, start_date, num_of_day, 'all', False)
    # a_list = compare.concept_similarity(patient_id, start_date, num_of_day, 0.1, 'path')
    print('以上是 compare 完 要標注的結果清單\n')


# 標注全部mm mapping 到的
# 用mapping出的所有CUI當作基底，等等做比對
if exe_step6_0:
    for p, d in patient_date.items():
        for i in range(2, d+1):
            all_list = compare.concept_id(p, i, 0, 'all', False)
            annotation.annotate(all_list, p, i, 0, False)
            

if exe_step6:
    # annotation.annotate(a_list, patient_id, start_date, num_of_day)
    for p, d in patient_date.items():
        for i in range(num_of_day+1, d+1):
            a_list = compare.concept_id(p, i, num_of_day, 'all', False)
            if p == 81111:
                annotation.annotate(a_list, p, i, num_of_day, False, False)
            else:
                annotation.annotate(a_list, p, i, num_of_day, False, True)
# 會返回 anno_list
    

#  This step is Validation
if exe_step7:
    for p, d in patient_date.items():
        for i in range(num_of_day+1, d+1):
            validate(p, i, num_of_day)

# for i in range(2, 13):
#             validate(80001, i, 1)