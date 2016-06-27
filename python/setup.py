#!/usr/bin/env python
from setuptools import setup, find_packages

readme = open("README.md").read()

setup(
	name = "intercoop",
	version = "1.3",
	description =
		"Intercooperation library",
	author = "Som Energia SCCL",
	author_email = "info@somenergia.coop",
	url = 'https://github.com/Som-Energia/somenergia-generationkwh',
	long_description = readme,
	license = 'GNU Affero General Public License v3 or later (AGPLv3+)',
	packages=find_packages(exclude=['*[tT]est*']),
	scripts=[
		'intercoop/apiexample.py',
		],
	install_requires=[
		'pycrypto',
		'yamlns>=0.3', # earlier are not Py2 compatible
		'requests',
		'flask',
	],
	include_package_data = True,
	test_suite = 'intercoop',
#	test_runner = 'colour_runner.runner.ColourTextTestRunner',
	classifiers = [
		'Programming Language :: Python',
		'Programming Language :: Python :: 3',
		'Topic :: Software Development :: Libraries :: Python Modules',
		'Intended Audience :: Developers',
		'Development Status :: 2 - Pre-Alpha',
		'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',
		'Operating System :: OS Independent',
	],
)

