
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
Test that the $PDFLATEXCOMSTR construction variable allows you to configure
the C compilation output.
"""

import os
import string
import sys
import TestSCons

python = TestSCons.python
_exe   = TestSCons._exe

test = TestSCons.TestSCons()



test.write('mypdflatex.py', r"""
import sys
outfile = open(sys.argv[1], 'wb')
infile = open(sys.argv[2], 'rb')
for l in filter(lambda l: l != '/*latex*/\n', infile.readlines()):
    outfile.write(l)
sys.exit(0)
""")

test.write('SConstruct', """
env = Environment(TOOLS = ['pdflatex'],
                  PDFLATEXCOM = r'%(python)s mypdflatex.py $TARGET $SOURCE',
                  PDFLATEXCOMSTR = 'Building $TARGET from $SOURCE')
env.PDF('test1', 'test1.latex')
""" % locals())

test.write('test1.latex', """\
test1.latex
/*latex*/
""")

test.run(stdout = test.wrap_stdout("""\
Building test1.pdf from test1.latex
""" % locals()))

test.must_match('test1.pdf', "test1.latex\n")



test.pass_test()
