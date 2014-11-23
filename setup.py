from distutils.core import setup
import py2exe, sys, os

setup(
	console = [{
		"script":"ODT2MatlabReadable.py"
        }],
        zipfile = None,
        data_files = None,
        version = "1.0",
        name = "Odt Matlab Readable",
        description = "A converter program for odt files",
        author = "Mitropoulos Spiros",
        license = "GNU GPL 3 License",
        url = "http://www.eyrhka.gr",
)