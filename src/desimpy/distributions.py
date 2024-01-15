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
		'''Sample from the distribution.'''
		return random.uniform(self.lower, self.upper)

class Triangular(Distribution):
	
	def __init__(self, lower: float, high: float, mode: float) -> NoReturn:
		self.lower = lower
		self.higher = higher
		self.mode = mode
	
	def sample(self):
		return random.triangular(self.lower, self.higher, self.mode)
