from setuptools import setup


setup(
    name='pygrep',
    version='0.1',
    description='A wrapper to the Youtube Data API',
    author='Daniel Duong',
    license='MIT',
    py_modules=['pygrep'],
    entry_points={
        'console_scripts': [
            'grepfunc = pygrep:grepfunc',
        ],
    }
)
