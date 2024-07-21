import pytest
import operator
from desimpy.distributions import (
    Distribution,
    DegenerateDistribution,
    TransformDistribution,
    Exponential,
    ContinuousUniform,
    RejectDistribution,
    dist_cast,
    reject_negative
)

import numpy as np

# Concrete Distribution subclass for testing
class ConcreteDistribution(Distribution):
    def sample(self, context=None):
        return 1

def test_dist_cast_with_number():
    obj = 5
    result = dist_cast(obj)
    assert isinstance(result, DegenerateDistribution)
    assert result.sample() == 5

def test_dist_cast_with_distribution():
    obj = ConcreteDistribution()
    result = dist_cast(obj)
    assert result == obj

def test_dist_cast_with_callable():
    obj = lambda context: 10
    result = dist_cast(obj)
    assert isinstance(result, DegenerateDistribution)
    assert result.sample() == 10

def test_dist_cast_with_string():
    obj = "test_string"
    result = dist_cast(obj)
    assert isinstance(result, DegenerateDistribution)
    assert result.sample() == "test_string"

def test_dist_cast_with_invalid_type():
    obj = [1, 2, 3]
    with pytest.raises(ValueError):
        dist_cast(obj)

def test_degenerate_distribution_initialization():
    func = lambda context: 5
    dist = DegenerateDistribution(func)
    assert dist.func == func

def test_degenerate_distribution_sample():
    func = lambda context: 5
    dist = DegenerateDistribution(func)
    result = dist.sample()
    assert result == 5

def test_degenerate_distribution_sample_with_context():
    context = {"key": "value"}
    func = lambda context: 5
    dist = DegenerateDistribution(func)
    result = dist.sample(context)
    assert result == 5

def test_exponential_distribution():
    rate = 2.0
    dist = Exponential(rate)
    sample = dist.sample()
    assert sample > 0

def test_exponential_repr():
    rate = 2.0
    dist = Exponential(rate)
    assert repr(dist) == f"Exponential(rate={rate})"

def test_exponential_pdf():
    rate = 2.0
    dist = Exponential(rate)
    x = 1.0
    pdf_value = dist.pdf(x)
    expected_value = rate * np.exp(-rate * x)
    assert pdf_value == expected_value

def test_continuous_uniform_distribution():
    lower = 0.0
    upper = 1.0
    dist = ContinuousUniform(lower, upper)
    sample = dist.sample()
    assert lower <= sample <= upper

def test_continuous_uniform_repr():
    lower = 0.0
    upper = 1.0
    dist = ContinuousUniform(lower, upper)
    assert repr(dist) == f"ContinuousUniform(lower={lower}, upper={upper})"

def test_transform_distribution():
    dist1 = ConcreteDistribution()
    dist2 = ConcreteDistribution()
    transform_dist = TransformDistribution((dist1, dist2), operator.add)
    assert transform_dist.sample() == 2

def test_reject_distribution():
    dist = Exponential(1.0)
    reject_dist = RejectDistribution(dist, reject_negative)
    sample = reject_dist.sample()
    assert sample >= 0

def test_reject_distribution_repr():
    dist = Exponential(1.0)
    reject_dist = RejectDistribution(dist, reject_negative)
    assert repr(reject_dist) == f"RejectDistribution({dist}, {reject_negative})"

