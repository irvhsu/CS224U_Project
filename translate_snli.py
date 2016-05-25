import json
from pprint import pprint
from googleapiclient.discovery import build
import googleapiclient
import time

service = build('translate', 'v2',
            developerKey='AIzaSyCfYvtNzW5YuMXfi7J-QZfGpXdUE4M4Euc')

def execute_gt(source, target, query):
    trans = service.translations().list(
              source=source,
              target=target,
              q=query
            ).execute()
    return [trans['translations'][i]['translatedText'] for i in xrange(len(trans['translations']))]
#    return [trans['translations'][0]['translatedText'], trans['translations'][1]['translatedText']]

def get_para(lang, data):
    trans = execute_gt('en', lang, data)
    para = execute_gt(lang, 'en', trans)
    return para
 
def is_same(orig, para):
    if orig[0] == para[0] and orig[1] == para[1]: return True
    return False 

count = 0
lines_read = 0
f = open('train_para.jsonl', 'a')
with open('snli_1.0/snli_1.0_train.jsonl') as data_file:
    for line in data_file:
        lines_read += 1
        if lines_read < 75800:
            continue
        if count % 100 == 0:
            print("Count " + str(count)) 
        data = json.loads(line)
        if data['gold_label'] != 'entailment':
            continue
        data = [data['sentence1'], data['sentence2']]
        es_para = get_para('es', data)
        fr_para = get_para('fr', data)
        if not is_same(data, es_para):
            f.write(str({'sentence1': es_para[0], 'sentence2': es_para[1]}) + '\n')
        if not is_same(data, fr_para) and not is_same(es_para, fr_para):
            f.write(str({'sentence1': fr_para[0], 'sentence2': fr_para[1]}) + '\n')
        count += 1
f.close()
            

count = 0
lines_read = 0
with open('train_para.jsonl', 'a') as f:
    with open('snli_1.0/snli_1.0_train.jsonl') as data_file:
        for line in data_file:
            while True:
                lines_read += 1
                if lines_read < 417550:
                    break
                # print lines_read, count, line
                if count % 10 == 0:
                    print("Count " + str(count)) 
                
                try:
                    data = json.loads(line)
                    if data['gold_label'] != 'entailment':
                        break
                    data = [data['sentence1'], data['sentence2']]
                    es_para = get_para('es', data)
                    fr_para = get_para('fr', data)
                    if not is_same(data, es_para):
                        f.write(str({'sentence1': es_para[0], 'sentence2': es_para[1]}) + '\n')
                    if not is_same(data, fr_para) and not is_same(es_para, fr_para):
                        f.write(str({'sentence1': fr_para[0], 'sentence2': fr_para[1]}) + '\n')
                except googleapiclient.errors.HttpError as err:
                    if err.resp.status in [403, 500, 503]:
                        print(err)
                        time.sleep(1)
                        continue
                    else: raise
                count += 1
                break 

    f.close()