""" setup.py

    Basic setup file to enable pip install
    
    
"""

from distutils.core import setup
setup(  name='brining',
        version='0.1.3',
        #py_modules=['brining'],
        requires='simplejson',
        packages=['brining'],
        package_dir={'brining': 'brining'},        
        package_data={'brining': ['tests/*.py']},
        description='Python object to/from JSON serialization/deserialization module',
        author='Samuel M Smith',
        author_email='smith.samuel.m@gmail.com',
        url='https://github.com/SmithSamuelM/brine',      
      )

