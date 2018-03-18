#!/usr/bin/env python

from jsonschema import validate
from jsonschema.exceptions import ValidationError
from yamlns import namespace as ns
from consolemsg import step, error
import os
import sys

def local(filename):
	return os.path.join(os.path.dirname(os.path.abspath(__file__)),filename)

step("Loading schema")
schema = ns.load(local("../peerdescriptor-schema.yaml"))
for yamlfile in sys.argv[1:]:
	step("Validating {}", yamlfile)
	try:
		validate(ns.load(yamlfile), schema)
	except ValidationError as e:
		error(
			"Validation error at {filename}#/{path}:\n"
			"{msg}",
			filename=yamlfile,
			path='/'.join(format(x) for x in e.path),
			msg=e.message,
			)





