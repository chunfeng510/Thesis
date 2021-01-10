from mytool import cui
from mytool import sentenizer

'''
Step 1 :先處理 txt 檔案的句子，讓句子前面都有SID編號
'''
# sentenizer.file_process(80002, 9)
# sentenizer.file_process(80003, 9)
# sentenizer.file_process(80004, 10)
# sentenizer.file_process(80005, 10)

'''
Step 2 : mapping 出不重複的CUI
這個只需要做一次 每個病人都有一份 list 就好
產出計算清單用
'''
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



# Step 3 : 輸出每個病人、每一天，mapping到的結果成csv 快速存取
cui.extract_sldiID(80001, 12,)

# Step 4 : 標注後輸出結果