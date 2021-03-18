import sqlite3
import copy


class Database():
    def __init__(self):
        self.insert_artist = "INSERT INTO Artists(spotify_id,name,count) Values(?,?,?)"

    def select_query(self, query_string, *args):
        con = sqlite3.connect('./sqllite/artistwatch.db')
        cur = con.cursor()
        cur.execute(query_string, args)
        result = cur.fetchall()
        con.close()
        return result

    def get_id_count(self):
        con = sqlite3.connect('./sqllite/artistwatch.db')
        cur = con.cursor()
        cur.execute('SELECT spotify_id,count,channel_id FROM Artists')
        res = cur.fetchall()
        con.close()
        return res

    def new_artist(self, *args):
        print(args)
        con = sqlite3.connect('./sqllite/artistwatch.db')
        cur = con.cursor()
        cur.execute(
            'INSERT INTO Artists(spotify_id,name,count,imageref,channel_id) Values(?,?,?,?,?)', args)
        con.commit()
        con.close()

    def update_count(self, spotify_id, new_count):
        print("UPDATE COUNT")
        con = sqlite3.connect('./sqllite/artistwatch.db')
        cur = con.cursor()
        cur.execute(
            'UPDATE Artists SET count = (?) WHERE spotify_id= (?)', (new_count, spotify_id))
        con.commit()
        con.close()

    def get_artists(self, channel_id):
        con = sqlite3.connect('./sqllite/artistwatch.db')
        cur = con.cursor()
        cur.execute(
            "SELECT spotify_id,name,imageref FROM Artists WHERE channel_id=?", (channel_id,))
        result = cur.fetchall()
        resultList = []
        for row in result:
            dict = {'spotify_id': row[0], 'name': row[1], 'image_ref': row[2]}
            resultList.append(copy.deepcopy(dict))
        con.close()
        return resultList


if __name__ == "__main__":
    db = Database()
    db.new_artist('3213', 'name', 32, 'ref', 'mychannel')
    print(Database().select_query(
        "SELECT * FROM Artists "))
