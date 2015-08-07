
import os

from .paths import LazyPath
from ..utils.verify import is_type_of


def is_lazy_path(obj, ignore=False):
	""" Check if an object is type LazyPath """
	return is_type_of(obj, LazyPath, ignore)

def get_current_path(_file_):
	""" To get the path of a file, you must specify that """
	return os.path.abspath(_file_)

def show_current_path(_file_):
	print get_current_path(_file_)








