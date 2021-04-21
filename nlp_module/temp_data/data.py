from enum import Enum


class GetTempIndexStatus(Enum):
    OK = 1
    UNKNOWN = 2
    UPDATE = 3


class GetTempIndexResult:
    status: GetTempIndexStatus = 1
    temp_index: int = None
