from setuptools import setup

required_modules = ['bouncer']

setup(name='flask_bouncer',
      version='0.0.1',
      description='Simple Declarative Authentication based on Ryan Bates excellent cancan library',
      url='http://github.com/jtushman/bouncer',
      author='Jonathan Tushman',
      author_email='jonathan@zefr.com',
      install_requires=required_modules,
      license='MIT',
      packages=['flask_abilities'],
      zip_safe=False,
      classifiers=[
          'Environment :: Web Environment',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: BSD License',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
          'Topic :: Software Development :: Libraries :: Python Modules'
      ])