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
"""
Test bin/update-release-info.py.  Also verify that the original files
have the appropriate triggers to cause the modifications.
"""

__revision__ = "__FILE__ __REVISION__ __DATE__ __DEVELOPER__"

import os, sys, time

import TestRuntest

TestSCons      = 'QMTest/TestSCons.py'             .split('/')
README         = 'README'                          .split('/')
ReleaseConfig  = 'ReleaseConfig'                   .split('/')
SConstruct     = 'SConstruct'                      .split('/')
Announce       = 'src/Announce.txt'                .split('/')
CHANGES        = 'src/CHANGES.txt'                 .split('/')
RELEASE        = 'src/RELEASE.txt'                 .split('/')
Main           = 'src/engine/SCons/Script/Main.py' .split('/')
main_in        = 'doc/user/main.in'                .split('/')
main_xml       = 'doc/user/main.xml'               .split('/')

test = TestRuntest.TestRuntest(
                    program = os.path.join('bin', 'update-release-info.py'),
                    things_to_copy = ['bin']
                    )
if not os.path.exists(test.program):
    test.skip_test("update-release-info.py is not distributed in this package\n")

test.run(arguments = 'bad', status = 1)

# Strings to go in ReleaseConfig
combo_strings = [
# Index 0: version tuple with bad release level
"""version_tuple = (2, 0, 0, 'bad', 0)
""",
# Index 1: Python version tuple
"""unsupported_python_version = (2, 3)
""",
# Index 2: Python version tuple
"""deprecated_python_version  = (2, 4)
""",
# Index 3: alpha version tuple
"""version_tuple = (2, 0, 0, 'alpha', 0)
""",
# Index 4: final version tuple
"""version_tuple = (2, 0, 0, 'final', 0)
""",
# Index 5: bad release date
"""release_date = (2011, 12)
""",
# Index 6: release date (hhhh, mm, dd)
"""release_date = (2011, 12, 21)
""",
# Index 7: release date (hhhh, mm, dd, hh, mm, ss)
"""release_date = (2011, 12, 21, 12, 21, 12)
""",
]

combo_error = \
"""ERROR: Config file must contain at least version_tuple,
\tunsupported_python_version, and deprecated_python_version.
"""

def combo_fail(*args, **kw):
    kw.setdefault('status', 1)
    combo_run(*args, **kw)

def combo_run(*args, **kw):
    t = '\n'
    for a in args:
        t += combo_strings[a]

    test.write(ReleaseConfig, t)

    kw.setdefault('stdout', combo_error)
    test.run(**kw)

combo_fail()
combo_fail(0)
combo_fail(1)
combo_fail(2)
combo_fail(0, 1)
combo_fail(0, 2)
combo_fail(1, 2)
combo_fail(0, 1, 2, stdout =
"""ERROR: `bad' is not a valid release type in version tuple;
\tit must be one of alpha, beta, candidate, or final
""")

# We won't need this entry again, so put in a default
combo_strings[0] = combo_strings[1] + combo_strings[2] + combo_strings[3]

combo_fail(0, 5, stdout =
"""ERROR: Invalid release date (2011, 12)
""")

def pave(path):
    path = path[:-1]
    if not path or os.path.isdir(os.path.join(*path)):
        return
    pave(path)
    test.subdir(path)

def pave_write(file, contents):
    pave(file)
    test.write(file, contents)

pave_write(CHANGES, """
RELEASE  It doesn't matter what goes here...
""")

pave_write(RELEASE, """
This file has a 3.2.1.beta.20121221 version string in it
""")

pave_write(Announce, """
RELEASE  It doesn't matter what goes here...
""")

pave_write(SConstruct, """
month_year = 'March 1945'
copyright_years = '2001, 2002, 2003, 2004, 2005, 2006, 2007'
default_version = '0.98.97'
""")

pave_write(README, """
These files are a part of 33.22.11:
        scons-33.22.11.tar.gz
        scons-33.22.11.win32.exe
        scons-33.22.11.zip

        scons-33.22.11.beta.20012122112.suffix
""")

pave_write(TestSCons, """
copyright_years = Some junk to be overwritten
default_version = More junk
python_version_unsupported = Yep, more junk
python_version_deprecated = And still more
""")

pave_write(Main, """
unsupported_python_version = Not done with junk
deprecated_python_version = It goes on forever
""")

pave_write(main_in, """
TODO
""")

pave_write(main_xml, """
TODO
""")

def updating_run(*args):
    stdout = ''
    for file in args:
        stdout += 'Updating %s...\n' % os.path.join(*file)
    combo_run(0, 7, stdout = stdout)

updating_run(CHANGES, RELEASE, Announce, SConstruct, README, TestSCons, Main)

test.must_match(CHANGES, """
RELEASE 2.0.0.alpha.yyyymmdd - NEW DATE WILL BE INSERTED HERE
""", mode = 'r')

test.must_match(RELEASE, """
This file has a 2.0.0.alpha.yyyymmdd version string in it
""", mode = 'r')

test.must_match(Announce, """
RELEASE 2.0.0.alpha.yyyymmdd - NEW DATE WILL BE INSERTED HERE
""", mode = 'r')

years = ', '.join(map(str, range(2001, time.localtime()[0] + 1)))
test.must_match(SConstruct, """
month_year = 'MONTH YEAR'
copyright_years = %s
default_version = '2.0.0.alpha.yyyymmdd'
""" % repr(years), mode = 'r')

test.must_match(README, """
These files are a part of 33.22.11:
        scons-2.0.0.alpha.yyyymmdd.tar.gz
        scons-2.0.0.alpha.yyyymmdd.win32.exe
        scons-2.0.0.alpha.yyyymmdd.zip

        scons-2.0.0.alpha.yyyymmdd.suffix
""", mode = 'r')

# should get Python floors from TestSCons module.
test.must_match(TestSCons, """
copyright_years = '2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011'
default_version = '2.0.0.alpha.yyyymmdd'
python_version_unsupported = (2, 3)
python_version_deprecated = (2, 4)
""", mode = 'r')

# should get Python floors from TestSCons module.
test.must_match(Main, """
unsupported_python_version = (2, 3)
deprecated_python_version = (2, 4)
""", mode = 'r')

#TODO: Release option
#TODO: ==============
#TODO: 
#TODO: Dates in beta/candidate flow
#TODO: 
#TODO: Dates in final flow
#TODO: 
#TODO: Post option
#TODO: ===========
#TODO: 
#TODO: Dates in post flow
#TODO: 
#TODO: Update minor or micro version
#TODO: 
#TODO: ReleaseConfig - new version tuple
#TODO: 
#TODO: CHANGES - new section
#TODO: 
#TODO: RELEASE - new template
#TODO: 
#TODO: Announce - new section

test.pass_test()

# Local Variables:
# tab-width:4
# indent-tabs-mode:nil
# End:
# vim: set expandtab tabstop=4 shiftwidth=4:
