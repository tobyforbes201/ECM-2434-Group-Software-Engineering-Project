"""This module tests that code is formatted correctly and
adheres to good practice according to pylint."""
import sys
from datetime import datetime
import pylint.lint

def run_pylint_tests():
	"""Run a pylint test to ensure good formatting and coding practice
	has been done throughout the application"""
	pylint_opts = ['--disable=bad-indentation,relative-beyond-top-level',
	'--ignore=migrations', '../polls']
	std_out_origin=sys.stdout
	# output is appended to the test file
	sys.stdout = open("pylint_test_out.txt", "a")
	# state date and time of each test
	print("New Test | Date: "+str(datetime.now()))
	pylint.lint.Run(pylint_opts)
	sys.stdout.close()
	sys.stdout=std_out_origin

run_pylint_tests()
