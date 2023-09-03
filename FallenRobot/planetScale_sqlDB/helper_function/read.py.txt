import threading
from FallenRobot import con
from FallenRobot.planetScale_sqlDB.playerDB import check_user
import json


class read:
    def __init__(self):
        self.PLAYER_LOCK = threading.RLock()

    def ruby(self, user_id):
        with self.PLAYER_LOCK:
            cur = con.cursor()
            cur.execute(f'''
                            SELECT ruby 
                            FROM playerDB 
                            WHERE user_id = {user_id}
                            ''')
            pd = cur.fetchone()
            cur.close()
            if pd == None:
                return 0
            else:
                return pd[0]
    def xp(self, user_id):
        with self.PLAYER_LOCK:
            cur = con.cursor()
            cur.execute(f'''
                            SELECT xp 
                            FROM playerDB 
                            WHERE user_id = {user_id}
                            ''')
            pd = cur.fetchone()
            cur.close()
            if pd == None:
                return 0
            else:
                return pd[0]
