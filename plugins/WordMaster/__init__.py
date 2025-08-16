from SvintTypes.plugin import SvintPlugin
import pathlib
import os
import logging
import yaml

class WordMaster(SvintPlugin):
    def Enable(self):
        self._setEventResponder("registerWord", self.registerWord)
        self._setEventResponder("getWord", self.getWord)
        pass

    def registerWord(self, event):
        plugin = event.caller
        pluginPath = pathlib.Path("plugins", plugin)
        localsPath = pathlib.Path(pluginPath, "words.yaml")
        if "words.yaml" in os.listdir(pluginPath):
            logging.debug(f"Words for {plugin} is already exist, ignoring")
            return
        words = event.params.get("words")
        with open(localsPath, "w") as f:
            yaml.safe_dump(words, f, encoding="UTF-8")
        
    def getWord(self, event):
        plugin = event.caller
        pluginPath = pathlib.Path("plugins", plugin)
        localsPath = pathlib.Path(pluginPath, "words.yaml")
        if not "words.yaml" in os.listdir(pluginPath):
            logging.warning(f"Plugin {plugin} do not translated!")
            return None
        with open(localsPath, "r") as f:
            words = yaml.safe_load(f)
        word = words.get(event.params.get("word"))
        if word is None:
            logging.warning(f"Trying to get unregistered word {event.params.get('word')} for plugin {plugin}")
            return None
        return word
        
        
        