'''
Tool icons are from the Material Design icon library.
icon_*.png and module_*.png are from cpenv.
'''

from os.path import abspath, dirname, join


res_package = dirname(__file__)


def get_path(*parts):
    return abspath(join(res_package, *parts)).replace('\\', '/')
