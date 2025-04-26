import logging

# Берем уже настроенный uvicorn-логгер
uvicorn_logger = logging.getLogger("uvicorn")

# Создаем свой логгер
logger = logging.getLogger(__name__)

# Чтобы не было пустого логгирования, копируем обработчики и уровень из uvicorn
logger.handlers = uvicorn_logger.handlers
logger.setLevel(logging.INFO)

# Чтобы избежать дублирования сообщений
logger.propagate = False

# Теперь экспортируем удобные короткие ссылки:
info = logger.info
debug = logger.debug
warning = logger.warning
error = logger.error
exception = logger.exception  # для логирования исключений с traceback
