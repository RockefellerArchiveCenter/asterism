from setuptools import setup

setup(name='asterism',
      version='0.1',
      description='Helpers for Project Electron infrastructure',
      url='http://github.com/RockefellerArchiveCenter/asterism',
      author='Rockefeller Archive Center',
      author_email='archive@rockarch.org',
      install_requires=['djangorestframework', 'django', 'psycopg2'],
      license='MIT',
      packages=['asterism'],
      test_suite='nose.collector',
      tests_require=['nose', 'django', 'djangorestframework', 'psycopg2'],
      zip_safe=False)
