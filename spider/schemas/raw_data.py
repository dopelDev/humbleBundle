from datetime import datetime
from typing import Any, Dict, Optional

from pydantic import BaseModel, Field


class LandingPageRawDataRecord(BaseModel):
    """
    Schema Pydantic para validar y representar el raw data de landingPage-json-data.
    
    Contiene el JSON completo obtenido del script landingPage-json-data junto
    con metadata sobre cuándo y de dónde se obtuvo.
    """
    json_data: Dict[str, Any] = Field(description='JSON completo de landingPage-json-data')
    scraped_date: datetime = Field(default_factory=datetime.utcnow, description='Fecha de scraping')
    source_url: str = Field(description='URL de donde se obtuvo el JSON')
    json_hash: Optional[str] = Field(default=None, description='Hash del JSON para detectar cambios')
    json_version: Optional[str] = Field(default=None, description='Versión o identificador del formato JSON')

    def to_orm_payload(self) -> dict:
        """
        Convierte el LandingPageRawDataRecord a un diccionario compatible con ORM.
        
        Returns:
            Diccionario con los datos listos para persistir en BD.
        """
        return self.model_dump()

