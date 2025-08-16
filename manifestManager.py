import yaml
import os
import pathlib
import logging

class SvintManifest:
    def __init__(self):
        if not "config.yaml" in os.listdir():
            with open("config.yaml", "w") as f:
                yaml.safe_dump({
                    "logging-level": "INFO"
                }, f)
        with open("config.yaml", "r", encoding="UTF-8") as f:
            self.config = yaml.safe_load(f)

    def getLoggingLevel(self):
        return logging._nameToLevel[self.config.get("logging-level")]
    
    def getLoggingFormat(self):
        form = self.config.get("logging-format")
        if form == "SHORT": return "[%(asctime)s] (%(levelname)s) %(message)s"
        elif form == "LONG": return "[%(asctime)s] in {%(filename)s %(funcName)s}: (%(levelname)s) %(message)s"
    
class PluginManifest:
    def __init__(self, pluginPath):
        with open(pathlib.Path(pluginPath, "manifest.yaml"), "r", encoding="UTF-8") as f:
            self.config = yaml.safe_load(f)

    def getDependencies(self):
        return self.config.get("dependencies")
    
    def getOptionalDependencies(self):
        return self.config.get("optionalDependencies")

    def getVersion(self):
        return self.config.get("version")
    
    def getSvintVersion(self):
        return self.config.get("svintVersion")
    
    def getID(self):
        return self.config.get("id")