__author__ = 'Dhruv Pathak'

from django.conf import settings
import pymongo
from pymongo.read_preferences import ReadPreference


class MongoWrapper(object):
    _shared_state = {}
    db_conn_map = {}

    def __init__(self):
        self.__dict__ = self._shared_state

  
    def mongo_db_connect(self, server_key, database, read_preference='PRIMARY_PREFERRED'):
        if self.db_conn_map.get(server_key, {}).get(database, {}).get(read_preference,None) is not None:
 	        return self.db_conn_map[server_key][database][read_preference]

        mongo_server_conf = settings.MONGODB_SERVER_CONF['servers'][server_key]
        connection_read_preference = getattr(ReadPreference,read_preference)

        if mongo_server_conf.get('REPLICA_SET_NAME') is None:
            mongo_conn = pymongo.MongoClient(host=mongo_server_conf['HOST'], read_preference=connection_read_preference, w= 0)
        else:
            mongo_conn = pymongo.MongoReplicaSetClient(host=mongo_server_conf['HOST'], read_preference=connection_read_preference, w=0, replicaSet=mongo_server_conf['REPLICA_SET_NAME'])

        mongo_db = mongo_conn[settings.MONGODB_STORAGE_CONF['databases'][database]]
        self.db_conn_map.setdefault(server_key, {}).setdefault(database,{})[read_preference] = mongo_db

        return mongo_db

    def get_mongo_collection(self, collection_name, database, server_key ):
        mongo_db = self.mongo_db_connect(server_key, database)
        return mongo_db[settings.MONGODB_STORAGE_CONF['collections'][collection_name]]
