from elasticsearch import Elasticsearch

es = Elasticsearch('localhost:9200')

doc = {
            "query": {
                "match": {
                    "content": "陕西省榆林市中级人民法院 民事判决书 （2017）陕08民终3845号"
                }
            }
        }
                    

res = es.search(index="legalsearch",doc_type="doc_type_test",body=doc)

print(res)