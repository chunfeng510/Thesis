from mytool import compare
from gatenlp import Document, Annotation


def annotate(anno_list, patient_id, start_date, num_of_day ):
    input_for_anno_path = 'Clinical_Note/'+str(patient_id)+'/output_no_sid/'+str(start_date)+'_o.txt'
    # Load document and create a new anno set
    doc = Document.load(input_for_anno_path)
    annset_target = doc.annset()

    def rowcol_to_position(line, start_pos, length):
        f = open(input_for_anno_path, "r")
        cur_pos = 0
        # cur_pos = 7
        cur_line = 1
        tmp_content = f.readline()
        # 一直執行迴圈
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
    #------------------- 
    while anno_list:
        # 判斷是否只有一個span
        if anno_list[0][1].find(',') is -1:
            # 行 = int(anno_list[0][0])
            # 頭位置  = int(anno_list[0][1].split('/')[0])
            # vary 長度 = int(anno_list[0][1].split('/')[1])
            start_pos, end_pos = rowcol_to_position(int(anno_list[0][0]), int(anno_list[0][1].split('/')[0]), int(anno_list[0][1].split('/')[1]))
            annset_target.add(start_pos, end_pos, "New Info")
        else:
            pos_start1 = int(anno_list[0][1].split(',')[0].split('/')[0])
            len1 = int(anno_list[0][1].split(',')[0].split('/')[1])
            start_pos1, end_pos1 = rowcol_to_position(int(anno_list[0][0]) ,pos_start1, len1)
            annset_target.add(start_pos1, end_pos1, "New Info")

            pos_start2 = int(anno_list[0][1].split(',')[1].split('/')[0])
            len2 = int(anno_list[0][1].split(',')[1].split('/')[1])
            start_pos2, end_pos2 = rowcol_to_position(int(anno_list[0][0]) ,pos_start2, len2)
            annset_target.add(start_pos2, end_pos2, "New Info")

        del anno_list[0]
    print("標注結果為：", annset_target)
    save_path = 'Clinical_Note/'+str(patient_id)+'/annotated/'+str(start_date)+'_'+str(num_of_day)+'.bdocjs'
    doc.save(save_path)

# 當作比較的基底
def annotate_all(patient_id, start_date):
    pass