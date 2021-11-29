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
    

class OptionTypeChoices(IntEnum):
    generic = 1
    
    
class MediaTypeChoices(IntEnum):
    avatar = 1
    gallery = 2
    others = 3