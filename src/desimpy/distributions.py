import abc
import random


class Distribution(abc.ABC):
	
	@abc.abstractmethod
	def sample(self, env):
		'''Return a sampled thing.'''
		raise NotImplementedError
