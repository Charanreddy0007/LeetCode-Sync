import sqlite3
import config

# creates connection
def getConnection():
    return sqlite3.connect(config.DATABASE)
