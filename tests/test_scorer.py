from doompets.scorer import classify_window, score, state_for


def test_classification():
    assert classify_window("YouTube - funny cats") == "doom"
    assert classify_window("main.py - Visual Studio Code") == "productive"
    assert classify_window("File Explorer") == "other"


def test_score_range():
    assert 0 <= score(0, 0) <= 100
    assert score(40, 0) == 100


def test_states():
    assert state_for(10, 0) == "normal"
    assert state_for(40, 0) == "concerned"
    assert state_for(80, 0) == "angry"
    assert state_for(10, 21) == "happy"
