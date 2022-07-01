from pydantic import BaseModel
from typing import Any, List, Optional, Type


def ld_urn(unique_suffix: str) -> str:
    return f"urn:ngsi-ld:{unique_suffix}"


class Attr(BaseModel):
    type: Optional[str]
    value: Any

    @classmethod
    def from_value(cls, v: Any) -> Optional['Attr']:
        if v is None:
            return None
        return cls(value=v)


class FloatAttr(Attr):
    type = 'Number' 
    value: float


class TextAttr(Attr):
    type = 'Text'
    value: str

class Structured(Attr):
    type = 'StructuredValue' #StructuredValue
    value: dict

class Arrayed(Attr):
    type = 'StructuredValue' #StructuredValue
    value: list


class BaseEntity(BaseModel):
    id: str
    type: str

    def set_id_with_type_prefix(self, unique_suffix: str):
        own_id = f"{self.type}:{unique_suffix}"
        self.id = ld_urn(own_id)
        return self

    @classmethod
    def from_raw(cls, raw_entity: dict) -> Optional['BaseEntity']:
        own_type = cls(id='').type
        etype = raw_entity.get('type', '')
        if own_type != etype:
            return None
        return cls(**raw_entity)


class EntityUpdateNotification(BaseModel):
    data: List[dict]

    def filter_entities(self, entity_class: Type[BaseEntity]) -> [BaseEntity]:
        candidates = [entity_class.from_raw(d) for d in self.data]
        return [c for c in candidates if c is not None]



class OPEEntity (BaseEntity):
    type = 'Optimal_Planer_Parameters'
    Operators : Optional[Arrayed]
    Orders : Optional[Arrayed]



# class RawReading(BaseModel):
#     AcelR: Optional[float]
#     fz: Optional[float]
#     Diam: Optional[float]
#     ae: Optional[float]
#     HB: Optional[float]
#     geom: Optional[float]
#     Ra: Optional[float]

#     def to_machine_entity(self, entity_id) -> MachineEntity:
#         e = MachineEntity(id=entity_id)

#         e.AcelR = FloatAttr.from_value(self.AcelR)
#         e.fz = FloatAttr.from_value(self.fz)
#         e.Diam = FloatAttr.from_value(self.Diam)
#         e.ae = FloatAttr.from_value(self.ae)
#         e.HB = FloatAttr.from_value(self.HB)
#         e.geom = FloatAttr.from_value(self.geom)
#         e.Ra = FloatAttr.from_value(self.Ra)

#         return e
