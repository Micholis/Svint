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

        self.adminID = self.config.get("adminID")
        self.includedModules = self.config.get("includedModules")

        logging.info("Activated aditional modules in telegram:")
        for module, status in self.includedModules.items():
            if status: logging.info(f"  - {module}")

        self.bot.register_message_handler(self.onStartCommand, commands=["start"])
        self._registerEvent("start_message", isAsync=True)

        if self.includedModules.get("getID"):
            self.bot.register_message_handler(self.onGetID, commands=["getID"])

        self.bot.register_message_handler(self.onTextMessage, content_types=["text"])
        self._registerEvent("text_message", isAsync=True)

        self._setEventResponder("get_bot", lambda: self.bot)
        self._addEventListener("core.loaded.async", self.OnSvintLoaded)   

        logging.info("Start bot polling!")
        asyncio.create_task(self.bot.polling(non_stop=True))

    async def onStartCommand(self, message):
        logging.debug("Start commang handler!")
        await self.bot.send_message(message.chat.id, self.localisation.get("startMessage"))
        await self._asyncCallEvent("telegram.start_message", message=message)

    async def onGetID(self, message):
        logging.debug("GetID")
        await self.bot.send_message(message.from_user.id, 
                                    self.localisation.get("getID").format(id = message.from_user.id)
                                    )

    async def onTextMessage(self, message):
        logging.debug(f"New message from telegram: {message}")
        await self._asyncCallEvent("telegram.text_message")

    async def OnSvintLoaded(self, event):
        if self.includedModules.get("messageToAdminOnLoad"):
            await self.bot.send_message(self.adminID, self.localisation.get("svintLoaded"))
