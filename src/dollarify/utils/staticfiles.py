try:
    import importlib.resources as pkg_resources
except ImportError:
    # Try importing 'importlib_resources'. Python < 3.7
    pkg_resources = __import__('importlib_resources')


from importlib.resources import Package
from dollarify import static


def load_static(path: str, binary = False, pkg: Package = static):
    if binary:
        return pkg_resources.read_binary(pkg, path)
    return pkg_resources.read_text(pkg, path)