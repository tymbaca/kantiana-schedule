from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions

from exceptions import *
from classes import *
from settings import *


def _init_browser():

    # Creating browser and maximizing the window
    browser = webdriver.Chrome(ChromeDriverManager().install())
    browser.maximize_window()
    browser.get(TARGET_URL)

    return browser


def _get_html(browser, group: str, date: str) -> str:
    # Finding input fields
    group_element = browser.find_element(By.ID, "select-state-selectized")
    date_element = browser.find_element(By.CLASS_NAME, "form-control")

    # Filling input fields
    group_element.send_keys(group + Keys.RETURN)
    date_element.send_keys(date + Keys.RETURN)

    wait = WebDriverWait(browser, 10)
    wait.until(expected_conditions.visibility_of(browser.find_element(by=By.CLASS_NAME, value="schedule")))
    return browser.page_source


def _get_html_list(group: str | int, entrance_year: str, start_date: datetime.datetime, day_count: int) -> list[str]:

    # Formatting data
    formatted_group = f'03_юр_{entrance_year}_О_/_{group}'
    formatted_dates_list = _get_formatted_dates_list(start_date, day_count)

    browser = _init_browser()

    try:
        html_list: list[str] = []
        for formatted_date in formatted_dates_list:
            html = _get_html(browser, group=formatted_group, date=formatted_date)
            html_list.append(html)

    except GetHtmlError as err:
        raise err
    finally:
        browser.close()
        browser.quit()

    return html_list


def _date_range(start_date: datetime.date, day_count):
    for day in range(day_count):
        yield start_date + datetime.timedelta(day)


def _get_formatted_dates_list(start_date: datetime.datetime, day_count: int) -> list[str]:
    formatted_dates_list: list[str] = []
    for date in _date_range(start_date, day_count):
        formatted_date = date.strftime(DATE_FORMAT)
        formatted_dates_list.append(formatted_date)
    return formatted_dates_list


def get_html_list(group: int = 1,
                  entrance_year: str = "19",
                  start_date: datetime.datetime | str = datetime.datetime.today(),
                  day_count: int = 365) -> list[str]:
    """Base function"""

    if type(start_date) is str:
        start_date = datetime.datetime.strptime(start_date, DATE_FORMAT)
        # start_date = start_datetime.date()

    html_list = _get_html_list(group, entrance_year, start_date, day_count)
    return html_list


if __name__ == '__main__':
    get_html_list(start_date="01.9.2022")
