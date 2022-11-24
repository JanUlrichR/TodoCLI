from enum import Enum

priority_ids = {
    "Low": "4",
    "Medium": "3",
    "High": "2",
    "Highest": "1",
}


class Priority(str, Enum):
    low = "Low"
    medium = "Medium"
    high = "High"
    highest = "Highest"

    def to_priority_id(self):
        return priority_ids[self]
