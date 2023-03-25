from setuptools import setup, find_packages

setup(
    name='fastQuast',
    version='1.0.2',
    description='Fast and simple Quality Assessment Tool for Large Genomes',
    author='Aleksey Komissarov',
    author_email='ad3002@gmail.con',
    url='https://github.com/aglabx/fastQuast',
    packages=find_packages(),
    install_requires=[
    ],
    license='MIT',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    entry_points={
        'console_scripts': [
            'fastQuast=fastQuast.fastQuast:main',
            'fastquast=fastQuast.fastQuast:main',
        ],
    },
)