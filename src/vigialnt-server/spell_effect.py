from card import Unit
from keywords import Keyword


def give_keyword(targets: list[Unit], keyword: Keyword) -> None:
    for target in targets:
        target.add_child(keyword)
