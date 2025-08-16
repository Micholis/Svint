from SvintTypes.plugin import SvintPlugin
import logging
from . import WordMaster
import asyncio
import aiogram

class telegram(SvintPlugin):
    def Enable(self):
        WordMaster.tgClass = self
        WordMaster.addWords()
        self._addEventListener("core.loaded", self.OnSvintLoaded)    

    def OnSvintLoaded(self, event):
        logging.debug("Svint loaded!")
        logging.info(WordMaster.getWord("startMessage"))
