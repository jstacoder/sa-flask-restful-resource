
class BaseConfig(object):
    SECRET_KEY = 'xxx'

class TestConfig(BaseConfig):
    DATABASE_URI = 'sqlite:///test.db'

class ProdConfig(BaseConfig):
    DATABASE_URI = 'sqlite:///prod.db'
