from enum import Enum
import csv


class ScanType(Enum):
    passive = 0
    passive_and_active = 1


class Target:
    target: str
    should_spider: bool
    scan_type: ScanType

    def __init__(
        self,
        target: str,
        should_spider: bool,
        scan_type: ScanType,
    ) -> None:
        self.target = target
        self.should_spider = should_spider
        self.scan_type = scan_type

    @staticmethod
    def fromCSVRow(row: list[str]):
        target: str | None
        should_spider: bool | None
        scan_type: ScanType | None

        if row[0] == "":
            raise ValueError(f"CSV column 2 (third) must not be empty.")
        else:
            target = row[0]

        if len(row) < 2 or row[1] == "false":
            should_spider = False
        elif row[1] == "true":
            should_spider = True
        else:
            raise ValueError(
                f"CSV column 1 (second) value must be either `true` or `false`. Received `{row[0]}`."
            )

        if len(row) < 3 or row[2] == "passive":
            scan_type = ScanType.passive
        elif row[2] == "passive_and_active":
            scan_type = ScanType.passive_and_active
        else:
            raise ValueError(
                f"CSV column 2 (third) value must be either `passive` or `passive_and_active`. Received `{row[1]}`."
            )

        return Target(
            target=target,
            should_spider=should_spider,
            scan_type=scan_type,
        )


def get_targets(targets_file: str) -> list[Target]:
    targets: list[Target] = []
    with open(targets_file, "r") as file:
        data = csv.reader(file)
        for row in data:
            targets.append(Target.fromCSVRow(row))
    return targets
