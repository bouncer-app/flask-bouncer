from setuptools import setup

required_modules = ['bouncer', 'Flask>=0.9']

setup(name='flask-bouncer',
      version='0.0.1',
      description='Flask Simple Declarative Authentication based on Ryan Bates excellent cancan library',
      url='http://github.com/jtushman/flask-bouncer',
      author='Jonathan Tushman',
      author_email='jonathan@zefr.com',
      install_requires=required_modules,
      license='MIT',
      py_mocdules=['flask_bouncer'],
      zip_safe=False,
      platforms='any',
      tests_require=['nose'],
      test_suite='nose.collector',
      classifiers=[
          'Environment :: Web Environment',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: BSD License',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
          'Topic :: Software Development :: Libraries :: Python Modules'
      ])