import os
import urlparse

from .exceptions import SchemeError, HostError
from ..utilities.verify import is_type_of, is_str


class LazyUrl(object):
	""" 
	A more friendly API to urls, using the urlparse library to split and join
	urls.
	"""
	url = ''
	scheme, host, path, params, query, fragment = ('','','','','','')
	allowed_schemes = ['http', 'https']
	auto_fix = True

	### Builtin Methods ############################################
	def __init__(self, url, auto_fix=True):
		self.auto_fix = auto_fix
		self.set_url(url)

	def __str__(self): return self.url
	def __repr__(self): return self.url
	def __iter__(self):
		for x in [self.scheme, self.host, self.path,\
		self.params, self.query, self.fragment]: yield x

	def __ne__(self, other): return not self.__eq__(other)
	def __eq__(self, other):
		if other == self.url:
			return self.url == True
		if isinstance(other, self.__class__):
			return other.__dict__ == self.__dict__
		return False
	################################################################

	### Getters / Setters ##########################################
	def set_url(self, url):
		is_str(self.url)
		self.url = url
		self._delegate_url_pieces()
		self._fix_url()
		self.join_url()

	def set_scheme(self, scheme, join=True):
		self.scheme = scheme if scheme in self.allowed_schemes else 'http'
		self.join_url(join)
	def set_host(self, host, join=True):
		self.host = host
		self.join_url(join)
	def set_path(self, path, join=True):
		self.path = path
		self.join_url(join)
	def set_params(self, params, join=True):
		self.params = params
		self.join_url(join)
	def set_query(self, query, join=True):
		self.query = query
		self.join_url(join)
	def set_fragment(self, fragment, join=True):
		self.fragment = fragment
		self.join_url(join)

	def get_url(self): return self.url
	def get_scheme(self): return self.scheme
	def get_host(self): return self.host
	def get_path(self): return self.path
	def get_params(self): return self.params
	def get_query(self): return self.query
	def get_fragement(self): return self.fragment

	def get_full_path(self):
		""" Return the url without the scheme and host parts """
		idx = len(self.scheme) + len(self.host) + 3 # +3 for ://
		return self.url[idx:]

	def clear_full_path(self):
		""" Remove all url pieces except the scheme and host """
		self.set_path('', False)
		self.set_params('', False)
		self.set_query('', False)
		self.set_fragment('', False)
		self.join_url()
	################################################################

	### Validation #################################################
	def has_url(self):
		if not url: 
			return False
		return True

	def is_valid_url(self):
		is_str(self.url)
		url = urlparse(self.url)
		url.host = url.netloc
		if url.shcheme not in self.allowed_schemes:
			raise SchemeError(url.scheme, self.allowed_schemes)
		elif not url.host:
			raise HostError()
		return True
	################################################################


	### Operations #################################################
	def join_url(self, join=True):
		""" Join the url pieces to form a new url """
		if not self.path:
			self.path = '/'
		elif self.path[0] is not '/':
			self.path = '/' + self.path
		if join:
			self.url = urlparse.urlunparse(self)


	def _delegate_url_pieces(self):
		""" Delegate the url parts from ParseResult, to self """
		self.scheme, self.host, self.path, self.params,\
		self.query, self.fragment = urlparse.urlparse(self.url)

	def _fix_url(self):
		""" Attempt to fix any broken parts of the url """ 
		if self.scheme not in self.allowed_schemes:
			if not self.auto_fix:
				raise SchemeError(self.scheme, self.allowed_schemes)
			self.scheme = self.allowed_schemes[0]


		if not self.host:
			if not self.auto_fix:
				raise HostError()

			elif self.path:
				pieces = self.path.split('/')
				
				if len(pieces) == 1:
					if not pieces[0]: raise HostError()
					else: self.host = pieces.pop(0)
				elif pieces[0]:
					self.host = pieces.pop(0)
				elif pieces[1]:
					self.host = pieces.pop(1)
				else:
					raise HostError()
				self.path = '/'.join(pieces)

		self.join_url()

	def print_overview(self, url=None):
		if isinstance(url, urlparse.ParseResult):
			url.host = url.netloc
			url.url = url.geturl()
		else:
			url = self
	
		print '\nOverview:\n'
		print '\tUrl: %s\n' % url.url
		print '\tScheme: %s' % url.scheme
		print '\tHost: %s' % url.host
		print '\tPath: %s' % url.path	
		print '\tQuery: %s' % url.query
		print '\tFragment: %s\n' % url.fragment

	################################################################


