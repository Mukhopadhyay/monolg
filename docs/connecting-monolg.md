# Connecting to MongoDB

Monolg uses `pymongo.MongoClient` under the hood, so connecting to your Mongo instance is very simple. This documentation will guide you about establishing your connection.

## Connecting to your local MongoDB instance
Let's assume that MongoDB is running locally in your system in the default 27017 port. Since that is the default, you won't have to do much, simply

```python
from monolg import Monolg

mlg = Monolg()                              # Defaults to localhost:27017
mlg.connect()                               # Establishes the connection

>>> 10-10-2022 10:10:10 [INFO] [system] monolg connected to mongodb
```

Or alternatively, you can pass in the __host__ and __port__ like so,

```python
mlg = Monolg(host='127.0.0.1', port=27017)  # Passing the host and the port number
```

## Connecting via Connection string

If you have the connectiong string to the MongoDB instance, you can simply pass that while
instantiating the `Monolg` object,

```python
mlg = Monolg('mongodb://localhost:27017')   # Passing in the MongoDB connection string
```

If you need further help writing the connectiong string for you database, refer to this [guide](https://www.mongodb.com/docs/manual/reference/connection-string/) by MongoDB. This might be helpful.

## Instantiating from an existing connection

If you want to establish the connection to mongo yourself, i.e., if you want to have access to the `pymongo.MongoClient` then you can use the `Monolg.from_client` classmethod. Using this you'd be able to use monolg with an existing client.

```python
import pymongo
from monolg import Monolg

mongo_client = pymongo.MongoClient('mongodb://localhost:27017')
mlg = Monolg.from_client(mongo_client)      # Creating monolg instance using existing MongoClient

>>> 10-10-2022 10:10:10 [INFO] [system] monolg connected to mongodb
```

__NOTE__: If we instantiate the `Monolg` class using an existing client, we will not have the freedom of closing (`Monolg.close()`) and then reopening the connection (`Monolg.reopen()`)

```python
import pymongo
from monolg import Monolg

mongo_client = pymongo.MongoClient('mongodb://localhost:27017')
mlg = Monolg.from_client(mongo_client, verbose=True)

mlg.connect()
>>> 10-10-2022 10:10:10 [INFO] [system] monolg connected to mongodb

mlg.close()                                 # Closing the connection
>>> 10-10-2022 10:10:10 [INFO] [system] monolg connection with mongodb closed

mlg.reopen()                                # Attempting to reopen the connection

>>> Traceback (most recent call last):
>>> ...
>>> monolg.errors.ConnectionNotReopened: Cannot re-establishh connection. Object was
>>> instantiated using client. Try instantiating using the constructor.

```
