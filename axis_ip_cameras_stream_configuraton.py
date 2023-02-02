"""script for adding stream on axis cameras v.P3225-LVE MKII RU"""
from pythonping import ping
import time
import pyautogui as pg
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException


username = ''  # write here username for login
password = ''  # write here password for login
inaccessible_cameras = []


def generate_ip_list(first_ip: str, number_of_cameras: int) -> list:
    """function to create a list of ip cameras adresses."""
    cameras_list = []
    last_number = int(first_ip.split('.')[-1])
    for _ in range(number_of_cameras):
        cameras_list.append(f'{first_ip[:-2]}{last_number+_}')
    return cameras_list


def check_cameras_access(list_of_cameras: list) -> list:
    unavailable_cameras = []
    for _ in range(len(list_of_cameras)):
        camera_ping = ping(f'{_}', verbose=True, timeout=0.1)
        if 'Request timed out' in str(camera_ping):
            print('adress unavailable')
            unavailable_cameras.append(str(camera_ping))
            list_of_cameras.pop(camera_ping[i])
        else:
            print('adress available')
    return list_of_cameras


cameras = list(generate_ip_list('192.168.0.90', 2))  # example of input values
available_cameras = check_cameras_access(cameras)

for i in range(len(cameras)):
    try:
        with webdriver.Chrome() as browser:
            browser.get(f'http://{cameras[i]}/')
            action = ActionBuilder(browser)
            pg.click(769, 271)
            pg.typewrite(username)
            time.sleep(0.5)
            pg.click(769, 291)
            pg.typewrite(password)
            pg.click(709, 365)
            browser.set_window_size(1590, 850)
            setup_key = WebDriverWait(browser, 2).until(
                EC.presence_of_element_located((By.ID, "view_SetTxt1")))
            setup_key.click()
            video_setup = WebDriverWait(browser, 2).until(
                EC.presence_of_element_located((By.LINK_TEXT, "Video")))
            video_setup.click()
            stream_setup = WebDriverWait(browser, 2).until(
                EC.presence_of_element_located((By.LINK_TEXT, "Stream Profiles")))
            stream_setup.click()
            add_button = WebDriverWait(browser, 2).until(
                EC.presence_of_element_located((By.ID, "addBtn")))
            add_button.click()
            time.sleep(0.5)
            browser.switch_to.window(browser.window_handles[1])
            browser.set_window_size(1000, 1000)
            time.sleep(0.5)
            browser.switch_to.frame('settings')
            profile_name = browser.find_element(By.NAME, 'StreamProfile_Name')
            profile_name.send_keys('1')
            resolution_select = browser.find_element(By.ID, 'resolution')
            x = Select(resolution_select)
            x.select_by_value('1024x768')
            time.sleep(0.5)
            fps = WebDriverWait(browser, 2).until(
                EC.presence_of_element_located((By.NAME, "fps")))
            fps.send_keys(Keys.BACKSPACE, Keys.BACKSPACE)
            fps.send_keys('15')
            save_button = browser.find_element(By.NAME, 'save')
            save_button.click()
            browser.switch_to.window(browser.window_handles[0])
            add_button = WebDriverWait(browser, 2).until(
                EC.presence_of_element_located((By.ID, "addBtn")))
            add_button.click()
            browser.switch_to.window(browser.window_handles[1])
            browser.switch_to.frame('settings')
            profile_name = browser.find_element(By.NAME, 'StreamProfile_Name')
            profile_name.send_keys('2')
            resolution_select = browser.find_element(By.ID, 'resolution')
            x = Select(resolution_select)
            x.select_by_value('320x180')
            time.sleep(0.5)
            fps = WebDriverWait(browser, 2).until(
                EC.presence_of_element_located((By.NAME, "fps")))
            fps.send_keys(Keys.BACKSPACE, Keys.BACKSPACE)
            fps.send_keys('15')
            save_button = browser.find_element(By.NAME, 'save')
            time.sleep(0.5)
            save_button.click()
            time.sleep(5)
    except WebDriverException:
        print('ping camera')
print('Camera streams was added')
