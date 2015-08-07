from .urls import LazyUrl

def is_lazy_url(obj, ignore=False):
	""" Check if an object is type LazyUrl """
	return is_type_of(obj, LazyUrl, ignore)

