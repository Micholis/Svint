from pluginManager import pluginManager as pm
from manifestManager import PluginManifest

class SvintPlugin:
    def __init__(self, manifest: PluginManifest, pluginManager: pm):
        self.manifest = manifest
        self.Svint = pluginManager
        self.id = manifest.getID()
        self.Enable()

    def Enable(self):
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
        return await self.Svint.callEvent(self.id, eventName, **kwargs)