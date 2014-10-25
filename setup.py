from setuptools import setup

setup(name='freeverse',
    version='0.0.0',
    description='A new way to write free-form, minimalistic specs (tests) in Python that favor natural language',
    url='https://github.com/Kazark/pyfreeverse',
    author='Kazark',
    author_email='kazark@zoho.com',
    license='MIT',
    packages=['freeverse'],
    test_suite='nose.collector',
    tests_require=['nose'],
    zip_safe=False)
