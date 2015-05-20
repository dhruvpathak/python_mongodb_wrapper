MONGODB_STORAGE_CONF = {
     'server_sets' : {
        'my_replica_set': {
            'HOST':'FIRST_IP:FIRST_PORT,SECOND_IP:SECOND_PORT',
            'REPLICA_SET_NAME':'my_replica_set_name'
        },

    },
    'db_collections':{
        'school_db':['students'],
    },
}
