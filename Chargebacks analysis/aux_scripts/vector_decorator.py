import numpy as np
import functools


class vectorize(np.vectorize):
	"""
	Alter the np.vectorize class so that it can be used to decorate methods
	"""
	def __get__(self, obj, objtype):
		return functools.partial(self.__call__, obj)