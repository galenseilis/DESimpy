"""Simulation-compatible probability distributions."""

from abc import ABC, abstractmethod
import operator
import numbers
import random

class Distribution(ABC):
    """Definition of simulation-compatible distributions."""

    @abstractmethod
    def sample(self, context):
        """Sample from distribution."""

    def __add__(self, other):
        """
        Add two distributions such that sampling is the sum of the samples.
        """
        dist = dist_cast(other)
        return TransformDistribution((self, dist), operator.add)

    def __sub__(self, other):
        """
        Subtract two distributions such that sampling is the difference of the samples.
        """
        dist = dist_cast(other)
        return TransformDistribution((self, dist), operator.sub)

    def __mul__(self, other):
        """
        Multiply two distributions such that sampling is the product of the samples.
        """
        dist = dist_cast(other)
        return TransformDistribution((self, dist), operator.mul)

    def __truediv__(self, other):
        """
        Divide two distributions such that sampling is the ratio of the samples.
        """
        dist = dist_cast(other)
        return TransformDistribution((self, dist), operator.truediv)


def dist_cast(obj):
    """Cast object to a distribution."""
    if isinstance(obj, numbers.Number):
        return DegenerateDistribution(func=lambda context: obj)
    if isinstance(obj, Distribution):
        return obj
    if callable(obj):
        return DegenerateDistribution(func=obj)
    if isinstance(obj, str):
        return DegenerateDistribution(func=lambda context: obj)

    raise ValueError(f"Could not cast {obj} to type `Distribution`.")


class ExponentialDistribution(Distribution):
    def __init__(self, rate):
        self.rate = rate

    def sample(self, context):
        return random.expovariate(self.rate)


class UniformDistribution(Distribution):
    def __init__(self, lower, upper):
        self.lower = lower
        self.upper = upper

    def sample(self, context):
        return random.uniform(self.lower, self.upper)


class DegenerateDistribution(Distribution):
    def __init__(self, func: Callable):
        self.func = func

    def sample(self, context):
        return self.func(context)


class TransformDistribution(Distribution):
    """A distribution that combines the samples of two or more other distributions via an operator.

    This implicitly induces a change of variables.
    """

    def __init__(self, dists, operator: Callable):
        self.dists = copy.deepcopy(dists)
        self.operator = operator

    def __repr__(self):
        return f"TransformDistribution({self.dists}, {self.operator})"

    def sample(self, context):
        samples = [dist.sample(context) for dist in self.dists]
        return self.operator(*samples)


class RejectDistribution(Distribution):
    """Add rejection sampling to a distribution.

    For example, lower truncation of a distribution
    to zero can restrict a real support distribution to
    a non-negative real support distribution.
    """

    def __init__(self, dist: Distribution, reject: Callable):
        self.dist = dist
        self.reject = reject

    def __repr__(self):
        return f"RejectDistribution({self.dist}, {self.reject})"

    def sample(self):
        while True:
            candidate = self.dist.sample()
            if not reject(candidate):
                return candidate
