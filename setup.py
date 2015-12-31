# -*- coding: utf-8 -*-

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

try:
    import pypandoc
    readme = pypandoc.convert('README.md', 'rst')
    history = pypandoc.convert('HISTORY.md', 'rst')
except ImportError:
    with open('README.md') as readme_file, open('HISTORY.md') as history_file:
        readme = readme_file.read()
        history = history_file.read()

with open('requirements.txt') as requirements_file:
    requirements = requirements_file.read().splitlines()

test_requirements = [
        'pytest>=2.6.4'
        ]

setup(
        name="urlmon",
        version="0.1.1",
        description="Python script to monitor a webpage for changes.",
        long_description=readme + "\n\n" + history,
        author="Nathan Henrie",
        author_email="nate@n8henrie.com",
        url="https://github.com/n8henrie/urlmon",
        packages=[
            "urlmon",
            ],
        package_dir={"urlmon": "urlmon"},
        include_package_data=True,
        install_requires=requirements,
        license="MIT",
        zip_safe=False,
        keywords="urlmon",
        classifiers=[
            "Natural Language :: English",
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.3",
            "Programming Language :: Python :: 3.4",
            "Programming Language :: Python :: 3.5",
            ],
        test_suite="tests",
        tests_require=test_requirements,
        entry_points={
            'console_scripts': ['urlmon=urlmon.urlmon:_cli']
            }
        )
