#!/usr/bin/env python
#
# __COPYRIGHT__
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY
# KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
# WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

__revision__ = "__FILE__ __REVISION__ __DATE__ __DEVELOPER__"

"""
Test how we handle symlinks in end-cases.
"""

import os
import string

import TestSCons

test = TestSCons.TestSCons()

if not hasattr(os, 'symlink'):
    print "No os.symlink() method, no symlinks to test."
    test.no_result(1)

foo_obj = 'foo' + TestSCons._obj

test.write('SConstruct', """
Program('foo.c')
""")

test.write('foo.c', """\
#include "foo.h"
""")

test.symlink('nonexistent', 'foo.h')

test.run(arguments = '.',
         status = 2,
         stderr = None)

expect = "scons: *** [%s] Error 1\n" % foo_obj
test.fail_test(string.find(test.stderr(), expect) == -1)

test.write('SConstruct', """
Command('file.out', 'file.in', Copy('$TARGET', '$SOURCE'))
""")

test.symlink('nonexistent', 'file.in')

test.run(arguments = '.',
         status = 2,
         stderr = "scons: *** Source `file.in' not found, needed by target `file.out'.  Stop.\n")

test.pass_test()