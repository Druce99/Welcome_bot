from enum import Enum


class UserRole(str, Enum):
    BUYER = "buyer"
    OWNER = "owner"


class MessageType(str, Enum):
    CASE = "case"
    OFFER = "offer"
