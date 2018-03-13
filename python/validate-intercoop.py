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
for data in sys.argv[1:]:
	step("Validating {}", data)
	try:
		validate(ns.load(data), schema)
	except ValidationError as e:
		error("Validation error:\n{}",e)




