# file = open('Clinical_Note/example.txt', 'a+')
# file.seek(5)
# file.write('<Node id="27"/>')
# for l in file:
#     print(l)
# print(file)
from mytool import compare

def txt_insert(line, pos_start, length, file_path, trigger=None,):
    # OPEN FILE
    f = open(file_path, "r")
    cur_pos = 0
    cur_line = 1

    tmp_content = f.readline()
    while True:
        if tmp_content:
            # print(tmp_content)
            if(cur_line < line):
                cur_pos += len(tmp_content)
                cur_line += 1
                tmp_content = f.readline()
                break
                
        else:
            pass
        tmp_content = f.readline()
    print(tmp_content.find(trigger))
    if trigger is not None:
        pos_start =  tmp_content.find(trigger)-length-1
    
    tag_start = cur_pos + pos_start+7
    tag_end = tag_start+length
    f.close()
    f = open(file_path, "r")
    offset = 12
    if (tag_start/100) ==1 and (tag_end/100) ==1:
        offset = 13
    else:
        offset = 12

    content = f.read()
    content = content[:tag_start]+"<Node id="+str(tag_start)+">"+content[tag_start:]
    content = content[:tag_end+offset]+"<Node id="+str(tag_end)+">"+content[tag_end+offset:]
    # 19 就是19，39是27加上12漂移字元，如果是三位數則是加上13漂移
    f = open('Clinical_Note/80001/output/5_o2.txt', "w")
    f.write(content)
    f.close()

# test = compare.concept_id(80001, 5,)
# print(test)
file_path = 'Clinical_Note/80001/output/5_o.txt'
txt_insert(2, 54, 6, file_path, "severe",)