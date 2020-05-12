from os.path import abspath, dirname, join


res_package = dirname(__file__)


def get_path(*parts):
    return abspath(join(res_package, *parts)).replace('\\', '/')
