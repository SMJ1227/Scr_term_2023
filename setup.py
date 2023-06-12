from distutils.core import setup

setup(
    name='exchange_program',
    version='1.0',
    py_modules=['noti', 'teller', 'term'],
    package_data={'': ['*.png']},
)