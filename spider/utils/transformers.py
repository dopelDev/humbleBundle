from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Any, Iterable, Optional


BASE_URL = 'https://www.humblebundle.com'


def normalize_text(value: Optional[str]) -> Optional[str]:
    """
    Normaliza un texto eliminando espacios en blanco al inicio y final.
    
    Args:
        value: String a normalizar. Puede ser None.
        
    Returns:
        String normalizado sin espacios al inicio/final, o None si el
        valor es None o si después de limpiar queda vacío.
    """
    if value is None:
        return None
    cleaned = value.strip()
    return cleaned or None


def serialize_list(value: Any) -> Optional[str]:
    """
    Serializa una lista o estructura de datos a JSON string.
    
    Si el valor ya es un string, lo retorna tal cual. Si es una lista o
    diccionario, lo serializa a JSON. Si es None, string vacío o lista
    vacía, retorna None.
    
    Args:
        value: Valor a serializar. Puede ser cualquier tipo.
        
    Returns:
        String JSON serializado, o None si el valor es None/vacío.
    """
    if value in (None, '', []):
        return None
    if isinstance(value, str):
        return value
    try:
        return json.dumps(value, ensure_ascii=False)
    except (TypeError, ValueError):
        return str(value)


def absolute_url(value: Optional[str], base: str = BASE_URL) -> Optional[str]:
    """
    Convierte una URL relativa a una URL absoluta.
    
    Si la URL ya es absoluta (empieza con http:// o https://), la retorna
    tal cual. Si es relativa, la combina con la URL base.
    
    Args:
        value: URL relativa o absoluta. Puede ser None.
        base: URL base para construir URLs absolutas. Por defecto BASE_URL.
        
    Returns:
        URL absoluta o None si el valor es None o vacío.
    """
    if not value:
        return None
    if value.startswith('http://') or value.startswith('https://'):
        return value
    return f'{base.rstrip("/")}/{value.lstrip("/")}'


def safe_float(value: Any) -> Optional[float]:
    """
    Convierte un valor a float de forma segura.
    
    Intenta convertir el valor a float. Si el valor es None, string vacío
    o lista vacía, retorna None. Si la conversión falla, también retorna None.
    
    Args:
        value: Valor a convertir. Puede ser cualquier tipo.
        
    Returns:
        Float convertido o None si el valor es inválido o no convertible.
    """
    if value in (None, '', []):
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def compute_duration_days(start: Optional[datetime], end: Optional[datetime]) -> Optional[float]:
    """
    Calcula la duración en días entre dos fechas.
    
    Args:
        start: Fecha de inicio. Puede ser None.
        end: Fecha de fin. Puede ser None.
        
    Returns:
        Número de días (float con 3 decimales) entre las fechas, o None
        si alguna de las fechas es None.
    """
    if not start or not end:
        return None
    delta = end - start
    return round(delta.total_seconds() / 86400, 3)


def compute_is_active(start: Optional[datetime], end: Optional[datetime], now: Optional[datetime] = None) -> bool:
    """
    Determina si un bundle está activo en un momento dado.
    
    Un bundle está activo si la fecha/hora actual está entre la fecha
    de inicio y la fecha de fin (inclusive).
    
    Args:
        start: Fecha de inicio del bundle. Puede ser None.
        end: Fecha de fin del bundle. Puede ser None.
        now: Fecha/hora de referencia. Si es None, se usa la fecha/hora
            actual en UTC.
            
    Returns:
        True si el bundle está activo, False en caso contrario o si
        alguna fecha es None.
    """
    now = now or datetime.now(timezone.utc)
    if not start or not end:
        return False
    return start <= now <= end


def normalize_columns(frame, columns: Iterable[str]):
    """
    Normaliza las columnas especificadas de un DataFrame.
    
    Aplica la función normalize_text a todas las columnas especificadas
    que existan en el DataFrame, eliminando espacios en blanco al inicio
    y final de los valores.
    
    Args:
        frame: DataFrame de pandas a normalizar (se modifica in-place).
        columns: Iterable con los nombres de las columnas a normalizar.
    """
    for column in columns:
        if column in frame.columns:
            frame[column] = frame[column].apply(normalize_text)

