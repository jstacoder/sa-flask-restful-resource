from setuptools import setup


setup_requires = [
    'aniso8601==1.0.0',
    'Flask==0.10.1',
    'Flask-RESTful==0.3.3',
    'itsdangerous==0.24',
    'Jinja2==2.7.3',
    'MarkupSafe==0.23',
    'pytz==2015.4',
    'six==1.9.0',
    'SQLAlchemy==1.0.4',
    'Werkzeug==0.10.4',
]
tests_require = [
    'twill==1.8.0',
    'nose==1.3.7',
    'Flask-Testing==0.4.2',
    'fake-factory==0.5.1',
]
install_requires = setup_requires

setup(
    name="sa-flask-restful-resource",
    version="0.0.2",
    setup_requires=setup_requires,
    install_requires=install_requires,
    tests_require=tests_require,
    test_suite="demo.tests",
    description="base class for sqlalchemy and flask-restless",
    long_description="base class for building apis with sqlalchemy and flask-restless",
)
