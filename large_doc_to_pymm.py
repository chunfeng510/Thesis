import sys
import traceback
from pymm import Metamap
mm = Metamap('/home/feng/public_mm/bin/metamap')
mmos = mm.parse(['John had a huge heart attack and fever', 'I am cold'])


def read_lines(file_name, fast_forward_to, batch_size, preprocessing):
    sentences = list()
    with open(file_name, 'r') as fp:
        for i in range(fast_forward_to):
            fp.readline()

        for idx, line in enumerate(fp):
            sentences.append(preprocessing(line))
            if (idx+1) % batch_size == 0:
                yield sentences
                sentences.clear()


CLINICAL_TEXT_FILE = 1
last_checkpoint = 1
BATCH_SIZE = 1
# clean_text =

try:
    for i, sentences in enumerate(read_lines(CLINICAL_TEXT_FILE, last_checkpoint, BATCH_SIZE, clean_text)):
        timeout = 0.33*BATCH_SIZE
        try_again = False
        try:
            mmos = mm.parse(sentences, timeout=timeout)
        except MetamapStuck:
            # Try with larger timeout
            print("Metamap Stuck !!!; trying with larger timeout")
            try_again = True
        except:
            print("Exception in mm; skipping the batch")
            traceback.print_exc(file=sys.stdout)
            continue

        if try_again:
            timeout = BATCH_SIZE*2
            try:
                mmos = mm.parse(sentences, timeout=timeout)
            except MetamapStuck:
                # Again stuck; Ignore this batch
                print("Metamap Stuck again !!!; ignoring the batch")
                continue
            except:
                print("Exception in mm; skipping the batch")
                traceback.print_exc(file=sys.stdout)
                continue

        for idx, mmo in enumerate(mmos):
            for jdx, concept in enumerate(mmo):
                save(sentences[idx], concept)

        curr_checkpoint = (i+1)*BATCH_SIZE + last_checkpoint
        record_checkpoint(curr_checkpoint)
finally:
    mm.close()
