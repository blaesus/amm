from distutils.core import setup

setup(
    name='amm',
    version='0.0.1',
    packages=['amm'],
    license='MIT',
    author='Andy Shu',
    author_email='shu@immux.com',
    url='https://github.com/blaesus/amm',
    description='AI model manager',
    long_description=open('README.md').read(),
    install_requires=[
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
