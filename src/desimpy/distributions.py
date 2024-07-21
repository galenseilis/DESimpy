"""Simulation-compatible probability distributions."""

from abc import ABC, abstractmethod
import copy
import operator
import numbers
import random
from typing import Callable


class Distribution(ABC):
    """Definition of simulation-compatible distributions."""

    @abstractmethod
    def sample(self, context=None):
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


class Exponential(Distribution):
    """Exponential distribution."""

    def __init__(self, rate):
        self.rate = rate

    def sample(self, context=None):
        """Sample from distribution."""
        return random.expovariate(self.rate)

    @classmethod
    def fit(cls, data):
        """Fit distribution to data."""
        return Exponential(rate=len(data) / sum(data))


class ContinuousUniform(Distribution):
    """Continuous uniform distribution."""

    def __init__(self, lower, upper):
        self.lower = lower
        self.upper = upper

    def __repr__(self):
        return f"{self.__class__.__name__}(lower={self.lower}, upper={self.upper})"

    def sample(self, context=None):
        """Sample from distribution."""
        return random.uniform(self.lower, self.upper)

    @classmethod
    def fit(cls, data):
        """Fit distribution model.

        This estimator is biased.
        """
        return ContinuousUniform(lower=min(data), upper=max(data))


class DegenerateDistribution(Distribution):
    """Degenerate distribution."""

    def __init__(self, func: Callable):
        self.func = func

    def __repr__(self):
        return f"{self.__class__.__name__}(self.func)"

    def sample(self, context=None):
        """Sample from distribution."""
        return self.func(context)


class TransformDistribution(Distribution):
    """A distribution that combines the samples of two or more other distributions via an operator.

    This implicitly induces a change of variables.
    """

    def __init__(self, dists, transform: Callable):
        self.dists = copy.deepcopy(dists)
        self.transform = transform

    def __repr__(self):
        return f"{self.__class__.__name__}({self.dists}, {self.transform})"

    def sample(self, context=None):
        """Sample from distribution."""
        samples = [dist.sample(context) for dist in self.dists]
        return self.transform(*samples)


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

    def sample(self, context=None):
        """Rejection sample from distribution."""
        while True:
            candidate = self.dist.sample(context)
            if not self.reject(candidate, context=None):
                return candidate


def reject_negative(candidate: float, context=None) -> bool:  # pylint: disable=W0613
    """Reject negative candidates.

    Ignores context.
    """
    if candidate < 0:
        return False
    return True
