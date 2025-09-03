import logging
import utils
import asyncio

async def main():
    import manifestManager
    import pluginManager
    
    manifest = manifestManager.SvintManifest()
    logging.basicConfig(filename="latest.log", level=manifest.getLoggingLevel(), filemode="w", format=manifest.getLoggingFormat(), encoding="UTF-8")
    logging.info("Hello coder!")
    logging.debug("Oh, it looks like something went wrong for you to decide to turn on the debugger")
    plugins = pluginManager.pluginManager()
    plugins.registerEvent("core", "loaded")
    plugins.registerEvent("core", "tick")
    plugins.registerEvent("core", "loaded.async", asyncCallback=True)
    plugins.registerEvent("core", "tick.async", asyncCallback=True)
    await plugins.loadAllPluggins()   
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
    await plugins.asyncCallEvent("core", "core.loaded.async")

    await plugins.asyncCallEvent("core", "school.getDay", date="03-04-2025")
    while True:
        await asyncio.sleep(5)
        plugins.callEvent("core", "core.tick")
        await plugins.asyncCallEvent("core", "core.tick.async")
    
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        logging.exception("Oh, it looks like everything went wrong, Svint can't figure out the reason, it looks like you're going to do it, good luck;) \n")
        utils.crash()
