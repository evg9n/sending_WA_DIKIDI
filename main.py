# Логгер
from loguru import logger

from os.path import abspath, join

from clients import get_clients
# Константы
from constants import Constants
from send import send

constants = Constants()
logger.remove()
logger.add(
    abspath(join('logs', '{time:YYYY-MM-DD  HH.mm.ss}.log')),  # Путь к файлу логов с динамическим именем
    rotation=constants.ROTATION_LOGGER,  # Ротация логов каждый день
    compression="zip",  # Использование zip-архива
    level=constants.LEVEL_FILE_LOGGER,  # Уровень логирования
    format=constants.FORMAT_LOGGER,  # Формат вывода
    serialize=constants.SERIALIZE_LOGGER,  # Сериализация в JSON
)

# Вывод лога в консоль
logger.add(
    sink=print,
    level=constants.LEVEL_CONSOLE_LOGGER,
    format=constants.FORMAT_LOGGER,
)


if __name__ == '__main__':
    logger.info('RUN PROJECT')

    c = Constants()

    list_numbers = get_clients(c.PATH_FILE_CSV_CLIENT, delimiter=';')
    if list_numbers:
        send(path_driver=c.PATH_WEBDRIVER, path_file_message=c.PATH_FILE_MESSAGE_CLIENT, list_numbers=list_numbers,
             xpath_button=c.XPATH_BUTTON, xpath_field_input=c.XPATH_FIELD_INPUT, open_window=c.OPEN_WINDOW)
