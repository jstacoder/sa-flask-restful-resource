from flask import Flask,current_app
from flask_restful import Api,fields,reqparse
from sqlalchemy import create_engine,orm
from sqlalchemy.ext.declarative import declarative_base
from sa_flask_restful_resource import BaseResource
import sqlalchemy as sa
import os
import sys

sys.path.insert(0,os.path.realpath(os.path.dirname(__file__)))

app = Flask(__name__)
api = Api(app)

os.environ.setdefault('APP_CONFIG','todo_config.ProdConfig')
app.config.from_object(os.environ.get('APP_CONFIG'))

engine = create_engine(app.config.get('DATABASE_URI'),echo=True)
session = orm.scoped_session(orm.sessionmaker(bind=engine))()
base = declarative_base()
base.session = session

class Todo(base):
    __tablename__ = 'todos'

    id = sa.Column(sa.Integer,primary_key=True)
    name = sa.Column(sa.String(255))
    description = sa.Column(sa.Text)
    date_added = sa.Column(sa.DateTime,default=sa.func.now())
    project_id = sa.Column(sa.Integer,sa.ForeignKey('projects.id'))

class Project(base):
    __table_args__ = (
        (sa.UniqueConstraint('id','name')),
    )
    __tablename__ = 'projects'

    id = sa.Column(sa.Integer,primary_key=True)
    name = sa.Column(sa.String(255))
    todos = sa.orm.relation('Todo',lazy='dynamic',backref=orm.backref('project'))

todo_fields = {
    'id':fields.Integer,
    'name':fields.String,
    'description':fields.String,
    'date_added':fields.DateTime,
    'project_id':fields.Integer
}

proj_fields = {
    'id':fields.Integer,
    'name':fields.String,
    'todos':fields.List(fields.Nested(todo_fields))
}

todo_parser = reqparse.RequestParser()
todo_parser.add_argument('name',type=str,location='form')
todo_parser.add_argument('description',type=str,location='form')

proj_parser = reqparse.RequestParser()
proj_parser.add_argument('name',type=str,location='form')
proj_parser.add_argument('todos',type=list,location='form')

class Task(BaseResource):
    pass

class Proj(BaseResource):
    pass

api.add_resource(
        Task, 
        '/todo',
        '/todo/<int:item_id>',
        resource_class_kwargs = dict(
            model = Todo,
            fields = todo_fields,
            parser = todo_parser,
            make_model = lambda args:Todo(
                name = args.name,
                description = args.description
            )
        )
)

api.add_resource(
        Proj,
        '/project',
        '/project/<int:item_id>',
        resource_class_kwargs = dict(
            model = Project,
            fields = proj_fields,
            parser = proj_parser,
            make_model = 
            lambda args: Project(
                name = args.name
            )
        )
)

if __name__ == "__main__":
    app.run(port=4455,debug=True)
        
