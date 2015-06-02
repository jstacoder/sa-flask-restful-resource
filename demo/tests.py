from flask_testing import TestCase
import os
from sqlalchemy import create_engine,MetaData,orm
from todo import app,Todo,Project,Task,Proj
from flask_restful import marshal
import json
from faker.factory import Factory
import random

faker = Factory().create()

def gen_todo():
    return Todo(name=faker.word(),description=faker.text())

def gen_proj(name):
    return Project(name=name,todos=[gen_todo() for x in range(random.randrange(1,150))])

class BaseTest(TestCase):

    def _create_db(self):
        from todo import engine,session
        Todo.metadata.create_all(engine)
        self.session = session
        self.engine = engine
        names = set([faker.word() for x in range(random.randrange(1,50))])
        [session.add(gen_proj(name)) for name in names]
        session.commit()

    def setUp(self):        
        self.app = self.create_app()
        self.client = self.app.test_client()
        
    def tearDown(self):
        Todo.metadata.drop_all(self.engine)

    def create_app(self):
        os.environ['APP_CONFIG'] = 'todo_config.TestConfig'
        app.config.from_object(os.environ.get('APP_CONFIG'))
        self._create_db()
        return app


class TodoTest(BaseTest):
    def test_all_todos(self):
        res = self.client.get('/todo')
        self.assertEquals(res.content_type,'application/json')
        self.assertEquals(len(json.loads(res.data)),self.session.query(Todo).count())

    def test_each_todo(self):
        ids = [x.id for x in self.session.query(Todo).all()]
        for i in ids:
            res = self.client.get('/todo/{}'.format(i))
            self.assertEquals(json.loads(res.data).get('id'),i)

    def test_add_todo(self):
        todo_args = dict(name='new_test',description='this is a test task')
        res = self.client.post('/todo',data=todo_args)
        self.assertEquals(json.loads(res.data).get('id'),self.session.query(Todo).all()[-1].id)

class ProjectTest(BaseTest):

    def test_app_projects(self):
        res = self.client.get('/project')
        self.assertEquals(res.content_type,'application/json')
        self.assertEquals(len(json.loads(res.data)),self.session.query(Project).count())

    def test_each_project(self):
        ids = [x.id for x in self.session.query(Project).all()]
        for i in ids:
            res = self.client.get('/project/{}'.format(i))
            self.assertEquals(json.loads(res.data).get('id'),i)
    
    def test_add_project(self):
        args = dict(name='new_test',todos=[x.id for x in self.session.query(Todo).all()])
        res = self.client.post('/project',data=args)
        self.assertEquals(json.loads(res.data).get('id'),self.session.query(Project).all()[-1].id)



if __name__ == "__main__":
    from unittest.runner import TextTestRunner
    TextTestRunner().run()
