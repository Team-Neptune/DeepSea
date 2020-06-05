#!/usr/bin/env python3
#
# Kosmos Builder
# Copyright (C) 2020 Nichole Mattera
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301, USA.
#

import argparse
import common
import config
import modules
from pathlib import Path
import shutil
import sys
import json

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-v', '--version',
        default=None,
        type=str,
        help='Overrides the DeepSea Version from the config file.',
        metavar='DeepSeaVersion')
    parser.add_argument(
        "package_file",
        default=None,
        type=str,
        help="Create a release build using the provided json file.")
    parser.add_argument(
        "output",
        default=None,
        type=str,
        help='Zip file to create.')
    
    # Parse arguments
    args = parser.parse_args()

    return args


def get_deepsea_version(args):
    if args.version is not None:
        return args.version
    return config.version


def init_version_messages(package_content, kosmos_version):
    pkg_name = package_content['package_name']
    return [f'{pkg_name} {kosmos_version} built with:']


if __name__ == '__main__':
    args = parse_args()

    temp_directory = common.generate_temp_path()
    common.mkdir(temp_directory)
    deepsea_version = get_deepsea_version(args)

    auto_build = False
    if hasattr(args, 'auto'):
        auto_build = args.auto

    with open(args.package_file,'r') as pkgfile:
        package_content = json.load(pkgfile)

    version_messages = init_version_messages(package_content, deepsea_version)

    build_messages = modules.build(
        temp_directory, deepsea_version, package_content, auto_build)

    common.delete(args.output)

    if build_messages is not None:
        version_messages += build_messages

        if package_content['is_sdsetup']:
            common.move(temp_directory, args.output)
        else:
            shutil.make_archive(
                Path(args.output).stem,
                'zip',
                temp_directory)

        for message in version_messages:
            print(message)

    common.delete(Path.cwd().joinpath('tmp'))
