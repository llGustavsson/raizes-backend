import enum

class RoleEnum(str, enum.Enum):
    ADMIN = "ADMIN"
    CUSTOMER = "CUSTOMER"

class ChannelEnum(str, enum.Enum):
    APP = "APP"
    TOTEM = "TOTEM"
    COUNTER = "COUNTER"
    WEB = "WEB"

class OrderStatusEnum(str, enum.Enum):
    CREATED = "CREATED"
    PAID = "PAID"
    CANCELED = "CANCELED"