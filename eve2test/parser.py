# Copyright (C) 2019 Open Information Security Foundation
#
# You can copy, redistribute or modify this Program under the terms of
# the GNU General Public License version 2 as published by the Free
# Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# version 2 along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301, USA.

import argparse


def parse_args():
    """
    Parse arguments and return them to main for processing.
    """
    parser = argparse.ArgumentParser(
        description="Convert eve.json to test.yaml")
    parser.add_argument("path-to-eve", metavar="<path-to-eve>",
                        help="Path to eve.json")
    parser.add_argument("output-path", metavar="<output-path>",
                        help="Path to the folder where generated test.yaml should be put")
    parser.add_argument("--eventtype-only", default=None, action="store_true",
                        help="Create filter blocks based on event types only")
    parser.add_argument("--allow-events", nargs="?", default=None,
                        help="Create filter blocks for the specified events")

    # add arg to allow stdout only
    args = parser.parse_args()

    return args
