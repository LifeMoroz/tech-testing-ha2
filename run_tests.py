#!/usr/bin/env python2
import os
import sys
import unittest

if __name__ == '__main__':
    loader = unittest.TestLoader()
    testdir = os.path.abspath(os.path.dirname(__file__)) + '/tests/'
    suite = loader.discover(testdir, pattern='*test.py')
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    sys.exit(not result.wasSuccessful())
