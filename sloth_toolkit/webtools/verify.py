from .urls import LazyUrl
from ..utilities.verify import is_type_of


def is_lazy_url(obj, ignore=False):
	""" Check if an object is type LazyUrl """
	return is_type_of(obj, LazyUrl, ignore)

