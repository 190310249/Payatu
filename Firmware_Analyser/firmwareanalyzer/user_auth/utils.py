from enum import Enum 

class UserTypeEnumType(Enum):
    
    ENTERPRISE = "ENTERPRISE"
    ORGANISATION = "ORGANISATION"
    INDIVIDUAL = "INDIVIDUAL"
    
    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]

