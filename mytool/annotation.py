from mytool import compare
from gatenlp import Document, Annotation


def annotate(anno_list, patient_id, start_date, num_of_day, whether_print = True, anno_specific = False ):
    input_for_anno_path = 'Clinical_Note/'+str(patient_id)+'/output_no_sid/'+str(start_date)+'_o.txt'
    # Load document and create a new anno set
    doc = Document.load(input_for_anno_path)
    annset_target = doc.annset()

    def find_pos(target_string):
        
        if target_string == "V/S":
            f = open(input_for_anno_path, "r")
            tmp_cnt = f.read()
            if tmp_cnt.find("V/S") is not -1:
                
                start_pos = tmp_cnt.find("V/S") +4
                end_pos = tmp_cnt.find("\n", start_pos)
                return start_pos, end_pos
            else:
                return 0, 0

        elif target_string == "Vital signs":
            f = open(input_for_anno_path, "r")
            tmp_cnt = f.read()
            if tmp_cnt.find("Vital signs") is not -1:
                start_pos = tmp_cnt.find("Vital signs") +14
                end_pos = tmp_cnt.find("\n", start_pos)
                return start_pos, end_pos
            else:
                return 0, 0

        elif target_string == "VS Comment":
            f = open(input_for_anno_path, "r")
            tmp_cnt = f.read()
            if tmp_cnt.find("VS Comment") is not -1 or tmp_cnt.find("VS comment") is not -1:
                if tmp_cnt.find("VS Comment") is not -1:
                    start_pos = tmp_cnt.find("VS Comment")+10
                    end_pos = len(tmp_cnt)
                elif tmp_cnt.find("VS comment") is not -1:
                    start_pos = tmp_cnt.find("VS comment")+10
                    end_pos = len(tmp_cnt)
                return start_pos, end_pos
            else:
                return 0, 0
        elif target_string == "P":
            # 先判斷第一行有沒有以S開頭
            f1 = open(input_for_anno_path, "r")
            f2 = open(input_for_anno_path, "r")
            exam_cnt = f1.readline()
            tmp_cnt = f2.read()
            if exam_cnt.find("S:") is not -1:
                if tmp_cnt.find("P:") is not -1:
                    start_pos = tmp_cnt.find("P:") +2
                    # sen_splir = tmp_cmt[tmp_cmt.find("P "):len(tmp_cmt)]
                    end_pos = len(tmp_cnt)
                    return start_pos, end_pos
                else:
                    return 0, 0 
            elif (tmp_cnt.find("Plan") is not -1 )and (tmp_cnt.find("VS comment") is -1 and tmp_cnt.find("VS Comment") is -1):
                    start_pos = tmp_cnt.find("Plan") +4
                    end_pos = len(tmp_cnt)
                    return start_pos, end_pos
                
            else:
                return 0, 0

        else:
            return 0, 0

    # 把位置計算方式轉換
    def rowcol_to_position(line, start_pos, length):
        f = open(input_for_anno_path, "r")
        cur_pos = 0
        # cur_pos = 7
        cur_line = 1
        tmp_content = f.readline()
        

        # 一直執行迴圈，讀入新行
        while True:
            if tmp_content:

                if(line == 1):
                    break

                elif(cur_line < line):
                    cur_pos += len(tmp_content)
                    cur_line += 1
                    tmp_content = f.readline()    
                    
                else:
                    break   
            else:
                break
        start_pos = start_pos + cur_pos
        end_pos = start_pos + length
        return start_pos, end_pos
    #------end of rowcol 2 position------ 


    # 把anno list 中的元素都標註完
    while anno_list:
        # 判斷是否只有一個span
        if anno_list[0][1].find(';') is not -1:
            
            # anno_list[0][1].replace(';', ',')
            pos_start1 = int(anno_list[0][1].split(';')[0].split('/')[0])
            len1 = int(anno_list[0][1].split(';')[0].split('/')[1])
            start_pos1, end_pos1 = rowcol_to_position(int(anno_list[0][0]) ,pos_start1, len1)
            annset_target.add(start_pos1, end_pos1, "New Info")

            pos_start2 = int(anno_list[0][1].split(';')[1].split('/')[0])
            len2 = int(anno_list[0][1].split(';')[1].split('/')[1])
            start_pos2, end_pos2 = rowcol_to_position(int(anno_list[0][0]) ,pos_start2, len2)
            annset_target.add(start_pos2, end_pos2, "New Info")


        elif anno_list[0][1].find(',') is -1:
            # 行 = int(anno_list[0][0])
            # 頭位置  = int(anno_list[0][1].split('/')[0])
            # vary 長度 = int(anno_list[0][1].split('/')[1])
            start_pos, end_pos = rowcol_to_position(int(anno_list[0][0]), int(anno_list[0][1].split('/')[0]), int(anno_list[0][1].split('/')[1]))
            annset_target.add(start_pos, end_pos, "New Info")
        elif (anno_list[0][1].find(',') is not -1) and (anno_list[0][1].find('[') is not -1):
            info_process = anno_list[0][1].replace('[', '',2).replace(']', '',2)
            pos_start1 = int(info_process.split(',')[0].split('/')[0])
            len1 = int(info_process.split(',')[0].split('/')[1])
            start_pos1, end_pos1 = rowcol_to_position(int(anno_list[0][0]) ,pos_start1, len1)
            annset_target.add(start_pos1, end_pos1, "New Info")

            pos_start2 = int(info_process.split(',')[1].split('/')[0])
            len2 = int(info_process.split(',')[1].split('/')[1])
            start_pos2, end_pos2 = rowcol_to_position(int(anno_list[0][0]) ,pos_start2, len2)
            annset_target.add(start_pos2, end_pos2, "New Info")

        else :#(anno_list[0][1].find(',') is not -1):
            pos_start1 = int(anno_list[0][1].split(',')[0].split('/')[0])
            len1 = int(anno_list[0][1].split(',')[0].split('/')[1])
            start_pos1, end_pos1 = rowcol_to_position(int(anno_list[0][0]) ,pos_start1, len1)
            annset_target.add(start_pos1, end_pos1, "New Info")

            pos_start2 = int(anno_list[0][1].split(',')[1].split('/')[0])
            len2 = int(anno_list[0][1].split(',')[1].split('/')[1])
            start_pos2, end_pos2 = rowcol_to_position(int(anno_list[0][0]) ,pos_start2, len2)
            annset_target.add(start_pos2, end_pos2, "New Info")

        del anno_list[0]
    if anno_specific:
        s, e = find_pos("P")
        if (s is not 0) or (e is not 0):
            annset_target.add(s, e, "New Info")    
        s, e = find_pos("VS Comment")
        if (s is not 0) or (e is not 0):
            annset_target.add(s, e, "New Info") 
        s, e = find_pos("V/S")
        if (s is not 0) or (e is not 0):
            annset_target.add(s, e, "New Info") 
        s, e = find_pos("Vital signs")
        if (s is not 0) or (e is not 0):
            annset_target.add(s, e, "New Info")     


    if whether_print:
        print("標注結果為：", annset_target)
    save_path = 'Clinical_Note/'+str(patient_id)+'/annotated/'+str(start_date)+'_'+str(num_of_day)+'.bdocjs'
    doc.save(save_path)
    print("annotate complete!"+ str(patient_id), str(start_date), str(num_of_day))
# 當作比較的基底
def annotate_all(patient_id, start_date):
    pass