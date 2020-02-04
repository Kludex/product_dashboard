#!/usr/bin/env python

from pathlib import Path
from datetime import datetime

def project_root() -> Path:
    """
    Gets the project root.

    Returns:
        Path: project root path.
    """
    return Path(__file__).parent.parent

def date_parser(date):
    return datetime.strptime(date, '%Y-%m-%d')

def filename_from(path):
    return path.split('/')[-1]
