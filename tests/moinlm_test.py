#!/usr/bin/env python

import sys
import os
import unittest
import logging
#import config

log = logging

#outputdir = config.outputdir

class TestImports(unittest.TestCase):
    
    def setUp(self):
        self.funcname = '_'.join(self.id().split('.')[-2:])
            
    def test1(self):
    	import MoinMoin

    def test2(self):
    	import moinlm
    	
    def test3(self):
    	from moinlm.auth import uw_auth

    def test3(self):
    	from moinlm.auth import commandline_auth




