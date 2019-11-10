import logging

# create logger
logger = logging.getLogger("google-trends-logger")
logger.setLevel(logging.DEBUG)

# create file handler which logs even debug messages
fh = logging.StreamHandler()
fh.setLevel(logging.DEBUG)

# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s | [%(filename)s %(funcName)s:%(lineno)d] | [%(levelname)s] - %(message)s')
fh.setFormatter(formatter)

# add the handlers to the logger
logger.addHandler(fh)