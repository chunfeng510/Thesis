from gatenlp import Document
import math 
# from IPython.display import display

def validate(patient_id, start_date, num_of_day, ):
    input_path = 'Clinical_Note/'+str(patient_id)+'/annotated/'+str(start_date)+'_'+str(num_of_day)+'.bdocjs'
    # 這邊先用絕對路徑之後會改
    # 黃金準則 
    # doc_gold = Document.load('/home/feng/'+str(start_date)+'_1_o.xml', fmt = "gatexml")
    doc_gold = Document.load('Gold_Standard/'+str(patient_id)+'/'+str(start_date)+'_o.xml', fmt="gatexml")
    
    annset_gold = doc_gold.annset('').with_type('New Info')
    annset_whole_tk = doc_gold.annset('Token').with_type('Token')
    
    # mm 全標
    doc_mm = Document.load('Clinical_Note/'+str(patient_id)+'/annotated/'+str(start_date)+'_0'+'.bdocjs')
    annset_mm = doc_mm.annset('')
    
    annset_mm_mapping_tk = doc_mm.annset("mmtk")
    tmp3 = annset_mm.copy()
     # --------------annset_mm 前處理----------
    
    annset_mmanno_dup = doc_mm.annset("duplicate_mmanno")
    while annset_mm.size:
        annset_mmanno_first = annset_mm.first()
        annset_mm.remove(annset_mmanno_first)
        for i in annset_mm:
            while annset_mmanno_first.iswithin(i) or annset_mmanno_first.iscovering(i) or annset_mmanno_first.iscoextensive(i):
                annset_mmanno_dup.add_ann(i, i.id)
                annset_mm.remove(i)
                break
            break
    annset_mm = tmp3.copy()
    annset_mm.remove(annset_mmanno_dup)
    # ----------------------------------    

    annset_mm_tk =0

    for i in annset_mm:
        for j in annset_whole_tk:
            if i.iscovering(j) or i.iswithin(j):
                annset_mm_mapping_tk.add_ann(j)
                annset_mm_tk += 1
    tmp = annset_mm_mapping_tk.copy()
    # ------------annset_mm_mapping_tk 前處理---------------
    mm_duplicate = 0
    annset_mm_dup = doc_mm.annset("duplicate_mmtk")
    while annset_mm_mapping_tk.size:
        annset_mmtki_first = annset_mm_mapping_tk.first()
        annset_mm_mapping_tk.remove(annset_mmtki_first)
        for i in annset_mm_mapping_tk:
            while annset_mmtki_first.iswithin(i) or annset_mmtki_first.iscovering(i) or annset_mmtki_first.iscoextensive(i):
                annset_mm_dup.add_ann(i, i.id)
                annset_mm_mapping_tk.remove(i)
                break
            break 
    annset_mm_mapping_tk = tmp.copy()
    annset_mm_mapping_tk.remove(annset_mm_dup)
    # ----------------------------------

    # 系統標注的
    doc_target = Document.load(input_path)
    # 系統標注的 annotation set
    annset_target = doc_target.annset('')
    tmp2 = annset_target.copy()
    # ----------annset_target 前處理-------------
    
    annset_tgano_dup = doc_target.annset("duplicate_tg_anno")
    while annset_target.size:
        annset_tg_first = annset_target.first()
        annset_target.remove(annset_tg_first)
        for i in annset_target:
            while annset_tg_first.iswithin(i) or annset_tg_first.iscovering(i) or annset_tg_first.iscoextensive(i):
                annset_tgano_dup.add_ann(i, i.id)
                annset_target.remove(i)
                break
            break

    annset_target = tmp2.copy()
    
    annset_target.remove(annset_tgano_dup)
    # ----------------------------------

    # 文本共幾個 token
    text_all_tk = annset_whole_tk.size

    # 系統標注的 annotation set 透過 mm 轉成 token
    # 算出共標注幾個 tk (mm base)
    annset_target_tk = 0
    annset_target_tk2 = doc_target.annset("tgtk")
    
    for ann_t in annset_target:
        for ann_m in annset_mm_mapping_tk:
            if ann_t.iscovering(ann_m) or ann_t.iswithin(ann_m):
                annset_target_tk2.add_ann(ann_m)
                annset_target_tk += 1
                
    tmp4 = annset_target_tk2.copy()
    # annset_tg_tk2_orgset2 = annset_target_tk2.copy()
    # ----------annset_target_tk2 前處理------------------
    target_duplicate = 0
    annset_tg_dup = doc_target.annset("duplicate_tg")
    
    while annset_target_tk2.size:
        annset_tgtk2_first = annset_target_tk2.first()
        annset_target_tk2.remove(annset_tgtk2_first)
        for i in annset_target_tk2:
            while annset_tgtk2_first.iswithin(i) or annset_tgtk2_first.iscovering(i) or annset_tgtk2_first.iscoextensive(i):
                annset_tg_dup.add_ann(i, i.id)
                annset_target_tk2.remove(i)
                break
            break
    annset_target_tk2 = tmp4.copy()
    annset_target_tk2.remove(annset_tg_dup)
    
    # ----------------------------------
    
    # 黃金準則標注的 annotation set 轉成 token
    # annset_gold_tk = 0 
    # for i in annset_gold:
    #     for j in annset_tk:
    #         if i.iscovering(j):
    #             annset_gold_tk += 1
    annset_gold_tk = 0 
    annset_gold_tk2 = doc_gold.annset("goldtk")

    for i in annset_gold:
        for j in annset_mm_mapping_tk:
            if i.iscovering(j) or i.iswithin(j):
                annset_gold_tk2.add_ann(j.copy())
                annset_gold_tk += 1
    # print("annset_gold_tk", annset_gold_tk)
    
    
    annset_score = doc_target.annset("score")
    score = 0

    

    # 計分區
    for i in annset_target_tk2:
        for j in annset_gold_tk2:
            if i.iscoextensive(j):
                annset_score.add_ann(i.copy())
                score += 1

    score_tk = 0
    for i in annset_score:
        for j in annset_mm_mapping_tk:
            if i.iscovering(j) or i.iswithin(j):
                score_tk += 1

    # ----------annset_score 前處理------------------
    score_duplicate = 0
    tmp5 = annset_score.copy()
    annset_sc_dup = doc_target.annset("duplicate")
    annset_score_original = annset_score.size #共有幾個（含重複）
    while annset_score.size:
        annset_score_first = annset_score.first()
        annset_score.remove(annset_score_first)
        for i in annset_score:
            while annset_score_first.iswithin(i) or annset_score_first.iscovering(i) or annset_score_first.iscoextensive(i):
                annset_sc_dup.add_ann(i, i.id)
                annset_score.remove(i)
                break
            break
    annset_score = tmp5.copy()
    annset_score.remove(annset_sc_dup)
    # annset_score_cali = annset_score_original - annset_sc_dup.size
    # ----------------------------------
    
    print("黃金準則token(對照mm)", annset_gold_tk2.size, "系統標註筆數(對照mm 不重複)", annset_target_tk2.size-math.sqrt(annset_target_tk2.size), "標註得分token", annset_score_original,
    "校正後得分：", annset_score.size,)
    
    if annset_gold_tk is not 0 and annset_target_tk2.size is not  0:
        print("Precision:", round ((annset_score.size / (annset_target_tk2.size-math.sqrt(annset_target_tk2.size))*100), 2), "Recall:", round ((annset_score.size / annset_gold_tk2.size*100), 2))
        # 寫入報告
        f = open("Clinical_Note/Result/"+str(patient_id)+'_result.csv', 'a')
        str_in = str(start_date)+","+str(num_of_day)
        f.writelines(str_in)

        if round ((annset_score_original*2 / (annset_target_tk2.size-math.sqrt(annset_target_tk2.size))*100), 2) > 100:
            res_p = 100
        else:
            res_p = round ((annset_score_original*2 / (annset_target_tk2.size-math.sqrt(annset_target_tk2.size))*100), 2)
        
        if round ((annset_score.size / annset_gold_tk2.size*100), 2) > 100:
            res_r = 100
        else:
            res_r = round ((annset_score.size / annset_gold_tk2.size*100), 2)

        str_in = ","+ str(res_p)+ ","+ str(res_r)+'\n'
        f.writelines(str_in)
        
