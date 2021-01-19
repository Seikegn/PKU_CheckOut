# -*- coding: utf-8
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from urllib.parse import quote
from urllib import request
import time
import warnings
import json
from configparser import ConfigParser
import warnings
import sys
import os

warnings.filterwarnings('ignore')


def login(userName, password, retry=0):
    if retry == 3:
        raise Exception('门户登录失败')

    print('门户登陆中...')

    appID = 'portal2017'
    iaaaUrl = 'https://iaaa.pku.edu.cn/iaaa/oauth.jsp'
    appName = quote('北京大学校内信息门户新版')
    redirectUrl = 'https://portal.pku.edu.cn/portal2017/ssoLogin.do'

    driver.get('https://portal.pku.edu.cn/portal2017/')
    driver.get(
        f'{iaaaUrl}?appID={appID}&appName={appName}&redirectUrl={redirectUrl}')
    WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.ID, 'logon_button')))
    driver.find_element_by_id('user_name').send_keys(userName)
    time.sleep(0.1)
    driver.find_element_by_id('password').send_keys(password)
    time.sleep(0.1)
    driver.find_element_by_id('logon_button').click()
    try:
        WebDriverWait(driver,
                      5).until(EC.visibility_of_element_located((By.ID, 'all')))
        print('门户登录成功！')
    except:
        print('Retrying...')
        login(driver, userName, password, retry + 1)

def go_to_simso():
    driver.find_element_by_id('all').click()
    WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.ID, 'tag_s_stuCampusExEnReq')))
    driver.find_element_by_id('tag_s_stuCampusExEnReq').click()
    time.sleep(1)
    driver.switch_to.window(driver.window_handles[-1])
    WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.CLASS_NAME, 'el-card__body')))

def go_to_application():
    go_to_simso()
    driver.find_element_by_class_name('el-card__body').click()
    WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.CLASS_NAME, 'el-input__inner')))

def locate_ul():
    #all_uls = WebDriverWait(driver, 5).until(
    #    EC.presence_of_element_located(
    #   (By.XPATH, '//ul[contains(@class,"el-scrollbar__view el-select-dropdown__list")]')))
    all_uls = driver.find_elements_by_xpath('//ul[contains(@class,"el-scrollbar__view el-select-dropdown__list")]')
    time.sleep(1)
    for ul in all_uls:
        if len(ul.text) > 0:
            #print(ul.text)
            return ul

def make_selection(input_locus, value):
    input_locus.click()
    try:
        ul = locate_ul()
        #span = WebDriverWait(driver, 5).until(
        #    EC.presence_of_element_located(
        #    (By.XPATH, ul.find_element_by_xpath(f'./li/span[contains(text(),"{value}")]').get_attribute('innerHTML'))))
        ul.find_element_by_xpath(f'./li/span[contains(text(),"{value}")]').click()
        #span.click()
    except:
        input_locus.clear()
        input_locus.send_keys(value)
        
def add_gate():
    input_loci = driver.find_elements_by_class_name('el-input__inner')
    for input_locus in input_loci:
        label = input_locus.find_element_by_xpath('./../../../..')
        if label.text == '终点校门':
            print('添加终点校门...')
            input_locus.click()
            ul = locate_ul()
            ul.find_element_by_xpath(f'.//li/span[contains(text(),"西门")]').click()
            time.sleep(0.1)


def select_input():
    input_loci = driver.find_elements_by_class_name('el-input__inner')
    select_dict = {'出入校起点':'畅春园','出入校终点':'燕园','出入校事由':'科研','园区':'畅春园','邮箱':'xinyu.yang@pku.edu.com','手机号':'13120129722','宿舍楼':'畅春园63楼','宿舍房间号':'527'}
    for input_locus in input_loci:
        label = input_locus.find_element_by_xpath('./../../../..')
        for query, value in select_dict.items():    
            if label.text == query:
                print('添加{0}...'.format(query))
                make_selection(input_locus, value)
                time.sleep(0.1)
    #初始界面中没有“终点校门”选项，且xpath结构不同于初始选项
    add_gate()


def make_filling(input_locus, value):
    input_locus.click()
    input_locus.send_keys(value)
    
def fill_input():
    input_loci = driver.find_elements_by_class_name('el-textarea__inner')
    fill_dict =  {'出入校具体事项':'科研','基本轨迹':'畅春园-吕志和楼-畅春园'}
    for input_locus in input_loci:
        label = input_locus.find_element_by_xpath('./../../..')
        for query, value in fill_dict.items():
            if label.text.split()[0] == query:
                print('添加{0}...'.format(query))
                make_filling(input_locus, value)
                time.sleep(0.1)


def finish():
    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'el-checkbox__inner'))).click()
    save = driver.find_element_by_xpath('//button/span[contains(text(),"保存")]').click()
    time.sleep(2)
    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, '//button/span[contains(text(),"提交")]'))).click()

def run(userName, password):
    login(userName, password)
    go_to_application()
    loci = select_input()
    fill_input()
    finish()

if __name__ == '__main__':
    global driver
    base = os.path.dirname(os.path.realpath(__file__))
    conf = ConfigParser()
    conf.read(os.path.join(base,'config.ini'), encoding='utf8')

    userName, password = dict(conf['login']).values()
    start = dict(conf['start']).values()
    end = 0
    dorm = 0
    reason = 0
    print(start)
    driver = webdriver.Chrome(executable_path=r'F:\Python_64bit\chromedriver.exe')
    loci = run(userName, password)

    print('Driver Launching...')
    #driver_chrome.quit()

