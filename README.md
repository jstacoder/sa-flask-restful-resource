##SA-FLASK-RESTFUL-RESOURCE

###Finally creating Api resources from sqlalchemy models is easy again!!!

to use: 

```bash
$ pip install sa-flask-restful-resource
```

then just define:
* your models
* your app 
* and create / register the resource
    * pass your model to your Api when you register it
    * pass it as a keyword arg called `resource_class_kwargs`

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

now you have these routes defined: 

    `'/myresource' -> GET(get all resources),POST(create a new resource)`
    `'/myresource/<int:item_id>' -> GET(get resource identifed by item_id)`

this is a work in progress, pull requests are welcome, 
i plan on adding more automatic routes in the future. 


for more detailed usage, see the demo and test files.
