import csv
from . import mmi_parser
def concept_id(patientID, start_date, number_of_day=1, mode='or', whether_print=False):
    """用以比較病例，從未出現過的CUI，才會被標注

    Args:
        patientID (int): 輸入病人ID
        start_date (str): 目標病例，輸入第幾天
        number_of_days (int, optional): 欲往前比較天數. Defaults to 1.
        mode (str, optional):選擇比較模式 and或是 or. Defaults to 'or'.
        whether_print(bool, optional):要不要列印出比較結果
    Returns:
        list: 傳回要標注的新資訊位置 行, 字元
    """  
    anno_list = list() #欲標注的
    end_boundry = start_date-number_of_day-1 # 目標天數～第幾天
    
    pre_date = start_date-1
    input_path = 'Clinical_Note/'+str(patientID)+'/csv/'+str(start_date)+'.csv'
    # 讀取第n天 csv檔案 因為有該天CUI資訊
    
    # input_path_pre = 'Clinical Note/'+str(patientID)+'/csv/'+str(pre_date)+'.csv'
    csv_file_cur = open(input_path, newline='') #打開今天的csv檔案
    # csv_file_pre = open(input_path_pre, newline='')
    
    def to_pre_path(date):
    # 產生前一天檔案之路徑
        input_path_pre = 'Clinical_Note/'+str(patientID)+'/csv/'+str(date)+'.csv'
        return input_path_pre

    rows_cur = list(csv.DictReader(csv_file_cur))
    # 目前的 csv to list 

    # rows_pre = list(csv.DictReader(csv_file_pre))
    # 前一次的 csv to list

    org_cnt = 0
    for row_cur in rows_cur:
        org_cnt+=1
        # print(row_cur['CUI'])
    # print('rows_cur共有'+str(cnt)+'個CUI')

    if start_date != number_of_day:
        for n in range(start_date, end_boundry, -1):
            # 總共做幾次
            if whether_print:
                print("Now processing...", "第", n, "天")
            
            csv_file_pre = open(to_pre_path(n), newline='')
            # 打開昨天csv檔
            rows_pre = list(csv.DictReader(csv_file_pre))
            for row_cur in rows_cur: 
                for row_pre in rows_pre:
                    # row_pre['CUI']
                    if row_cur['CUI'] == row_pre['CUI']:
                        if whether_print:
                            print(row_cur['CUI'])
                        # 輸出一樣的CUI
                        rows_cur.pop()

        
                        
                            # del row_cur
        now_cnt = 0
        for r in rows_cur:
            now_cnt+=1

        if whether_print:
            print("病人", patientID, "第", start_date, "天的病例, 往前追朔", number_of_day, "天")
            print("----原本", str(org_cnt), "個CUI，現在剩下", now_cnt, "個CUI----")
        n = 0
        for r in rows_cur:
            if whether_print:
                print(r['CUI'], r['ROW'], r['POSITION'], r['NEGATION'],)
            anno_list.append([])
            anno_list[n].append(str(r['ROW']))
            anno_list[n].append(str(r['POSITION']))
            anno_list[n].append(r['TEXT_TRIGGER'])
            n+=1
        
        if whether_print:
            print(anno_list)
        return anno_list
    else:
        print("錯誤！\n開始日跟追朔日期一樣，不行！")



def concept_similarity():
    pass