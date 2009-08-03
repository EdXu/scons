"""SCons.Variables.PathVariable

This file defines an option type for SCons implementing path settings.

To be used whenever a a user-specified path override should be allowed.

Arguments to PathVariable are:
  option-name  = name of this option on the command line (e.g. "prefix")
  option-help  = help string for option
  option-dflt  = default value for this option
  validator    = [optional] validator for option value.  Predefined
                 validators are:

                     PathAccept -- accepts any path setting; no validation
                     PathIsDir  -- path must be an existing directory
                     PathIsDirCreate -- path must be a dir; will create
                     PathIsFile -- path must be a file
                     PathExists -- path must exist (any type) [default]

                 The validator is a function that is called and which
                 should return True or False to indicate if the path
                 is valid.  The arguments to the validator function
                 are: (key, val, env).  The key is the name of the
                 option, the val is the path specified for the option,
                 and the env is the env to which the Otions have been
                 added.

Usage example:

  Examples:
      prefix=/usr/local

  opts = Variables()

  opts = Variables()
  opts.Add(PathVariable('qtdir',
                      'where the root of Qt is installed',
                      qtdir, PathIsDir))
  opts.Add(PathVariable('qt_includes',
                      'where the Qt includes are installed',
                      '$qtdir/includes', PathIsDirCreate))
  opts.Add(PathVariable('qt_libraries',
                      'where the Qt library is installed',
                      '$qtdir/lib'))

"""

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

__all__ = ['PathVariable',]

import os
import os.path

import SCons.Errors

from SCons.i18n import _

class _PathVariableClass:

    def PathAccept(self, key, val, env):
        """Accepts any path, no checking done."""
        pass

    def PathIsDir(self, key, val, env):
        """Validator to check if Path is a directory."""
        if not os.path.isdir(val):
            if os.path.isfile(val):
                m = _('Directory path for option %(key)s is a file: %(val)s')
            else:
                m = _('Directory path for option %(key)s does not exist: %(val)s')
            raise SCons.Errors.UserError(m % {"key":key, "val":val})

    def PathIsDirCreate(self, key, val, env):
        """Validator to check if Path is a directory,
           creating it if it does not exist."""
        if os.path.isfile(val):
            m = _('Path for option %(key)s is a file, not a directory: %(val)s')
            raise SCons.Errors.UserError(m % {"key":key, "val":val})
        if not os.path.isdir(val):
            os.makedirs(val)

    def PathIsFile(self, key, val, env):
        """validator to check if Path is a file"""
        if not os.path.isfile(val):
            if os.path.isdir(val):
                m = _('File path for option %(key)s is a directory: %(val)s')
            else:
                m = _('File path for option %(key)s does not exist: %(val)s')
            raise SCons.Errors.UserError(m % {"key":key, "val":val})

    def PathExists(self, key, val, env):
        """validator to check if Path exists"""
        if not os.path.exists(val):
            m = _('Path for option %(key)s does not exist: %(val)s')
            raise SCons.Errors.UserError(m % {"key":key, "val":val})

    def __call__(self, key, help, default, validator=None):
        # NB: searchfunc is currenty undocumented and unsupported
        """
        The input parameters describe a 'path list' option, thus they
        are returned with the correct converter and validator appended. The
        result is usable for input to opts.Add() .

        The 'default' option specifies the default path to use if the
        user does not specify an override with this option.

        validator is a validator, see this file for examples
        """
        if validator is None:
            validator = self.PathExists

        if SCons.Util.is_List(key) or SCons.Util.is_Tuple(key):
            return (key, '%s ( /path/to/%s )' % (help, key[0]), default,
                    validator, None)
        else:
            return (key, '%s ( /path/to/%s )' % (help, key), default,
                    validator, None)

PathVariable = _PathVariableClass()

# Local Variables:
# tab-width:4
# indent-tabs-mode:nil
# End:
# vim: set expandtab tabstop=4 shiftwidth=4:
