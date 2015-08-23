
import os

from .paths import LazyPath
from ..utilities.verify import is_type_of


def is_lazy_path(obj, ignore=False):
	""" Check if an object is type LazyPath """
	return is_type_of(obj, LazyPath, ignore)

def get_current_path(_file_):
	""" To get the path of a file, you must pass __file__ """
	return os.path.abspath(_file_)

def show_current_path(_file_):
	""" Print the path of a file, you must pass __file__ """
	print get_current_path(_file_)








