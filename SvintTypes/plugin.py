from pluginManager import pluginManager as pm
from manifestManager import PluginManifest
import pathlib
import os 
import yaml

class SvintPlugin:
    def __init__(self, manifest: PluginManifest, pluginManager: pm):
        self.manifest = manifest
        self.Svint = pluginManager
        self.id = manifest.getID()
        self.path = pathlib.Path("plugins", self.id)

        if not "config.yaml" in os.listdir(self.path):
            with open(pathlib.Path(self.path, "config.yaml"), "w") as f:
                yaml.safe_dump(self.manifest.getConfig(), f)
                self.config = self.manifest.getConfig()
        else:
            with open(pathlib.Path(self.path, "config.yaml")) as f:
                self.config = yaml.safe_load(f)

        self.Enable()

    def Enable(self):
        pass

    async def EnableAsync(self):
        pass

    def _registerEvent(self, eventName, isAsync = False):
        self.Svint.registerEvent(self.id, eventName, isAsync)

    def _addEventListener(self, eventName, callback):
        self.Svint.addEventListener(self.id, eventName, callback)
    
    def _setEventResponder(self, eventName, callback, isAsync = False):
        self.Svint.registerEventWithResponse(self.id, eventName, isAsync)
        self.Svint.addEventListener(self.id, f"{self.id}.{eventName}", callback)

    def _callEvent(self, eventName, **kwargs):
        return self.Svint.callEvent(self.id, eventName, **kwargs)

    async def _asyncCallEvent(self, eventName, **kwargs):
        return await self.Svint.asyncCallEvent(self.id, eventName, **kwargs)
    
    def _pluginAvailable(self, pluginName):
        return pluginName in self.Svint.loadedPlugins.keys()