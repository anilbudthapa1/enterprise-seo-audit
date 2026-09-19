import pytest
from core.state_machine import State, transition

def test_no_implementing_to_completed():
    with pytest.raises(ValueError):
        transition(State.IMPLEMENTING, State.COMPLETED)

def test_verified_to_completed():
    assert transition(State.VERIFIED, State.COMPLETED)==State.COMPLETED
