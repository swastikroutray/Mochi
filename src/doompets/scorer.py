from dataclasses import dataclass
from time import monotonic


@dataclass
class Session:
    app: str
    started_at: float
    seconds: float = 0.0


DOOM_APPS = ("youtube", "instagram", "reddit", "tiktok", "facebook", "x.com", "twitter")
PRODUCTIVE_APPS = ("code", "visual studio", "pycharm", "leetcode", "terminal", "powershell", "docs", "notion")


def classify_window(title: str) -> str:
    value = title.lower()
    if any(token in value for token in DOOM_APPS):
        return "doom"
    if any(token in value for token in PRODUCTIVE_APPS):
        return "productive"
    return "other"


def score(minutes_doom: float, minutes_productive: float) -> int:
    """Small, explainable v1 score. Range: 0..100."""
    raw = minutes_doom * 2.5 - minutes_productive * 1.0
    return max(0, min(100, round(raw)))


def state_for(score_value: int, productive_streak_minutes: float) -> str:
    if productive_streak_minutes >= 20:
        return "happy"
    if score_value >= 70:
        return "angry"
    if score_value >= 35:
        return "concerned"
    return "normal"
