from enum import Enum, IntEnum


class GenderChoices(Enum):
    male = 'male'
    female = 'female'
    none = ''
    

class CivilStatChoices(Enum):
    single = 'single'
    married = 'married'
    livein = 'livein'
    none = ''


class PermChoices(Enum):
    user = 'user'
    group = 'group'
    

class TaxoTypeChoices(IntEnum):
    generic = 1
    category = 2
    tag = 3
