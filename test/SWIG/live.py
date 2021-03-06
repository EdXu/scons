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
Test SWIG behavior with a live, installed SWIG.
"""

import os.path
import sys

import TestSCons

# swig-python expects specific filenames.
# the platform specific suffix won't necessarily work.
if sys.platform == 'win32':
    _dll = '.dll'
else:
    _dll   = '.so'

test = TestSCons.TestSCons()

swig = test.where_is('swig')
if not swig:
    test.skip_test('Can not find installed "swig", skipping test.\n')

python, python_include, python_libpath, python_lib = \
             test.get_platform_python_info()
Python_h = os.path.join(python_include, 'Python.h')
if not os.path.exists(Python_h):
    test.skip_test('Can not find %s, skipping test.\n' % Python_h)

# handle testing on other platforms:
ldmodule_prefix = '_'

test.write("wrapper.py",
"""import os
import sys
open('%s', 'wb').write("wrapper.py\\n")
os.system(" ".join(sys.argv[1:]))
""" % test.workpath('wrapper.out').replace('\\', '\\\\'))

test.write('SConstruct', """\
foo = Environment(SWIGFLAGS='-python',
                  CPPPATH=[r'%(python_include)s'],
                  LDMODULEPREFIX='%(ldmodule_prefix)s',
                  LDMODULESUFFIX='%(_dll)s',
                  SWIG=[r'%(swig)s'],
                  LIBPATH=[r'%(python_libpath)s'],
                  LIBS='%(python_lib)s',
                  )

swig = foo.Dictionary('SWIG')
bar = foo.Clone(SWIG = [r'%(python)s', 'wrapper.py', swig])
foo.LoadableModule(target = 'foo', source = ['foo.c', 'foo.i'])
bar.LoadableModule(target = 'bar', source = ['bar.c', 'bar.i'])
""" % locals())

test.write("foo.c", """\
char *
foo_string()
{
    return "This is foo.c!";
}
""")

test.write("foo.i", """\
%module foo
%{
/* Put header files here (optional) */
/*
 * This duplication shouldn't be necessary, I guess, but it seems
 * to suppress "cast to pointer from integer of different size"
 * warning messages on some systems.
 */
extern char *foo_string();
%}

extern char *foo_string();
""")

test.write("bar.c", """\
char *
bar_string()
{
    return "This is bar.c!";
}
""")

test.write("bar.i", """\
%module \t bar
%{
/* Put header files here (optional) */
/*
 * This duplication shouldn't be necessary, I guess, but it seems
 * to suppress "cast to pointer from integer of different size"
 * warning messages on some systems.
 */
extern char *bar_string();
%}

extern char *bar_string();
""")

test.run(arguments = ldmodule_prefix+'foo' + _dll)

test.must_not_exist(test.workpath('wrapper.out'))

test.run(program = python, stdin = """\
import foo
print foo.foo_string()
""", stdout="""\
This is foo.c!
""")

test.up_to_date(arguments = ldmodule_prefix+'foo' + _dll)

test.run(arguments = ldmodule_prefix+'bar' + _dll)

test.must_match('wrapper.out', "wrapper.py\n")

test.run(program = python, stdin = """\
import foo
import bar
print foo.foo_string()
print bar.bar_string()
""", stdout="""\
This is foo.c!
This is bar.c!
""")

test.up_to_date(arguments = '.')


test.pass_test()

# Local Variables:
# tab-width:4
# indent-tabs-mode:nil
# End:
# vim: set expandtab tabstop=4 shiftwidth=4:
