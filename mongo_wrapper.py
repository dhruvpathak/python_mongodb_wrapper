__author__ = "Dhruv Pathak"

from django.conf import settings
from pymongo.read_preferences import ReadPreference
from pymongo import MongoClient


class MongoWrapper(object):
    _shared_state = {}
    db_conn_map = {}

    def __init__(self):
        self.__dict__ = self._shared_state


    def mongo_db_connect(self,server_key,database):
        if self.db_conn_map.get(server_key, {}).get(database, None) is not None:
            return self.db_conn_map[server_key][database]

        mongo_server_conf = settings.MONGODB_COMBINED_STORAGE_CONF['server_sets'][server_key]
        if mongo_server_conf.get('REPLICA_SET_NAME') is None:
            mongo_conn = MongoClient(host=mongo_server_conf['HOST'], read_preference=ReadPreference.PRIMARY_PREFERRED)
        else:
            mongo_conn = MongoClient(host=mongo_server_conf['HOST'], replicaset=mongo_server_conf['REPLICA_SET_NAME'], read_preference=ReadPreference.PRIMARY_PREFERRED)

        if database not in settings.MONGODB_COMBINED_STORAGE_CONF['db_collections']:
            raise Exception(u"'{0}' is not a predefined database".format(database))

        mongo_db = mongo_conn[database]
        self.db_conn_map.setdefault(server_key, {})[database] = mongo_db
        return mongo_db

    def get_mongo_collection(self, collection_name, database, server_key):
        mongo_db = self.mongo_db_connect(server_key, database)
        if collection_name not in settings.MONGODB_COMBINED_STORAGE_CONF['db_collections'][database]:
            raise Exception(u"'{0}' is not a predefined collection in '{1}' database".format(collection_name,database))
        return mongo_db[collection_name]


