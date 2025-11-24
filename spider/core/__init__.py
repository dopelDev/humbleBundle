"""Core del spider: lógica principal y excepciones."""

from .spider import HumbleSpider
from .errors import HumbleSpiderError

__all__ = ['HumbleSpider', 'HumbleSpiderError']

