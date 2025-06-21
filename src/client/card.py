class Card:
    zero = None

    def __init__(
        self,
        damage: None | int,
        health: None | int,
        name: str,
        card_type: str = "",
        keywords: str = "",
    ):
        self.name = name
        self.keywords = keywords
        self.card_type = card_type
        self.damage = str(damage) if damage != None else ""
        self.health = str(health) if health != None else ""

    def render(self):
        res = [
            (
                " |>---|---<| "
                if self.card_type == ""
                else " |-<{type:^5}>-| ".format(type=self.card_type)
            ),
            " |{damage:^4}|{health:^4}| ".format(
                damage=self.damage, health=self.health
            ),
            " |>---|---<| ",
            " |{name:^9}| ".format(name=self.name),
            " |{status:^9}| ".format(status=""),
            " |{keyword:^9}| ".format(keyword=self.keywords),
            " |>-------<| ",
        ]
        return res

    @classmethod
    def blank(cls):
        if cls.zero is None:
            cls.zero = Card(None, None, "")
            return cls.zero
        return cls.zero


def generate_board(
    ally: list[Card], enemy: list[Card], ally_health: int, enemy_health: int
) -> list[str]:
    res: list[str] = []
    renders = [card.render() for card in enemy]
    for line in range(6, -1, -1):
        text = ""
        for render in renders:
            text += render[line]
        res.append(text)
    res.append("                                                                 ")
    res.append(
        " >=============<{:>2}>===========<vs.>===========<{:<2}>=============< ".format(
            ally_health, enemy_health
        )
    )
    res.append("                                                                 ")
    renders = [card.render() for card in ally]
    for line in range(7):
        text = ""
        for render in renders:
            text += render[line]
        res.append(text)
    return [line + "  ||" for line in res]


for line in generate_board(
    [Card.blank() for _ in range(5)], [Card.blank() for _ in range(5)], 20, 20
):
    print(line)
