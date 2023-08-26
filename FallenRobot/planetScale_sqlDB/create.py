import threading
from FallenRobot import con
from FallenRobot.planetScale_sqlDB.playerDB import check_user

class create: 
    def __init__(self):
        self.PLAYER_LOCK = threading.RLock()

    def add_player_db(self, user_id, username, level=0, xp=0, ruby=0):
        with self.PLAYER_LOCK:
            with con.cursor() as cur:
                if not check_user(user_id):
                    query = """
                    INSERT INTO playerDB (user_id, username, level, xp, ruby)
                    VALUES (%s, %s, %s, %s, %s)
                    """
                    cur.execute(query, (user_id, username, level, xp, ruby))
                    con.commit()
                else:
                    return False
