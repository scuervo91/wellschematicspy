from pydantic import BaseModel, Extra, validator, Field
from pydantic.color import Color
from typing import List, Optional

class SectionModel(BaseModel):
    name:str = Field(...)
    top: float = Field(...)
    bottom: float = Field(...)

    class Config:
        validate_assignment = True
        extra = Extra.forbid
        
class OpenHole(SectionModel):
    diameter: float = Field(...)  
    color: Color = Field('#cfd4d3')
    hatch: Optional[str] = Field(None)

    class Config:
        validate_assignment = True
        validate_all = True
        extra = Extra.forbid

    
class Cement(SectionModel):
    oh: float = Field(...) 
    color: Color = Field('#60b1eb')
    hatch: str = Field('.')

    class Config:
        validate_assignment = True
        validate_all = True
        extra = Extra.forbid
    
class Perforation(SectionModel):
    oh: float = Field(...) 
    color: Color = Field('#030302')
    hatch: str = Field('*')
    scale: float = Field(1)
    penetrate: float = Field(1.1)

    class Config:
        validate_assignment = True
        validate_all = True
        extra = Extra.forbid
    
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
        extra = Extra.forbid
        
class Tubing(SectionModel):
    diameter: float  = Field(...)
    pipe_width: float = Field(0.02, gt=0)
    color: Color = Field('#828783')
    hatch: str = Field(None)

    class Config:
        validate_assignment = True
        validate_all = True
        extra = Extra.forbid
    
class BridgePlug(SectionModel):
    diameter: float  = Field(...)
    color: Color = Field('#7a2222')
    hatch: str = Field('xx')

    class Config:
        validate_assignment = True
        validate_all = True
        extra = Extra.forbid

class Sleeve(SectionModel):
    diameter: float  = Field(...)
    color: Color = Field('#74876d')
    hatch: str = Field('|')

    class Config:
        validate_assignment = True
        validate_all = True
        extra = Extra.forbid
    
class Plug(SectionModel):
    diameter: float  = Field(...)
    color: Color = Field('#60b1eb')
    hatch: str = Field('..')

    class Config:
        validate_assignment = True
        validate_all = True
        extra = Extra.forbid

class Packer(SectionModel):
    diameter: float  = Field(...)
    inner_diameter: float  = Field(...)
    color: Color = Field('#7a2222')
    hatch: str = Field('xx')

    class Config:
        validate_assignment = True
        validate_all = True
        extra = Extra.forbid
    
    @validator('inner_diameter')
    def check_inner_dia_is_less_diameter(cls,v, values):
        if v >= values['diameter']:
            raise ValueError('inner_diameter must be less than diameter')
        return v
    
    

    

    
    

