import glob
patient = [80001, 80002, 80003, 80004, 80005, 80006, 80007, 80008, 80009, 80010]
measure = "path"
# 取得該目錄下的所有txt檔
for i in range(1,10):
    file_list = glob.glob("/home/feng/桌面/to_be_calculated/"+str(patient[i])+"/score/"+measure+"/*.txt")
    op_file = "Clinical_Note/"+str(patient[i])+"/"+str(patient[i])+"_scoredb_"+measure+".txt"
    # 將某病人某方法算出的全部smt相似度分數都聚合在一起
    print("正在結合所有相似度分數 for", patient[i], ".....")
    if True:
        with open(op_file, 'w') as outfile:
            for fname in file_list:
                with open(fname) as infile:
                    outfile.write(infile.read())

    from tinydb import TinyDB
    from tinydb.queries import Query, where
    print("正在建立分數資料庫 for", patient[i], ".....")
    db = TinyDB("Clinical_Note/"+str(patient[i])+"/DB/"+str(patient[i])+"_scoredb_path.json")
    f = open("Clinical_Note/"+str(patient[i])+"/"+str(patient[i])+"_scoredb_path.txt")
    rec = f.readline()
# # print(rec.split("<>")[0], rec.split("<>")[1], rec.split("<>")[2].replace('\n', ''))
# q = Query()
# res = db.search((q.cui1 == 'C0748646') & (q.cui2 == 'C0010520'))

# # print(res[0]['score'])
# print(res)

# 建立DB階段
    if True:
        cnt = 0
        while rec: 
            db.insert({'score': rec.split("<>")[0] , 'cui1': rec.split("<>")[1], 'cui2': rec.split("<>")[2].replace('\n', '')})
            rec = f.readline()
            cnt += 1
        print(cnt)

