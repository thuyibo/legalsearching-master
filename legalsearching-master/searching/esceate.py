from elasticsearch import Elasticsearch
es = Elasticsearch('localhost:9200')

mappings = {
            "mappings": {
                "type_doc_test": {
                    "properties": {
                        "path": {
                            "type": "keyword",
                            "index": True
                        },
                        "content": {
                            "type": "text",
                            "index": True
                        }
                    }
                }
            }
        }

res = es.indices.create(index = 'legalsearch',body =mappings)