import logging

# We take the already configured uvicorn logger
uvicorn_logger = logging.getLogger("uvicorn")

# Create your own logger
logger = logging.getLogger(__name__)

# To avoid empty logging, copy the handlers and level from uvicorn
logger.handlers = uvicorn_logger.handlers
logger.setLevel(logging.INFO)

# To avoid duplicate messages
logger.propagate = False

# Now we export convenient short links
info = logger.info
debug = logger.debug
warning = logger.warning
error = logger.error
exception = logger.exception  # for logging exceptions with traceback
