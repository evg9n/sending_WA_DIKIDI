from os.path import exists

from selenium import webdriver  # Импортируем webdriver
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.common.by import By  # Для поиска элементов по CSS селекторам
from selenium.webdriver.chrome.service import Service  # Для указания пути к ChromeDriver
from selenium.webdriver.chrome.options import Options  # Для настроек браузера

from typing import Optional
import time

from loguru import logger


def get_message(path_file_message: str) -> Optional[list]:
    """
    Получить текст сообщения в виде списка строк
    :param path_file_message: Абсолютынй путь к тектовому файлу текста сообщения
    :return: list
    """
    with open(path_file_message, 'r', encoding='utf-8') as file:
        message = file.read()

    if message:
        return message.split('\n')

    return None


def send(path_driver: str, path_file_message: str, list_numbers: list,
         xpath_field_input: str, xpath_button: str, open_window: bool):
    """
    Отправка сообщений
    :param path_driver: Абсолютынй путь к вебдрайверу
    :param path_file_message: Абсолютынй путь к тектовому файлу текста сообщения
    :param list_numbers: Список номеров, ожидается в виде "79999999999"
    :param xpath_field_input: XPATH к полю ввода сообщение
    :param xpath_button: XPATH к кнопке отправить
    :param open_window: Открыть окно браузера? Первый раз обязательно, для входа в аккаунт

    :return: True - успешно, False - не успешно
    """
    new = False
    chrome_options = Options()

    if not exists('profile'):
        new = True

    if not open_window and not new:
        chrome_options.add_argument("--headless")

    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--user-data-dir=profile")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                                "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option("useAutomationExtension", False)

    service = Service(path_driver)

    # Открываем сайт
    with webdriver.Chrome(service=service, options=chrome_options) as driver:

        driver.get(f'https://web.whatsapp.com')
        time.sleep(10)
        if new or 'Используйте WhatsApp на' in driver.page_source:
            logger.error("Не авторизован")
            input('После входа нажмите enter и перезапустите программу: ')
            return

        message = get_message(path_file_message)
        if message is None:
            return

        for number in list_numbers:
            driver.get(f'https://web.whatsapp.com/send/?phone=+{number}')
            time.sleep(20)
            field_input = driver.find_element(By.XPATH, xpath_field_input)

            actions = ActionChains(driver=driver)
            actions.move_to_element(field_input)

            actions.click()
            for line in message:
                actions.send_keys(line)
                actions.key_down(Keys.SHIFT).send_keys(Keys.ENTER).key_up(Keys.SHIFT)

            # actions.perform()
            time.sleep(5)

            actions.send_keys(Keys.ENTER)
            actions.perform()

            # button_send = driver.find_element(By.XPATH, xpath_button)
            # button_send.click()

            logger.info(f'Отправлено на номер +{number}')
            time.sleep(5)
