from setuptools import setup

required_modules = ['bouncer>=0.1.8', 'Flask>=0.9', 'blinker']

setup(name='flask-bouncer',
      version='0.1.13',
      description='Flask Simple Declarative Authentication based on Ryan Bates excellent cancan library',
      url='http://github.com/jtushman/flask-bouncer',
      author='Jonathan Tushman',
      author_email='jonathan@zefr.com',
      install_requires=required_modules,
      license='MIT',
      py_modules=['flask_bouncer'],
      zip_safe=False,
      platforms='any',
      tests_require=['nose', 'flask-classy>=0.6.10'],
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
