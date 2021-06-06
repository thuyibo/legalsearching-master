from elasticsearch import Elasticsearch
es = Elasticsearch('localhost:9200')

mappings = {
            "mappings": {
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

res = es.indices.create(index = 'legalsearch',body =mappings)