from flask_restful import Resource,fields,reqparse,marshal
from functools import wraps
import os

def late_marshal(f):
    @wraps(f)
    def wrapper(self,*args,**kwargs):
        return marshal(f(self,*args,**kwargs),self.model_fields)
    return wrapper

class BaseResource(Resource):
    models = {}
    make_model = {}
    parsers = {}

    def __init__(self,model=None,session=None,fields=None,parser=None,make_model=None,*args,**kwargs):
        self.model = model
        self.model_name = model.__name__.lower()
        BaseResource.models[self.model_name] = self.model
        BaseResource.make_model[self.model_name] = make_model
        BaseResource.parsers[self.model_name] = parser
        self.session = session
        BaseResource.session = self.session
        self.__class__.model_name = self.model_name
        self.model_fields = fields
        
        super(BaseResource,self).__init__(*args,**kwargs)

    @late_marshal
    def get(self,item_id=None):
        return self._get(item_id)

    @late_marshal
    def post(self):
        return self._post()

    @classmethod
    def get_model(cls,model,model_id):
        return cls.session.query(cls.models[model]).get(model_id)

    @classmethod
    def get_models(cls,model):
        return cls.session.query(cls.models[model]).all()

    def _get_model(self,model_id):
        return self.session.query(self.model).get(model_id)

    def _get_models(self):
        return self.session.query(self.model).all()

    def _get(self,mid=None):
        return self._get_models() if mid is None else self._get_model(mid)
   
    def _post(self):
        args = self.parsers[self.model_name].parse_args()        
        model_instance = self.make_model[self.model_name](args)
        self.session.add(model_instance)
        self.session.commit()
        return model_instance

