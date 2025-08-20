import logging
import utils
import asyncio

def load():
    import manifestManager
    import pluginManager
    
    manifest = manifestManager.SvintManifest()
    logging.basicConfig(filename="latest.log", level=manifest.getLoggingLevel(), filemode="w", format=manifest.getLoggingFormat(), encoding="UTF-8")
    logging.info("Hello coder!")
    logging.debug("Oh, it looks like something went wrong for you to decide to turn on the debugger")
    plugins = pluginManager.pluginManager()
    plugins.registerEvent("core", "loaded")
    plugins.registerEvent("core", "tick")
    plugins.loadAllPluggins()
    logging.info(f"Svint: {utils.SVINT_VERSION}")
    logging.info("  - Plugins:")
    for plugin in plugins.loadedPlugins.values():
        logging.info(f"    - {plugin.get('id')}: {plugin.get('version')}")
    logging.info("  - Now registered events:")
    for event in plugins.registeredEvents.values():
        logging.info(f"    - {event.name} ({event.eventType.name}) {'[ASYNC]' if event.asyncCallback else ''}")
    logging.info("-------------------------")
    logging.info(r"   _____      _       __ ")
    logging.info(r"  / ___/   __(_)___  / /_")
    logging.info(r"  \__ \ | / / / __ \/ __/")
    logging.info(r" ___/ / |/ / / / / / /_  ")
    logging.info(r"/____/|___/_/_/ /_/\__/  ")
    logging.info("-------------------------")
    logging.info("Done! Svint is loaded!")
    plugins.callEvent("core", "core.loaded")

    return manifest, plugins

async def main():
    manifest, plugins = load()
    while True:
        await asyncio.sleep(5)
        plugins.callEvent("core", "core.tick")
    
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        logging.exception("Oh, it looks like everything went wrong, Svint can't figure out the reason, it looks like you're going to do it, good luck;) \n")
        utils.crash()
