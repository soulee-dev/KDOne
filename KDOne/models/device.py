from dataclasses import dataclass
from typing import Dict, Any
from enum import Enum


class DeviceType(Enum):
    LIGHT = "1401"


class StatusType(Enum):
    OnOffStatus = "OnOffStatus"
    DimmingLevel = "DimmingLevel"
    DimmingFunction = "DimmingFunction"
    MaxDimmingLevel = "MaxDimmingLevel"


@dataclass
class Device:
    type: DeviceType
    group_id: int
    sub_id: int
    remark: str
    status_type: StatusType
    status: str

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Device":
        device_type = DeviceType(data.get("Device_Type", "1401"))
        status_type = StatusType(data.get("Status_Type", "OnOffStatus"))

        return cls(
            type=device_type,
            group_id=int(data.get("Group_Id", 0)),
            sub_id=int(data.get("Sub_Id", 0)),
            remark=data.get("Device_Remark", ""),
            status_type=status_type,
            status=data.get("Status", ""),
        )
