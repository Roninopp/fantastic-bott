import threading
from Powers.planetScale_sqlDB import con


class playerDataBase:
    def __init__(self, user_id, username, ruby, level, xp):
        self.user_id = user_id
        self.username = username
        self.ruby = ruby
        self.level = level
        self.xp = xp

    def to_dict(self):
        return {"user_id": self.user_id, "username": self.username, "ruby": self.ruby, "level": self.level, "xp": self.xp}


with con.cursor() as cur:
    cur.execute("""
        CREATE TABLE IF NOT EXISTS playerDB (
        user_id varchar(255) primary key, 
        username varchar(255),
        level BIGINT,
        xp BIGINT,
        ruby INT
        )
    """)
    con.commit()
    cur.close()


PLAYER_LOCK = threading.RLock()


def check_user(user_id):
    with PLAYER_LOCK:
        cur = con.cursor()
        query = "SELECT * FROM playerDB WHERE user_id = %s"
        cur.execute(query, (user_id,))
        user = cur.fetchone()
        cur.close()
        if not user:
            return False
        else:
            return True
