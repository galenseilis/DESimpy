"""```yaml
source:https://simpy.readthedocs.io/en/stable/topical_guides/environments.html#simulation-control
```
"""

from desimpy import EventScheduler

if __name__ == "__main__":
    env = EventScheduler()
    for i in range(100):
        _ = env.run_until_max_time(i)
