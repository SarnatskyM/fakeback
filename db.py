import sqlite3
from flask import jsonify


class DB:
    def __init__(self):
        self.connection = sqlite3.connect("data.db")
        self.cursor = self.connection.cursor()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS card(id INTEGER PRIMARY KEY, card_number INTEGER, card_cvv INTEGER, card_gg INTEGER, card_mm INTEGER)")

    def get_cards(self):
        with self.connection:
            data = []
            result = self.cursor.execute(f"SELECT * FROM `card`").fetchall()
            for card in result:
                data.append({'id':card[0],'card_number':str(card[1])[-4::], 'card_cvv':True if card[2] else False, 'card_gg':card[3], 'card_mm':card[4]})
            return jsonify(data)

    def add_card(self, card_number, card_cvv, card_gg, card_mm):
        with self.connection:
            return self.cursor.execute(f"INSERT INTO `card` VALUES(?,?,?,?,?)", (None, card_number, card_cvv, card_gg, card_mm))


    def exist_card(self, card_number):
        with self.connection:
            result = self.cursor.execute(f'SELECT * FROM card WHERE card_number={card_number}').fetchall()
            return bool(len(result))
    
    def get_card(self, id):
        with self.connection:
            result = self.cursor.execute(f'SELECT * FROM card WHERE id={id}').fetchall()
            for i in result:
                data=[{'id':i[0], 'card_number':i[1], 'card_cvv':i[2], 'card_gg':i[3], 'card_mm':i[4]}]
            return jsonify(data)