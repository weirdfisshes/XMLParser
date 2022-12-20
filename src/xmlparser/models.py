import dataclasses


@dataclasses.dataclass()
class FlowerPriceItem():
    code: int
    name: str
    group: str | None
    price: float | None
