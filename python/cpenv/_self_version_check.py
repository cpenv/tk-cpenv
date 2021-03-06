# -*- coding: utf-8 -*-

# Standard library imports
import os
import sys
import subprocess
from datetime import datetime

# Local imports
from . import __version__
from .api import get_cache_path
from .versions import parse_version, default_version


_cache_expiration = 3600  # seconds - 1 hour
_warning_template = '''
WARNING: You are using cpenv version {}, however version {} is available.
You should consider upgrading via the 'pip install --upgrade cpenv' command.
'''


def is_latest_version():
    '''Check if the current version is the latest version.

    Returns:
        (bool, Version, Version) - is_latest, current, latest
    '''

    current = get_current_version()
    latest = get_latest_version()
    return current >= latest, current, latest


def warn_newer_version_available(current, latest):
    '''Warn user that a new version is available.

    To be used in conjunction with is_latest_version.
    '''

    print(_warning_template.format(current.string, latest.string))


def get_current_version():
    '''Return the current version of cpenv as a Version object'''

    return parse_version(__version__)


def get_latest_version():
    '''Use pip search to query pypi for the latest version of cpenv.'''

    latest_file = get_cache_path('latest_version')
    latest_file_expired = True
    if os.path.isfile(latest_file):
        time_since_modified = (
            datetime.now()
            - datetime.fromtimestamp(os.path.getmtime(latest_file))
        ).total_seconds()
        latest_file_expired = time_since_modified > _cache_expiration

    latest = default_version()
    if latest_file_expired:
        python = sys.executable
        query = subprocess.check_output(python + ' -m pip search cpenv')
        query = query.decode(sys.stdout.encoding)
        for line in query.splitlines():
            if 'latest:' in line.lower():
                latest = parse_version(line.split(':')[-1].strip())

        if latest:
            with open(latest_file, 'w') as f:
                f.write(latest.string)
    else:
        with open(latest_file, 'r') as f:
            latest_string = f.read()

        latest = parse_version(latest_string)

    return latest
