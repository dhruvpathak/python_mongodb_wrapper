# python_mongodb_wrapper
A simple mongodb wrapper class for pymongo driver.
It provides simple interface over pymongo to connect to a mongodb deployment (single,master-slave or replica sets),
and use the data.
The class uses Borg pattern to emulate singleton behaviour and hence reuses the connections in 
multiple instances.
In pymongo, the connection pooling is done internally by the driver.



- Setup initial sample data using sample_data.txt file ( Optional )

```javascript
mongoimport -d school_db -c students
```

- You can then use mongowrapper class in any of your python code to connect and use the data.
Usage
```python
from mongo_wrapper import MongoWrapper

students_collection = MongoWrapper().get_mongo_collection(server_key='my_replica_set',database='school_db',collection_name='students')
for student in students_collection.find():
    print(student)
```    
