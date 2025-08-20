from SvintTypes.plugin import SvintPlugin
import logging
import pathlib
import asyncio
from telebot import async_telebot
import yaml

class telegram(SvintPlugin):
    def Enable(self):
        with open(pathlib.Path(self.path, "localisation.yaml")) as f:
            self.localisation = yaml.safe_load(f)

        self.bot = async_telebot.AsyncTeleBot(
            self.config.get("tgToken"),
            parse_mode="Markdown"
        )        

        self.bot.register_message_handler(self.onStartCommand, commands=["start"])
        self.bot.register_message_handler(self.onTextMessage, content_types=["text"])
        self._registerEvent("start_message", isAsync=True)
        self._registerEvent("text_messages", isAsync=True)
        self._setEventResponder("get_bot", lambda: self.bot)

        self._addEventListener("core.loaded", self.OnSvintLoaded)   

    async def onStartCommand(self, message):
        logging.debug("Start commang handler!")
        await self.bot.send_message(message.chat.id, self.localisation.get("startMessage"))
        await self._asyncCallEvent("telegram.start_message", message=message)

    async def onTextMessage(self, message):
        await self._asyncCallEvent("telegram.text_message")

    def OnSvintLoaded(self, event):
        logging.info("Start bot polling!")
        asyncio.create_task(self.bot.polling(non_stop=True))
