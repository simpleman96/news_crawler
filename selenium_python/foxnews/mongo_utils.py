from pymongo import MongoClient
import traceback


class MongoUtils:
    def __init__(self):
        self.client = MongoClient("localhost", 27011)

    def save_doc(self, db_name, collection_name, key, doc):
        collection = self.client[db_name][collection_name]
        find_collection = collection.find({"key": key})
        if find_collection.count() == 0:
            try:
                collection.insert_one(doc)
                return True
            except Exception:
                traceback.print_exc()
                return False
        else:
            return False

    def check_doc_saved(self, db_name, collection_name, key):
        return self.client[db_name][collection_name].find({"key": key}).count() > 0


# client = MongoUtils()
# client.save_doc("tich_hop_xu_ly_du_lieu", "covid_news_data", "123456", {"key": "123456"})
