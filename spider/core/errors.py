"""Excepciones personalizadas para el módulo spider."""


class HumbleSpiderError(RuntimeError):
    """Errores controlados del spider."""


class ImageUrlScraperError(RuntimeError):
    """Errores al scrapear URLs de imágenes."""

