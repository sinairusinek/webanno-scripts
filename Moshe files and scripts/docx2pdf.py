#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import subprocess
import re
"""
this module can run as a standalone applocation
to use the libreoffice convertion functionality as a subprocess
and convert the files provided to pdf
call the convert_to() function with the output folder and the input file
"""

#############################################################
def convert_to(folder, source, timeout=None):
    args = [libreoffice_exec(), '--headless', '--convert-to', 'pdf', '--outdir', folder, source]

    try:
        process = subprocess.call(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return "pdf"
    except:
        raise ValueError("convertion failed!")

#############################################################

#############################################################
def libreoffice_exec():
    if sys.platform == 'darwin':
        return '/Applications/LibreOffice.app/Contents/MacOS/soffice'
    return 'libreoffice'
#############################################################

#############################################################
class LibreOfficeError(Exception):
    def __init__(self, output):
        self.output = output
