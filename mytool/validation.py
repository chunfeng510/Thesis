from gatenlp import Document
# from IPython.display import display

def validate(patient_id, start_date, num_of_day, ):
    input_path = 'Clinical_Note/'+str(patient_id)+'/annotated/'+str(start_date)+'_'+str(num_of_day)+'.bdocjs'
    # 這邊先用絕對路徑之後會改
    # 黃金準則 
    doc_gold = Document.load('/home/feng/7_1_o.xml', fmt = "gatexml")
    
    annset_gold = doc_gold.annset('')
    annset_tk = doc_gold.annset('Token').with_type('Token')
    
    # mm 全標
    doc_mm = Document.load('Clinical_Note/'+str(patient_id)+'/annotated/'+str(start_date)+'_0'+'.bdocjs')
    annset_mm = doc_mm.annset()
    annset_mm_tk = 0
    for i in annset_mm:
        for j in annset_tk:
            if i.iscovering(j):
                annset_mm_tk += 1


    # 系統標注的
    doc_target = Document.load(input_path)
    # 系統標注的 annotation set
    annset_target = doc_target.annset()

    # 文本共幾個 token
    text_all_tk = annset_tk.size

    # 系統標注的 annotation set 轉成 token
    annset_target_tk = 0
    for ann_t in annset_target:
        for ann_g in annset_mm:
            if ann_t.iscovering(ann_g):
                annset_target_tk += 1
    
    # 黃金準則標注的 annotation set 轉成 token
    # annset_gold_tk = 0 
    # for i in annset_gold:
    #     for j in annset_tk:
    #         if i.iscovering(j):
    #             annset_gold_tk += 1
    annset_gold_tk = 0 
    for i in annset_gold:
        for j in annset_mm:
            if i.iscovering(j):
                annset_gold_tk += 1
    print("annset_gold_tk", annset_gold_tk)
    
    annset_score = doc_target.annset("score")
    score = 0
    
    # 計分區
    for i in annset_target:
        for j in annset_gold:
            if i.iswithin(j):
                annset_score.add_ann(i.copy())
                score += 1

    score_tk = 0
    for i in annset_score:
        for j in annset_tk:
            if i.iscovering(j):
                score_tk += 1
    
    print("黃金準則 token", annset_gold_tk, "系統標注 token", annset_target.size, "score_token", score_tk)
    print("Precision:", round ((score_tk / (annset_gold_tk)*100), 2), "Recall:", round ((score_tk / annset_target_tk*100), 2))

validate(80001, 7, 1)