from typing import List


def transform_labels(labels: List[str]) -> List[str]:
    return list(map(lambda label: label.lower(), labels))
