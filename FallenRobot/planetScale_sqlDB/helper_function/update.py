#!/usr/bin/python
# -*- coding: utf-8 -*-
import threading
from FallenRobot import con
from FallenRobot.planetScale_sqlDB.playerDB import check_user


class update:

    def __init__(self):
        self.PLAYER_LOCK = threading.RLock()

    def add_money(self, user_id, amount):
        with self.PLAYER_LOCK:
            cur = con.cursor()

            try:
                if check_user(user_id):
                    cur.execute('''
                    UPDATE playerDB
                    SET ruby = %s
                    WHERE user_id = %s
                ''',
                                (amount, user_id))
                    print 'added money'
                    con.commit()
            finally:
                cur.close()

    def add_xp(self, user_id, amount):
        with self.PLAYER_LOCK:
            try:
                if check_user(user_id):
                    cur = con.cursor()
                    cur.execute('''
                  UPDATE playerDB
                  SET xp = %s
                  WHERE user_id = %s
              ''',
                                (amount, user_id))
                    con.commit()
            finally:
                cur.close()
