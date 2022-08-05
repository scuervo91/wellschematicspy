from pydantic import BaseModel, Extra, validator, Field
from pydantic.color import Color
from typing import List, Optional
import pandas as pd
from datetime import date

class SectionModel(BaseModel):
    name:str = Field(...)
    top: float = Field(...)
    bottom: float = Field(...)
    install_date: Optional[date] = Field(None)
    remove_date: Optional[date] = Field(None)

    class Config:
        validate_assignment = True
        extra = Extra.ignore
        
    def is_installed_at_date(self, date:date):
        if self.install_date is None:
            return False
        if self.install_date is not None and self.remove_date is not None:
            return self.install_date <= date <= self.remove_date
        if self.install_date is not None and self.remove_date is None:
            return date >= self.install_date
        if self.install_date is None and self.remove_date is None:
            return False
    
    def to_series(self):
        return pd.Series(self.dict())

class OpenHole(SectionModel):
    diameter: float = Field(...)  
    color: Color = Field('#cfd4d3')
    hatch: Optional[str] = Field(None)

    class Config:
        validate_assignment = True
        validate_all = True
        extra = Extra.ignore

    
class Cement(SectionModel):
    oh: float = Field(...) 
    color: Color = Field('#60b1eb')
    hatch: str = Field('.')

    class Config:
        validate_assignment = True
        validate_all = True
        extra = Extra.ignore
    
class Perforation(SectionModel):
    oh: float = Field(...) 
    color: Color = Field('#030302')
    hatch: str = Field('*')
    scale: float = Field(1)
    penetrate: float = Field(1.1)

    class Config:
        validate_assignment = True
        validate_all = True
        extra = Extra.ignore
    
class Casing(SectionModel):
    diameter: float = Field(...) 
    cement: Optional[List[Cement]] = Field(None)
    perforations: Optional[List[Perforation]]  = Field(None)
    pipe_width: float = Field(0.03, gt=0)
    shoe_scale: float = Field(5, gt=0)
    color: Color = Field('Black')
    
    class Config:
        validate_assignment = True
        validate_all = True
        extra = Extra.ignore
        
class Tubing(SectionModel):
    diameter: float  = Field(...)
    pipe_width: float = Field(0.02, gt=0)
    color: Color = Field('#828783')
    hatch: str = Field(None)

    class Config:
        validate_assignment = True
        validate_all = True
        extra = Extra.ignore
    
class BridgePlug(SectionModel):
    diameter: float  = Field(...)
    color: Color = Field('#7a2222')
    hatch: str = Field('xx')

    class Config:
        validate_assignment = True
        validate_all = True
        extra = Extra.ignore

class Sleeve(SectionModel):
    diameter: float  = Field(...)
    color: Color = Field('#74876d')
    hatch: str = Field('|')

    class Config:
        validate_assignment = True
        validate_all = True
        extra = Extra.ignore
    
class Plug(SectionModel):
    diameter: float  = Field(...)
    color: Color = Field('#60b1eb')
    hatch: str = Field('..')

    class Config:
        validate_assignment = True
        validate_all = True
        extra = Extra.ignore

class Packer(SectionModel):
    diameter: float  = Field(...)
    inner_diameter: float  = Field(...)
    color: Color = Field('#7a2222')
    hatch: str = Field('xx')

    class Config:
        validate_assignment = True
        validate_all = True
        extra = Extra.ignore
    
    @validator('inner_diameter')
    def check_inner_dia_is_less_diameter(cls,v, values):
        if v >= values['diameter']:
            raise ValueError('inner_diameter must be less than diameter')
        return v
    
    

    

    
    

