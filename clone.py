#!/usr/bin/env python
##
## (C) Copyright 2011-2013 Nuxeo SA (http://nuxeo.com/) and contributors.
##
## All rights reserved. This program and the accompanying materials
## are made available under the terms of the GNU Lesser General Public License
## (LGPL) version 2.1 which accompanies this distribution, and is available at
## http://www.gnu.org/licenses/lgpl-2.1.html
##
## This library is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
## Lesser General Public License for more details.
##
## Contributors:
##     Stefane Fermigier
##     Julien Carsique
##
## This script clones or updates Nuxeo source code from Git repositories.
##
import optparse
import os
import sys

from scripts.nxutils import ExitException, Repository, log


def main():
    try:
        usage = "usage: %prog [options] [version|branch|tag]"
        parser = optparse.OptionParser(usage=usage, description="""Clone or
update Nuxeo source code.""")
        parser.add_option('-r', action="store", type="string",
                          dest='remote_alias', default='origin', help="""the
Git alias of remote URL (default: %default)""")
        parser.add_option("-a", "--all", action="store_true",
                          dest="with_optionals", default=False,
                          help="include 'optional' addons (default: %default)")
        parser.add_option('-f', "--fallback", action="store", type="string",
                          dest='fallback_branch', default=None, help="""a
branch to fallback on when the wanted branch doesn't exist locally neither
remotely (default: %default)""")
        parser.add_option('-n', "--nodrivemapping", action="store_true",
                          dest='no_drive_mapping', default=False,
                          help="""deactivate current directory mapping to a
virtual drive on Windows""")
        parser.add_option('-m', "--marketplace-conf", action="store",
                          type="string", dest='marketplace_conf', default=None,
                          help="""The Marketplace configuration URL
(default: %default)""")

        (options, args) = parser.parse_args()
        repo = Repository(os.getcwd(), options.remote_alias,
                          not options.no_drive_mapping)
        if len(args) == 0:
            version = None
        elif len(args) == 1:
            version = args[0]
        else:
            raise ExitException(1, "'version' must be a single argument. "
                                "See usage with '-h'.")
        repo.clone(version, options.fallback_branch, options.with_optionals,
                   options.marketplace_conf)
    #pylint: disable=C0103
    except ExitException, e:
        if e.message is not None:
            log("[ERROR] %s" % e.message, sys.stderr)
        sys.exit(e.return_code)
    finally:
        if "repo" in locals():
            repo.cleanup()

if __name__ == '__main__':
    main()
