from yattag import Doc, indent
from mytool import compare
import text_txt_position as tp
from shutil import copyfile

doc, tag, text = Doc().tagtext()

patientID = 80001
start_date = 5
num_of_day = 1
def annotate(patientID, start_date, num_of_day,):
    """做標注，冰柱完後會將結果輸出至 Clinical_Note/80001/output_annotated

    Args:
        patientID (int): 輸入欲標注的病人ID
        start_date (int): 起始天數
        num_of_day (int): 回搠幾天
    """

    # 要使用的標注檔案 複製一份到 tmp 資料夾內
    input_for_anno_path = 'Clinical_Note/'+str(patientID)+'/output/'+str(start_date)+'_o.txt'
    tmp_for_anno_path = 'Clinical_Note/'+str(patientID)+'/tmp/tmp_'+str(patientID)+'_'+str(start_date)+'_'+str(num_of_day)+'.txt'
    copyfile(input_for_anno_path, tmp_for_anno_path)

    #  --- 檢查檔案長度 ---
    file = open(input_for_anno_path, "r")
    data = file.read()
    end_node = len(data)
    file.close()
    #  --------------------

    # id 從1開始遞增
    id = 1

    # 標注完的 xml 檔案輸出位置
    after_anno_output_path = 'Clinical_Note/'+str(patientID)+'/output_annotated/'+str(start_date)+'_'+str(num_of_day)+'_annotated.xml'
    # input file 中的全部text
    content = ""

    content_anno = ""
    # 測試用
    # list_for_annotate = compare.concept_id(80001, 5, 1, )
    # 應改寫成
    list_for_annotate = compare.concept_id(patientID, start_date, num_of_day)

    with tag('GateDocument', version="3"):

        # Section 1 start ------------
        with tag('GateDocumentFeatures'):
            with tag('Feature'):
                with tag('Name', className = "java.lang.String"):
                    text('gate.SourceURL')
                with tag('Value', className = "java.lang.String"):
                    text('file'+':/home/feng/桌面/80001/output/2_o.txt')
            with tag('Feature'):
                with tag('Name', className = "java.lang.String"):
                    text('MimeType')
                with tag('Value', className = "java.lang.String"):
                    text('text/plain')
            with tag('Feature'):
                with tag('Name', className = "java.lang.String"):
                    text('docNewLineType')
                with tag('Value', className = "java.lang.String"):
                    text('LF')
        # Section 1 end ------------

        #  Section 2 start ----------
        
        # 此list 為欲標注的詞
        while list_for_annotate:    
            
            print("----------")
            # 呼叫標注器進行標注 回傳
            
            if list_for_annotate[0][1].find(',') is -1:
                # content_anno : 進行標注之後的結果
                # id: +1 之後回傳
                content_anno, id = tp.txt_insert_node(int(list_for_annotate[0][0]), int(list_for_annotate[0][1].split('/')[0]), int(list_for_annotate[0][1].split('/')[1]), tmp_for_anno_path, id, list_for_annotate[0][2].replace('"', ''), )
                # list for annotate 結構為：[[行, 位置, 目標字],[行, 位置, 目標字]]
            else:
                pos_start1 = int(list_for_annotate[0][1].split(',')[0].split('/')[0])
                length1 = int(list_for_annotate[0][1].split(',')[0].split('/')[1])
                content_anno, id = tp.txt_insert_node(int(list_for_annotate[0][0]), pos_start1, length1, tmp_for_anno_path, id, list_for_annotate[0][2].replace('"', ''))
                
                pos_start2 = int(list_for_annotate[0][1].split(',')[1].split('/')[0])
                length2 = int(list_for_annotate[0][1].split(',')[1].split('/')[1])
                content_anno, id = tp.txt_insert_node(int(list_for_annotate[0][0]), pos_start2, length2, tmp_for_anno_path, id, list_for_annotate[0][2].replace('"', '').split(' ')[1])

                    
            del list_for_annotate[0]
        print(content_anno)   
        with tag('TextWithNodes'):
            doc.stag('Node', id = "0" )
            f = open(tmp_for_anno_path, 'r')
            content+=f.read()
            text(content)
            doc.stag('Node', id = end_node)
        
        # Section 2 end ----------

        # Section 3 start ----------
        with tag('AnnotationSet'):
            text(content_anno)
        # Section 3 end ----------


        #  Section 4 start ---------
        with tag('AnnotationSet', Name = "Original markups"):
            with tag('Annotation', Id = "0", Type = "Paragraph", StartNode = "0", EndNode = end_node):
                pass
        #  Section 4 end ----------

    print(doc.getvalue())
    f = open(after_anno_output_path, "w")
    f.write(doc.getvalue())