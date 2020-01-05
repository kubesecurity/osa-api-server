#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Contains type definitions for the data model."""
from enum import Enum


class EventType(Enum):
    """Define the eventtype type, possible values: ISSUE/PULL_REQUEST/COMMIT."""

    ISSUE = "ISSUE"
    PULL_REQUEST = "PULL_REQUEST"
    COMMIT = "COMMIT"


class Severity(Enum):
    """Denote the severity of an identified CVE."""

    HIGH = "high"
    LOW = "low"
    MODERATE = "moderate"


class FeedBackType(Enum):
    """Denote the type of feedback(POSITIVE/NEGATIVE)."""

    POSITIVE = "positive"
    NEGATIVE = "negative"
