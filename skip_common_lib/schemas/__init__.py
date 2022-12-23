import pydantic as pyd


class CustomBaseModel(pyd.BaseModel):
    class Config:
        use_enum_values = True
        arbitrary_types_allowed = True
