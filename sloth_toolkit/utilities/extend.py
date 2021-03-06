
__doc__ = """ A module with the functionality to extend or modify an object."""

from slugify import slugify

from . import verify, prope


def validate_attribute_name(name):
	""" Modify a string to become a valid/legal lower case attribute """
	name = slugify(name).replace('-', '_')
	return name


def add_attribute(cls, attr_name, attr_value):
	""" Add a valid attribute name to a class and set the attribute value """
	attr_name = validate_attribute_name(attr_name)
	setattr(cls, attr_name, attr_value)


#  Code solution from: http://stackoverflow.com/questions/20078816/replace-non-ascii-characters-with-a-single-space
def validate_ascii_only(text, replacement=' '):
	""" 
	When mining for data, you may come across special characters
	that will raise a 'UnicodeEncodeError', this may include printing, 
	storing in a database or other reasons.
	
	Call the function, passing the inflicted string, to replace those characters 
	with, by default a space. Instead of a space the second paramater, which is
	optional allows you to specify the replacement character.
	""" 
	return str(re.sub( r'[^\x00-\x7F]+', replacement, text ))




def extend_get_has_response_header_methods(obj):
	""" 
	The passed object must have the attribute `response`, and that response
	must be an object that has an attribute named `headers` that is a dict.

	Dynamically create methods for the headers in the response object, 
	and append those methods to the class of the object (not the instance).
	"""

	verify.has_response(obj)
	verify.has_headers(obj.response)

	#### Methods Wrapper ##########################################
	def _make_method(header_name, has=False, get=False):
		""" Create a method for a header """			

		# Create a valid header name
		valid_header_name = verify.validate_attribute_name(header_name)
		
		#### Methods to make #######################
		def _has_header(self):
			""" Return Flase if header value is None """
			if header_name not in self.response.headers:
				self.response.headers[header_name] = None
			return self.response.headers[header_name] != None

		def _get_header(self): 
			""" Returns the header value """
			if header_name not in self.response.headers:
				self.response.headers[header_name] = None
			return self.response.headers[header_name]
		############################################

		if has:
			_method = _has_header
			_method.__name__ = 'has_%s_header' %  valid_header_name
		elif get:
			_method = _get_header
			_method.__name__ = 'get_%s_header' % valid_header_name
		return _method
	###############################################################


	objclass = prope.get_class(obj)
	for header_name in obj.response.headers:
		_has_method = _make_method(header_name, has=True)
		method_name = _has_method.__name__
		setattr(objclass, method_name, _has_method)

		_get_method = _make_method(header_name, get=True)
		method_name = _has_method.__name__
		setattr(objclass, method_name, _get_method)



