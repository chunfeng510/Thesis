from pymm import Metamap
mm = Metamap('/home/feng/public_mm/bin/metamap')
# mmos = mm.parse(['John had a huge heart attack and fever', 'I am cold'])
txt_file = "clinical_txt/1.txt"


def read_line(txt_file):
    sentences = list()
    with open(txt_file, 'r') as f:
        for i, l in enumerate(f):
            sentences.append(l)
            # print(l)
        lines = i + 1
        return sentences, lines
        # for i in range(lines):
        #     f.readline()


sents, lines = read_line(txt_file)
# 讀出來的句子，存成 list 一句一句儲存

try:
    mmos = mm.parse(sents, timeout=20)
    count = 1
    for idx, mmo in enumerate(mmos):
        count += 1
        for jdx, concept in enumerate(mmo):

            if concept.ismapping == 1:
                print(concept.cui, concept.score,
                      concept.matched, count, concept.matchedstart, concept.matchedend)
                print(concept.semtypes, concept.ismapping,
                      "NEG :"+concept.isnegated)

finally:
    mm.close()
