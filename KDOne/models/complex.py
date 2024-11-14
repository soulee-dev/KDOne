from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class Complex:
    id: str
    name: str
    address: str
    flag: bool

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Complex":
        return cls(
            id=data.get("Complex", ""),
            name=data.get("Complex_Name", ""),
            address=data.get("Complex_Addr", ""),
            flag=bool(int(data.get("Complex_Flag", "0"))),
        )
