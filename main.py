from mytool import cui
from mytool import sentenizer, compare

# ----executive switch-----
exe_step1 = 0
exe_step2 = 0
exe_step3 = 0
exe_step4 = 0
exe_step5 = False
# ---------


'''
Step 1 :先處理 txt 檔案的句子，讓句子前面都有SID編號
'''
patient_date = {80001:12, 80002:9, 80003:9, 80004:10, 80005:10, 80006:14, 80007:18, 80008:13, 80009:8, 80010:10}
if exe_step1:
    for patient, num_of_dates in patient_date.items():
        print("正在處理病人", patient, "共", num_of_dates, "天的病例.....")
        sentenizer.file_process(patient, num_of_dates)
    print("全部病人全部天數病例處理完畢！")

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
# cui.extract_sldiID(80001, 12,)

# Step 5 : 標注後輸出結果
compare.concept_id(80001, 8, 1)