from dataclasses import dataclass, field


@dataclass
class Grant:
    id: int | None = None

    source: str = ""

    amount: str = ""
    title: str = ""
    description: str = ""
    full_description: str = ""

    tags: list[str] = field(default_factory=list)

    company: str = ""
    deadline: str = ""
    status: str = ""

    url: str = ""

    embedding: list[float] | None = None