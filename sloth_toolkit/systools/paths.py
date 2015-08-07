
import os

from ..webtools.verify import is_lazy_url


class LazyPath(object):
	""" 
	A basic unix file manager. Can create directories and files. 

	getabspath() - used to get the absoulte path. This is most likely what you want.

	File Compatibility:
		- text (html, text, lst)
		- images (jpeg, jpg, png, bmp)
		- compression (7z, zip, gzip, rar, tar, tar.gz, tar.bz2)
	"""
	cwd = os.getcwd()
	rel = ''
	fname = ''
	ext = ''
	
	_image_extensions = ['jpeg', 'jpg', 'png', 'bmp']
	_text_extensions = ['txt', 'text', 'html', 'md', 'lst']
	_compressed_extensions = [
		'tar', 'tar.gz', 'tar.bz2', '7z', 'zip', 'gzip', 'rar'
	]

	def __init__(self, lazy_url, save=False):
		self.create_path(lazy_url)

	def __str__(self): return self.getpath()
	def __repr__(self): return self.getpath()
	def __unicode__(self): return unicode(self.getpath())
	

	def getcwd(self): return self.cwd
	def getrel(self): return self.rel
	def getfname(self): return self.fname
	def getext(self): return self.ext

	def getpath(self): return os.path.join(self.cwd, self.rel)
	def getfilename(self): return '.'.join([self.fname, self.ext])
	def getabspath(self):
		""" path including the file """
		return os.path.join(self.getpath(), self.getfilename())		

	def updatecwd(self):
		self.cwd = os.path.abspath(os.getcwd())
		return self.cwd

	def makedirs(self):
		dirs = self.rel.split(os.sep)
		dirs = [d for d in dirs if d]
		if not dirs: return

		for i, d in enumerate(dirs):
			path = os.sep.join(dirs[:i+1])
			try:
				os.mkdir(path)
			except OSError, e:
				if e.errno not in [errno.EEXIST, errno.EACCES, 
				errno.ENOSPC, errno.EROFS]:
					raise e
				pass
		return


	### File Operations #################################
	def save_file(self, data):
		""" Examine the extension to see how to download the file """
		if self.ext in self._text_extensions:
			self.save_text_file(data)
		elif self.ext in self._image_extensions:
			self.save_binary_file(data)
		elif self.ext in self._compressed_extensions:
			pass#self.save_compreessed_file(data)

	def write_and_close(self, file, data):
		file.write(data)
		file.close()

	def save_binary_file(self, data):
		file = open(self.abspath(), 'wb')

	def save_text_file(self, data):
		file = open(self.abspath(), 'w')
		self.write_and_Cose(file, data)

	####################################################


	def _join_fname(self): 
		self.fname = '.'.join(self.fname)
	def _join_fname_and_makedirs(self): 
		self._join_fname()
		self.makedirs()


	def create_path(self, lazy_url):
		is_lazy_url(lazy_url)

		self.rel = lazy_url.host
		self.fname = lazy_url.path.rsplit('/', 1)

		# Add the path to self.rel and use the last extension as the filename
		if len(self.fname) == 2:
			self.rel = lazy_url.host +'/' + self.fname.pop(0)

		self.fname = self.fname[0].rsplit('.', 1)

		# If the url path was empty name the file home.html
		if (len(self.fname) == 1 and self.fname[0] == '')\
		or (len(self.fname) == 0 ):
			self.fname = 'home'
			self.ext = 'html'
			self.makedirs()
			return
		
		# There was a path but no extension, lets use .html
		elif len(self.fname) == 1:
			self.ext = 'html'
			self._join_fname_and_makedirs
			return

		# check two-part extensions like .tar.gz
		self.ext = self.fname.pop()
		self.fname = self.fname.pop().rsplit('.', 1)

		# lets combine the two extensions
		ext = ''
		if len(self.fname == 2):
			ext = '.'.join([self.fname.pop(), self.ext])

		# Varified: two-part extension is a compression file
		if ext in self._compressed_extensions:
			self.ext = ext
		elif ext in self._text_extensions:
			self.ext = ext
		elif ext in self._image_extensions:
			self.ext = ext
		else:
			self.ext = 'html'

		self._join_filename_and_makedirs()
		return
	### End create_path() #############################################



