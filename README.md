##SA-FLASK-RESTFUL-RESOURCE

###Finally creating Api resources from sqlalchemy models is easy again!!!

to use: 

```bash
$ pip install sa-flask-restful-resource
```

then define your models, app and create the resource,
just pass your model when you register it with the api 
with a dict as a keyword arg called `resource_class_kwargs`

```python
from sqlalchemy.ext.declarative import declarative_base
from flask import Flask
from flask_restful import Api
from sa_flask_restful_resource import BaseResource

base = declarative_base()

class MyModel(base):
    pass

app = Flask(__name__)
api = Api(app)

class ModelResource(BaseResource):
    pass

api.add_resource(ModelResource,'/myresource',resource_class_kwargs=dict(model=MyModel))

app.run()

```

for more detailed usage, see the demo and test files.
