import logging

log = logging

log.basicConfig(filename='logs/app.log', filemode='w',
                format='%(levelname)s - %(asctime)s - %(message)s', level=logging.INFO)
log.basicConfig(filename='logs/app.log', filemode='w',
                format='%(levelname)s - %(asctime)s - %(message)s', level=logging.ERROR)
log.basicConfig(filename='logs/app.log', filemode='w',
                format='%(levelname)s - %(asctime)s - %(message)s', level=logging.CRITICAL)