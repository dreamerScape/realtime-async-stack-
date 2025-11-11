from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class ClosePollRequest(_message.Message):
    __slots__ = ("poll_id",)
    POLL_ID_FIELD_NUMBER: _ClassVar[int]
    poll_id: int
    def __init__(self, poll_id: _Optional[int] = ...) -> None: ...

class ClosePollResponse(_message.Message):
    __slots__ = ("status",)
    STATUS_FIELD_NUMBER: _ClassVar[int]
    status: str
    def __init__(self, status: _Optional[str] = ...) -> None: ...
