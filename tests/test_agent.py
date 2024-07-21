from abc import ABC
from desimpy.agent import Agent

# Create a concrete subclass of Agent for testing
class ConcreteAgent(Agent):
    pass

def test_agent_initialization():
    agent = ConcreteAgent(name="TestAgent")
    assert agent.name == "TestAgent"

def test_agent_repr():
    agent = ConcreteAgent(name="TestAgent")
    assert repr(agent) == "ConcreteAgent(name=TestAgent)"

