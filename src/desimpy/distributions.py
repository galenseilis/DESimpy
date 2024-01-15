import abc
import random
from typing import NoReturn

class Distribution(abc.ABC):
	
	@abc.abstractmethod
	def sample(self):
		'''Return a sampled thing.'''
		raise NotImplementedError


class ContinuousUniform(Distribution):
	'''Continuous uniform distribution between a lower and upper value.'''

	def __init__(self, lower: float, upper:float) -> NoReturn:
		'''Initialize distribution with lower/upper bounds as parameters.

		Args:
			lower (float): Lower bound of distribution.
			upper (float): Upper bound of distribution.
		'''
		self.lower = lower
		self.upper = upper

	def sample(self):
		'''Sample from the distribution.

		Returns:
			(float): Sampled result.
		'''
		return random.uniform(self.lower, self.upper)

class Triangular(Distribution):
	'''Triangular distribution.'''
	
	def __init__(self, low: float, high: float, mode: float) -> NoReturn:
		'''Initialize with parameters for triangular distribution.

		Args:
			low (float): Lower bound of the triangular distribution.
			high (float): Upper bound of the triangular distribution.
			mode (float): The mode of the triangular distribution.
		'''
		self.low = low
		self.high = high
		self.mode = mode
	
	def sample(self):
		'''Sample from the triangular distribution.'''
		return random.triangular(self.low, self.high, self.mode)
