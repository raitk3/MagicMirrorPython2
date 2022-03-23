from enum import Enum, auto

class ExtendedEnum(Enum):

    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))

class Size(ExtendedEnum):
    XXXX_SMALL = 12
    XXX_SMALL = 15
    XX_SMALL = 18
    X_SMALL = 24
    SMALL = 36
    MEDIUM = 48
    LARGE = 64
    X_LARGE = 72
    XX_LARGE = 96
    XXX_LARGE = 144 