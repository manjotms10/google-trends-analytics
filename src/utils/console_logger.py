import logging

'''
This file creates a logger that logs to the console. This is helpful in debugging the code. An example log line looks like the following - 
2019-12-02 20:01:28,941 | [google_trends.py __init__:29] | [INFO] - Successfully connected session to Google Trends

It displays the time of logging, file and method that logged this line, whether its INFO, DEBUG, WARN or ERROR, and finally the log line.
'''

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