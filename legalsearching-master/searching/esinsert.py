from elasticsearch import Elasticsearch

es = Elasticsearch('localhost:9200')

import os

g = os.walk(r"C:\Users\Yibo\Downloads\数据集") #改成数据集所在的绝对路径，运行需要等待一段时间，稍安勿躁

cnt = 0
for path,dir_list,file_list in g:
    for file_name in file_list:
        fpath = os.path.join(path, file_name)
        if fpath[-3:] == 'xml':
            try:
                f = open(fpath,'r', encoding='UTF-8').read()
            except:
                print(fpath)
            else:
                action = {
                    "path": fpath,
                    "content": f
                }
                es.index(index="legalsearch",doc_type="doc_type_test",body = action)
                cnt += 1
                print(cnt,fpath)
