from distutils.core import setup
import py2exe

import sys; sys.argv.append('py2exe')

py2exe_options = dict(
                      excludes=['_ssl','pyreadline', 'doctest','optparse', 'pickle','email'],
                      dll_excludes=['msvcr71.dll'],  # Exclude msvcr71
                      compressed=True,  # Compress library.zip
					  optimize=2
                      )

setup(
    windows = [
        {
            "script": "gui.py",                     ### Main Python script    
            "icon_resources": [(0, "icon.ico")]     ### Icon to embed into the PE file.
        }
    ],
) 