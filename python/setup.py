#!/usr/bin/env python
from setuptools import setup, find_packages

readme = open("README.md").read()

setup(
	name = "intercoop",
	version = "0.2",
	description =
		"Intercooperation library",
	author = "Som Energia SCCL",
	author_email = "info@somenergia.coop",
	url = 'https://github.com/Som-Energia/intercoop',
	long_description = readme,
	license = 'GNU Affero General Public License v3 or later (AGPLv3+)',
	packages=find_packages(exclude=['*[tT]est*']),
	scripts=[
		'api-example-somacme.py',
		'portal-example-somillusio.py',
		'validate-intercoop.py',
		],
	install_requires=[
		'pycrypto',
		'yamlns>=0.6',
		'requests',
		'requests-mock',
		'flask',
		'jsonschema<3',
		'erppeek',
#		'qrcode',
#		'lxml',
#		'qrtools',
#		'zbar',
	],
	include_package_data = True,
	test_suite = 'intercoop',
	classifiers = [
		'Programming Language :: Python',
		'Programming Language :: Python :: 2',
		'Programming Language :: Python :: 3',
		'Topic :: Software Development :: Libraries :: Python Modules',
		'Intended Audience :: Developers',
		'Development Status :: 4 - Beta',
		'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',
		'Operating System :: OS Independent',
	],
)

