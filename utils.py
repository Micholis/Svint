import logging

SVINT_VERSION = 0.1

def crash():
    logging.fatal("Oh! Svint is crashed! Try drinking some coffee and starting over.")
    logging.debug("Did you enable debugging? You clearly knew that you would break everything, but the important thing is to realize your mistake and try again)    ")
    exit()