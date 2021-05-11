import csv
from mytool import mmi_parser
from tinydb import TinyDB
from tinydb.queries import Query, where
def concept_id(patientID, start_date, number_of_day=1, mode='all', whether_print=False, ):
    """用以比較病例，從未出現過的CUI，才會被標注

    Args:
        patientID (int): 輸入病人ID
        start_date (str): 目標病例，輸入第幾天
        number_of_days (int, optional): 欲往前比較天數. Defaults to 1.
        mode (str, optional):選擇比較模式
        whether_print(bool, optional):要不要列印出比較結果
    Returns:
        list: 傳回要標注的新資訊位置 行, 字元
    """  
    anno_list = list() #欲標注的
    end_boundry = start_date-number_of_day # 目標天數～第幾天
    
    pre_date = start_date-1
    # 是否過濾特定SMT
    if mode == 'all':
        input_path = 'Clinical_Note/'+str(patientID)+'/csv_all/'+str(start_date)+'.csv'
    else:
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
                    if row_cur['CUI'] == row_pre['CUI']:
                        if whether_print:
                            print(row_cur['CUI'])
                        # 輸出一樣的CUI
                        rows_cur.remove(row_cur)
                        break
                    

        
                        
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



def concept_similarity(patientID, start_date, number_of_day=1, threshold = 0.5, measure = 'path', whether_print=True ):
    """使用相似度分數來比較新資訊

    Args:
        patientID (int): [description]
        start_date ([type]): [description]
        number_of_day (int, optional): [description]. Defaults to 1.
        threshold (float, optional): [description]. Defaults to 0.5.
        measure (str, optional): [description]. Defaults to 'path'.
    """
    # 指定要使用的相似度分數檔案DB
    score_file_in = 'Clinical_Note/'+str(patientID)+'_scoredb_'+measure+'.txt'
    score_db = TinyDB('Clinical_Note/'+str(patientID)+'/DB/'+str(patientID)+'_scoredb_'+measure+'.json')

    anno_list = list() #欲標注的
    end_boundry = start_date-number_of_day-1 # 目標天數～第幾天 的界線
    pre_date = start_date-1
    input_path = 'Clinical_Note/'+str(patientID)+'/csv/'+str(start_date)+'.csv'
    csv_file_cur = open(input_path, newline='') #打開今天的csv檔案
    # csv_file_pre = open(input_path_pre, newline='')
    
    def to_pre_path(date):
    # 產生前一天檔案之路徑
        input_path_pre = 'Clinical_Note/'+str(patientID)+'/csv/'+str(date)+'.csv'
        return input_path_pre
    
    def cal_score(cui1, cui2):
        q = Query()
        res = score_db.search((q.cui1 == cui1) & (q.cui2 == cui2))
        if len(res) == 1:
            return float(res[0]['score'])
        elif len(res) > 1:
            print("有錯誤，多餘一個結果")
        
        else: # < 1的話，再找一次
            res = score_db.search((q.cui2 == cui1) & (q.cui1 == cui2))
            if len(res) == 1:
                return float(res[0]['score'])
            else:
                return 0
        
    rows_cur = list(csv.DictReader(csv_file_cur))
    org_cnt = 0
    for row_cur in rows_cur:
        org_cnt+=1
        
    if start_date != number_of_day:
        for n in range(start_date, end_boundry, -1):
            # 總共做幾次
            if whether_print:
                print("Now processing...", "第", n, "天")
            
            csv_file_pre = open(to_pre_path(n), newline='')
            # 打開昨天csv檔，轉成 list
            rows_pre = list(csv.DictReader(csv_file_pre))
            for row_cur in rows_cur: 
                for row_pre in rows_pre:
                    # 代表相似資訊！
                    if cal_score(row_cur['CUI'], row_pre['CUI']) > threshold:
                        if whether_print:
                            print(row_cur['CUI'])
                        # 輸出一樣的CUI
                        rows_cur.remove(row_cur)
                        break
        now_cnt = 0
        for r in rows_cur:
            now_cnt+=1

        if whether_print:
            print("病人", patientID, "第", start_date, "天的病例, 往前追朔", number_of_day, "天")
            print("----原本", str(org_cnt), "個CUI，現在剩下", now_cnt, "個CUI----")
        n = 0
        for r in rows_cur:
            if whether_print:
                print(r['CUI'], r['ROW'], r['POSITION'], r['NEGATION'], )
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
