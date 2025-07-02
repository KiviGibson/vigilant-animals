import sqlite3 as sql
from .units import listed_units
from .card import Card, CardEffect


class DeckBase:
    def __init__(self, file: str):
        self.db = sql.connect(":memory:")
        cursor = self.db.cursor()
        cards_table = """ 
            CREATE TABLE IF NOT EXISTS cards(
            Id INTEGER PRIMARY KEY,
            Name TEXT NOT NULL,
            Cost INTEGER NOT NULL,
            Type TEXT NOT NULL,
            Damage INTEGER,
            Health INTEGER,
            Desc TEXT
            )"""
        deck_table = """
            CREATE TABLE IF NOT EXISTS decks(
            Id INTEGER PRIMARY KEY,
            CardId INTEGER,
            DeckId INTEGER,
            FOREIGN KEY(CardId) REFERENCES cards(Id),
            FOREIGN KEY(DeckId) REFERENCES player_decks(Id)
            )"""
        user_decks_table = """
            CREATE TABLE IF NOT EXISTS player_decks(
            Id INTEGER PRIMARY KEY,
            Username TEXT,
            Name TEXT
            )"""
        cursor.execute(cards_table)
        cursor.execute(deck_table)
        cursor.execute(user_decks_table)
        self.db.commit()
        for index, card in enumerate(listed_units):
            sum: CardEffect = card().children[0]
            data = sum.info()
            if data == {}:
                continue
            cursor.execute(
                "INSERT INTO cards VALUES(?,?,?,?,?,?,?)",
                [
                    index,
                    data["name"],
                    data["cost"],
                    data["type"],
                    data["damage"],
                    data["health"],
                    data["desc"],
                ],
            )
        self.db.commit()

    def get_all_cards(self) -> list[dict]:
        cursor = self.db.cursor()
        get_cards = """SELECT * FROM cards"""
        cursor.execute(get_cards)
        res = []
        for d in cursor.fetchall():
            res.append(
                {
                    "id": d[0],
                    "name": d[1],
                    "cost": d[2],
                    "type": d[3],
                    "damage": d[4],
                    "health": d[5],
                    "desc": d[6],
                }
            )
        return res

    def edit_deck(
        self, name: str, username: str, new_deck: list[tuple[int, int]]
    ) -> None:
        cursor = self.db.cursor()
        id = self.get_deck_id(name, username)
        remove_current_config = """ DELETE FROM decks WHERE Id = ? """
        cursor.execute(remove_current_config, [id])
        self.db.commit()
        cursor_add_deck_config = """ INSERT INTO decks(CardId, DeckId) VALUES (?, ?)"""
        cursor.executemany(cursor_add_deck_config, new_deck)

    def create_deck(self, name: str, username: str) -> None:
        cursor = self.db.cursor()
        condition = """ SELECT COUNT(*) as num FROM player_decks WHERE Name = ? and Username = ?"""
        cursor.execute(condition, [name, username])
        if cursor.fetchall()[0] > 0:
            return
        add_deck = """ INSERT INTO player_decks(name, usernme) VALUES(?, ?)"""
        cursor.execute(add_deck, [name, username])

    def get_deck_id(self, name: str, username: str) -> int:
        cursor = self.db.cursor()
        get_index = """ SELECT Id FROM player_decks WHERE name = ? and username = ?"""
        cursor.execute(get_index, [name, username])
        return cursor.fetchone()[0]

    def get_deck_list(self, username: str) -> list[dict]:
        cursor = self.db.cursor()
        get_decks = """SELECT Id, Name FROM player_decks WHERE username = ?"""
        cursor.execute(get_decks, [username])
        res = []
        for data in cursor.fetchall():
            res.append({"id": data[0], "name": data[1]})
        return res
