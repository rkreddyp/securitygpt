from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Dict, Any, Optional

@dataclass
class URLResource:
    url: str
    description: Optional[str]
    visited: Optional[bool]
    content: Optional[str] = None
    title: str = None

