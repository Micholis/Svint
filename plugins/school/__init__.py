from SvintTypes.plugin import SvintPlugin
import sqlite3
import logging
import pathlib

class school(SvintPlugin):
    def Enable(self):
        self.telegramAvailable = self._pluginAvailable("telegram")
        self.database = sqlite3.connect(pathlib.Path(self.path, "diary.db"))
        logging.info("Successfully connected to database!")
        self.dbCursor = self.database.cursor()

        self.dbCursor.execute("CREATE TABLE diary(Date date, lessons json)")
        self.database.commit()

