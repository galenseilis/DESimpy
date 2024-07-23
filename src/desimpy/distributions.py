"""Simulation-compatible probability distributions."""

from abc import ABC, abstractmethod
import copy
import operator
import numbers
from typing import Callable

import numpy as np


class Distribution(ABC):
    """Definition of simulation-compatible distributions."""

    def __repr__(self):
        return f"{self.__class__.__name__}"

    @abstractmethod
    def sample(self, context=None):
        """Sample from distribution."""

    def __abs__(self):
        return Transform((self,), operator.abs)

    def __add__(self, other):
        """
        Add two distributions such that sampling is the sum of the samples.
        """
        dist = dist_cast(other)
        return Transform((self, dist), operator.add)

    def __sub__(self, other):
        """
        Subtract two distributions such that sampling is the difference of the samples.
        """
        dist = dist_cast(other)
        return Transform((self, dist), operator.sub)

    def __mul__(self, other):
        """
        Multiply two distributions such that sampling is the product of the samples.
        """
        dist = dist_cast(other)
        return Transform((self, dist), operator.mul)

    def __truediv__(self, other):
        """
        Divide two distributions such that sampling is the ratio of the samples.
        """
        dist = dist_cast(other)
        return Transform((self, dist), operator.truediv)

    def __call__(self, other):
        """Overloaded call method.

        If `other` is of type `Distribution`, or is an iterable containing
        only elements of type `Distribution`, then it will attempt to
        compose the distributions. Note that this may fail silently until
        a sample is taken from the resulting distribution if the number of
        parameters in the class of `self` does not match the number of distributions
        representing in `other`.

        If the above is not true but other is nonthesless callable,
        then it will attempt to use it as a transform instead.
        """

        if isinstance(other, Distribution):
            return Compose(self.__class__, (other,))

        try:
            iter(other)
            if all(isinstance(d, Distribution) for d in other):
                return Compose(self.__class__, other)
        except ValueError as ve:
            pass

        if callable(other):
            return Transform((self,), other)

        raise ValueError(f'Invalid input {other=}.')

    def pdf(self, x):  # pylint: disable=C0103
        """Probability density function or
        probability mass function."""
        raise NotImplementedError('Method `pdf` not implemented.')

    def cdf(self, x):  # pylint: disable=C0103
        """Cumulative distribution function."""
        raise NotImplementedError('Method `cdf` not implemented')

    def quantile(self, p):  # pylint: disable=C0103
        """Quantile function"""
        raise NotImplementedError('Method `quantile` not implemented.')

    def mean(self):
        """Expected value."""
        raise NotImplementedError('Method `mean` not implemented')

    def median(self):
        """Median"""
        raise NotImplementedError('Method `median` not implemented.')

    def mode(self):
        """Mode"""
        raise NotImplementedError()

    def variance(self):
        """Variance"""
        raise NotImplementedError()

    def standard_deviation(self):
        """Standard deviation"""
        raise NotImplementedError()

    def mean_absolute_deviation(self):
        """Mean absolute deviation (MAD)."""
        raise NotImplementedError()

    def skewness(self):
        """Skewness."""
        raise NotImplementedError()

    def excess_kurtosis(self):
        """Excess kurtosis"""
        raise NotImplementedError()

    def entropy(self):
        """Entropy"""
        raise NotImplementedError()

    def moment_generating_function(self, t):  # pylint: disable=C0103
        """Moment generating function (MGF)."""
        raise NotImplementedError()

    def expected_shortfall(self, p):  # pylint: disable=C0103
        """Expected shortfall."""
        raise NotImplementedError()


def dist_cast(obj):
    """Cast object to a distribution."""
    if isinstance(obj, numbers.Number):
        return Degenerate(func=lambda context: obj)
    if isinstance(obj, Distribution):
        return obj
    if callable(obj):
        return Degenerate(func=obj)
    if isinstance(obj, str):
        return Degenerate(func=lambda context: obj)

    raise ValueError(f"Could not cast {obj} to type `Distribution`.")


class Exponential(Distribution):
    """Exponential distribution."""

    def __init__(self, rate, rng=None):
        self.rate = rate
        self.rng = np.random.default_rng() if rng is None else rng

    def __repr__(self):
        return f"{self.__class__.__name__}(rate={self.rate})"

    def sample(self, context=None):
        """Sample from distribution."""
        return self.rng.exponential(1 / self.rate)

    @classmethod
    def fit(cls, data):
        """Fit distribution to data."""
        return Exponential(rate=1 / np.mean(data))

    def pdf(self, x):
        return self.rate * np.exp(-self.rate * x)

    def cdf(self, x):
        return 1 - np.exp(-self.rate * x)

    def mean(self):
        return 1 / self.rate

    def median(self):
        return np.log(2) / self.rate

    def mode(self):
        return 0

    def variance(self):
        return 1 / np.square(self.rate)

    def standard_deviation(self):
        return 1 / self.rate

    def skewness(self):
        return 2

    def excess_kurtosis(self):
        return 6

    def entropy(self):
        return 1 - np.log(self.rate)

    def moment_generating_function(self, t):  # pylint: disable=C0103
        if t < self.rate:
            return self.rate / (self.rate - t)

        raise ValueError("The argument t must be less than the rate.")

    def expected_shortfall(self, p):
        return -(np.log(1 - p) + 1) / self.rate


class ContinuousUniform(Distribution):
    """Continuous uniform distribution."""

    def __init__(self, lower: float = 0, upper: float = 1, rng=None):
        self.rng = np.random.default_rng() if rng is None else rng
        self.lower = lower
        self.upper = upper

    def __repr__(self):
        return f"{self.__class__.__name__}(lower={self.lower}, upper={self.upper})"

    def sample(self, context=None):
        """Sample from distribution."""
        return self.rng.uniform(self.lower, self.upper)

    @classmethod
    def fit(cls, data):
        """Fit distribution model."""
        return ContinuousUniform(lower=min(data), upper=max(data))


class Degenerate(Distribution):
    """Degenerate distribution."""

    def __init__(self, func: Callable):
        self.func = func

    def __repr__(self):
        return f"{self.__class__.__name__}(self.func)"

    def sample(self, context=None):
        """Sample from distribution."""
        return self.func(context)


class Transform(Distribution):
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

class Compose(Distribution):
    """Composite distribution."""

    def __init__(self, dist_cls, dists):
        self.dist_cls = dist_cls
        self.dists = dists

    def sample(self, context=None):
        """Composite sampling."""
        return dist_cls(*[dist.sample(context) for dist in self.dists]).sample(context)

class Min(Distribution):
    """Distribution takes the minimum of samples from multiple distributions."""

    def __init__(self, dists):
        self.dists = copy.deepcopy(dists)

    def sample(self, context=None):
        samples = [dist.sample(context) for dist in self.dists]
        return min(samples)


class Max(Distribution):
    """Distribution takes the maximum of samples from multiple distributions."""

    def __init__(self, dists):
        self.dists = copy.deepcopy(dists)

    def sample(self, context=None):
        samples = [dist.sample(context) for dist in self.dists]
        return max(samples)

class Reject(Distribution):
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
            if not self.reject(candidate, context):
                return candidate


def is_negative(candidate: float, context=None) -> bool:  # pylint: disable=W0613
    """Reject negative candidates.

    Ignores context.
    """
    if candidate < 0:
        return True
    return False

def outside_interval(candidate, lower=0, upper=float('inf'), context=None) -> bool:
    """Truncate candidates to an interval.
    """
    if candidate < lower:
        return True
    if candidate > uppwer:
        return True
    return False

