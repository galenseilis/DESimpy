from desimpy import Event, EventScheduler, EventStatus

# Sample condition functions for testing

def always_true_condition(scheduler: EventScheduler, event: Event) -> bool:
    _ = scheduler
    _ = event
    """Condition that always returns True, activating all events."""
    return True

def always_false_condition(scheduler: EventScheduler, event: Event) -> bool:
    """Condition that always returns False, activating no events."""
    _ = scheduler
    _ = event
    return False

def time_less_than_20_condition(scheduler: EventScheduler, event: Event) -> bool:
    """Condition that activates events with time less than 20."""
    _ = scheduler
    return event.time < 20

def has_high_priority_condition(scheduler: EventScheduler, event: Event) -> bool:
    """Condition that activates events with high priority in their context."""
    _ = scheduler
    result: bool = event.context.get('priority') == 'high'
    return result

# Test Suite for activate_all_events_by_condition

def test_activate_all_events_by_condition_no_events():
    """Test `activate_all_events_by_condition` with an empty event queue."""
    scheduler = EventScheduler()
    
    scheduler.activate_all_events_by_condition(always_true_condition)
    
    assert scheduler.event_queue == [], "The event queue should remain empty when there are no events to activate."

def test_activate_all_events_by_condition_always_true():
    """Test `activate_all_events_by_condition` with a condition that always returns True."""
    scheduler = EventScheduler()
    event1 = Event(time=5)
    event2 = Event(time=15)
    event1.deactivate()
    event2.deactivate()
    
    scheduler.schedule(event1)
    scheduler.schedule(event2)
    
    scheduler.activate_all_events_by_condition(always_true_condition)
    
    assert event1.status == EventStatus.ACTIVE, "Event1 should be activated."
    assert event2.status == EventStatus.ACTIVE, "Event2 should be activated."

def test_activate_all_events_by_condition_always_false():
    """Test `activate_all_events_by_condition` with a condition that always returns False."""
    scheduler = EventScheduler()
    event1 = Event(time=5)
    event2 = Event(time=15)
    event1.deactivate()
    event2.deactivate()
    
    scheduler.schedule(event1)
    scheduler.schedule(event2)
    
    scheduler.activate_all_events_by_condition(always_false_condition)
    
    assert event1.status == EventStatus.INACTIVE, "Event1 should remain inactive."
    assert event2.status == EventStatus.INACTIVE, "Event2 should remain inactive."

def test_activate_all_events_by_condition_time_less_than_20():
    """Test `activate_all_events_by_condition` with a condition that activates events with time < 20."""
    scheduler = EventScheduler()
    event1 = Event(time=10)  # Should be activated
    event2 = Event(time=25)  # Should remain inactive
    event3 = Event(time=15)  # Should be activated
    
    event1.deactivate()
    event2.deactivate()
    event3.deactivate()
    
    scheduler.schedule(event1)
    scheduler.schedule(event2)
    scheduler.schedule(event3)
    
    scheduler.activate_all_events_by_condition(time_less_than_20_condition)
    
    assert event1.status == EventStatus.ACTIVE, "Event with time 10 should be activated."
    assert event2.status == EventStatus.INACTIVE, "Event with time 25 should remain inactive."
    assert event3.status == EventStatus.ACTIVE, "Event with time 15 should be activated."

def test_activate_all_events_by_condition_high_priority():
    """Test `activate_all_events_by_condition` with a condition that activates events with high priority."""
    scheduler = EventScheduler()
    event1 = Event(time=5, context={'priority': 'high'})  # Should be activated
    event2 = Event(time=10, context={'priority': 'low'})  # Should remain inactive
    event3 = Event(time=15, context={'priority': 'high'})  # Should be activated
    
    event1.deactivate()
    event2.deactivate()
    event3.deactivate()
    
    scheduler.schedule(event1)
    scheduler.schedule(event2)
    scheduler.schedule(event3)
    
    scheduler.activate_all_events_by_condition(has_high_priority_condition)
    
    assert event1.status == EventStatus.ACTIVE, "High priority event1 should be activated."
    assert event2.status == EventStatus.INACTIVE, "Low priority event2 should remain inactive."
    assert event3.status == EventStatus.ACTIVE, "High priority event3 should be activated."

def test_activate_all_events_by_condition_mixed_conditions():
    """Test `activate_all_events_by_condition` with events of mixed times and contexts."""
    scheduler = EventScheduler()
    event1 = Event(time=5, context={'priority': 'high'})    # Should be activated (high priority)
    event2 = Event(time=25, context={'priority': 'low'})    # Should remain inactive
    event3 = Event(time=15, context={'priority': 'medium'}) # Should remain inactive
    event4 = Event(time=10, context={'priority': 'high'})   # Should be activated (high priority)
    
    event1.deactivate()
    event2.deactivate()
    event3.deactivate()
    event4.deactivate()
    
    scheduler.schedule(event1)
    scheduler.schedule(event2)
    scheduler.schedule(event3)
    scheduler.schedule(event4)
    
    scheduler.activate_all_events_by_condition(has_high_priority_condition)
    
    assert event1.status == EventStatus.ACTIVE, "High priority event1 should be activated."
    assert event2.status == EventStatus.INACTIVE, "Low priority event2 should remain inactive."
    assert event3.status == EventStatus.INACTIVE, "Medium priority event3 should remain inactive."
    assert event4.status == EventStatus.ACTIVE, "High priority event4 should be activated."

def test_activate_all_events_by_condition_partial_activation():
    """Test `activate_all_events_by_condition` with events of mixed priorities and times."""
    scheduler = EventScheduler()
    event1 = Event(time=5, context={'priority': 'low'})   # Should remain inactive (low priority)
    event2 = Event(time=10, context={'priority': 'high'}) # Should be activated (high priority)
    event3 = Event(time=25, context={'priority': 'high'}) # Should be activated (high priority)
    event4 = Event(time=30, context={'priority': 'low'})  # Should remain inactive (low priority)
    
    event1.deactivate()
    event2.deactivate()
    event3.deactivate()
    event4.deactivate()
    
    scheduler.schedule(event1)
    scheduler.schedule(event2)
    scheduler.schedule(event3)
    scheduler.schedule(event4)
    
    scheduler.activate_all_events_by_condition(has_high_priority_condition)
    
    assert event1.status == EventStatus.INACTIVE, "Low priority event1 should remain inactive."
    assert event2.status == EventStatus.ACTIVE, "High priority event2 should be activated."
    assert event3.status == EventStatus.ACTIVE, "High priority event3 should be activated."
    assert event4.status == EventStatus.INACTIVE, "Low priority event4 should remain inactive."

