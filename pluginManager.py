import importlib
import logging
import manifestManager
import pathlib
import utils
import os
import SvintTypes

class pluginManager:
    def __init__(self):
        self.loadedPlugins = {}
        self.registeredEvents = {}

    def loadPlugin(self, pluginName):
        if pluginName in self.loadedPlugins.keys(): 
            logging.debug(f"{pluginName} is already installed.")
            return self.loadedPlugins.get(pluginName)["version"]

        if not pluginName in os.listdir("plugins"):
            logging.error(f"Try to load uninstalled plugin {pluginName}!")
            return None

        logging.info(f"Loading plugin {pluginName}")
        pluginPath = pathlib.Path("plugins", pluginName)
        pluginManifest = manifestManager.PluginManifest(pluginPath)
        logging.debug(f"Hello {pluginName} {pluginManifest.getVersion()}!")

        logging.debug("Checking svint version")
        if pluginManifest.getSvintVersion() < utils.SVINT_VERSION:
            logging.fatal(f"Error when loading {pluginName}")
            logging.fatal(f"This plugin requires svint version {pluginManifest.getSvintVersion()}, but {utils.SVINT_VERSION} is installed!")
            logging.info("Try to update svint")
            utils.crash()

        logging.debug("Loading dependencies...")
        for dep, version in pluginManifest.getDependencies().items():
            logging.debug(f"loading dependence {dep}")
            if dep in self.loadedPlugins.keys() and self.loadedPlugins[dep]["version"] >= version: 
                logging.debug(f"{dep} is already installed.")
            depVer = self.loadPlugin(dep)
            if depVer == None:
                logging.fatal(f"Error when loading {pluginName}")
                logging.fatal(f"This plugin requires plugin {dep} {version}, but it is not installed!")
                utils.crash()
            if depVer < version:
                logging.fatal(f"Error when loading {pluginName}")
                logging.fatal(f"This plugin requires plugin {dep} {version}, but version {depVer} is installed!")
                utils.crash()
        logging.debug("All dependencies are safely loaded!")

        logging.debug("Now we're finally downloading this fucking plugin")
        pluginModule = importlib.import_module(f"plugins.{pluginName}")
        pluginClass = getattr(pluginModule, pluginName)
        pluginInstance = pluginClass(pluginManifest, self)
        self.loadedPlugins[pluginName] = {
            "id": pluginName,
            "version": pluginManifest.getVersion(),
            "instance": pluginInstance
        }
        logging.info(f"Safely loaded {pluginName}")

        return pluginManifest.getVersion()

    def loadAllPluggins(self):
        logging.info("Loading all plugins...")
        for plugin in os.listdir("plugins"):
            self.loadPlugin(plugin)
        logging.info("All plugins are safely loaded!")

    def callEvent(self, caller, eventName, **kwargs):
        logging.debug(f"Calling event {eventName} from {caller}")
        event = self.registeredEvents.get(eventName)
        if event is None:
            logging.warning(f"Called unregistered event {eventName}!")
            return None
        if event.asyncCallback == True:
            logging.warning(f"Sync calling async event {event.name}!")
            return None
        eventBody = SvintTypes.CalledEvent(caller, kwargs)
        if event.eventType == SvintTypes.EventTypes.MULTICALL:
            for callback in event.callbacks:
                callback(eventBody)
            return None
        elif event.eventType == SvintTypes.EventTypes.SINGLE:
            return event.callback(eventBody)
        
    async def asyncCallEvent(self, caller, eventName, **kwargs):
        logging.debug(f"Calling event {eventName} from {caller}")
        event = self.registeredEvents.get(eventName)
        if event is None:
            logging.warning(f"Called unregistered event {eventName}!")
            return None
        if event.asyncCallback == False:
            logging.warning(f"Async calling sync event {event.name}!")
            return None
        eventBody = SvintTypes.CalledEvent(caller, kwargs)
        if event.eventType == SvintTypes.EventTypes.MULTICALL:
            for callback in event.callbacks:
                await callback(eventBody)
            return None
        elif event.eventType == SvintTypes.EventTypes.SINGLE:
            return await event.callback(eventBody)
        
    def registerEventWithResponse(self, registerer, eventName, asyncCallback = False):
        name = f"{registerer}.{eventName}"
        if self.registeredEvents.get(name) != None:
            logging.warning(f"Event {name} is already registered! Rewriting...")
        self.registeredEvents[name] = SvintTypes.SvintSingleEvent(
            asyncCallback=asyncCallback,
            name=name,
            registeredBy=registerer,
            pluginWithListener=None,
            callback=None
        )
        logging.info(f"Registered new single event: {name}")

    def registerEvent(self, registerer, eventName, asyncCallback = False):
        name = f"{registerer}.{eventName}"
        if self.registeredEvents.get(name) != None:
            logging.warning(f"Event {name} is already registered! Rewriting...")
        self.registeredEvents[name] = SvintTypes.SvintMulticallEvent(
            asyncCallback=asyncCallback,
            name=name,
            registeredBy=registerer,
            pluginsWithListeners=[],
            callbacks=[]
        )
        logging.info(f"Registered new multicall event: {name}")

    def addEventListener(self, registerer, eventName, callback):
        logging.info(f"Adding new event listener for event {eventName}")
        event = self.registeredEvents.get(eventName)
        if event is None:
            logging.warning(f"Registering event listener on unregistered event {eventName}!")
            return
        if event.eventType == SvintTypes.EventTypes.SINGLE:
            if event.callback != None:
                logging.warning(f"Event listener for event {eventName} is already registered! Rewriting...")
            event.callback = callback
            event.pluginWithListener = registerer
            self.registeredEvents[eventName] = event
        elif event.eventType == SvintTypes.EventTypes.MULTICALL:
            event.callbacks.append(callback)
            event.pluginsWithListeners.append(registerer)
            self.registeredEvents[eventName] = event
        