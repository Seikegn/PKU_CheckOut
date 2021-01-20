#学校网站细节已删去，仅留框架
# -*- coding: utf-8
#Author: Seikegn Yang
#Contact: seikegn_yang@163.com
#Github: https://github.com/Seikegn
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from urllib.parse import quote
import time
import datetime
import sys
import os


def login(userName, password, retry=0):
    if retry == 3:
        raise Exception('门户登录失败')

    appID = ''
    iaaaUrl = ''
    appName = quote('')
    redirectUrl = ''
    driver.get('')
    driver.get(
        f'{iaaaUrl}?appID={appID}&appName={appName}&redirectUrl={redirectUrl}')
    WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.ID, '')))
    driver.find_element_by_id('').send_keys(userName)
    time.sleep(0.1)
    driver.find_element_by_id('').send_keys(password)
    time.sleep(0.1)
    driver.find_element_by_id('').click()
    try:
        WebDriverWait(driver,
                      5).until(EC.visibility_of_element_located((By.ID, '')))
    except:
        print('Retrying...')
        login(userName, password, retry + 1)

def go_to_simso():
    driver.find_element_by_id('').click()
    WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.ID, '')))
    driver.find_element_by_id('').click()
    time.sleep(1)
    driver.switch_to.window(driver.window_handles[-1])
    WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.CLASS_NAME, '')))

def go_to_submission():
    driver.find_element_by_xpath('').click()
    WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.CLASS_NAME, '')))

def check_pop():
    try:
        pop = WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.XPATH, '')))
        close = pop.find_element_by_xpath('')
        close.click()
        time.sleep(1)
    except:
        pass

def locate_ul():
    all_uls = driver.find_elements_by_xpath('')
    time.sleep(1)
    for ul in all_uls:
        if len(ul.text) > 0:
            return ul

def make_selection(input_locus, value):
    input_locus.click()
    try:
        ul = locate_ul()
        ul.find_element_by_xpath(f'"{value}"').click()
    except:
        input_locus.clear()
        input_locus.send_keys(value)
        
def add_gate():
    input_loci = driver.find_elements_by_class_name('')
    for input_locus in input_loci:
        label = input_locus.find_element_by_xpath('./../../../..')
        if label.text == '终点校门':
            print('添加终点校门...')
            input_locus.click()
            ul = locate_ul()
            ul.find_element_by_xpath(f'''''').click()
            time.sleep(0.1)

def select_input():
    input_loci = driver.find_elements_by_class_name('')
    select_dict = {}
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
    fill_dict =  {}
    for input_locus in input_loci:
        label = input_locus.find_element_by_xpath('./../../..')
        for query, value in fill_dict.items():
            if label.text.split()[0] == query:
                print('添加{0}...'.format(query))
                make_filling(input_locus, value)
                time.sleep(0.1)

def finish():
    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CLASS_NAME, ''))).click()
    save = driver.find_element_by_xpath('').click()
    time.sleep(2)
    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, '')))
    driver.find_element_by_xpath('').click()
    time.sleep(1)

def submit():
    login(Info_Dict['账号'], Info_Dict['密码'])
    check_pop()
    go_to_simso()
    go_to_submission()
    loci = select_input()
    fill_input()
    finish()
    print('已保存并提交')

def go_to_check():
    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, '')))
    driver.find_element_by_xpath('').click()
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, '')))

def check_today():
    today = datetime.date.today()
    tomorrow = today + datetime.timedelta(days=1)
    tomorrow = tomorrow.strftime("%Y%m%d")
    try:
        date = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, f'"{tomorrow}"')))  
        submission = date.find_element_by_xpath('')
        print('正在检查{0}的申请状态'.format(tomorrow))
        print('提交状态: {0}'.format(submission.text.strip()))
        qualification = date.find_element_by_xpath('')
        print('审核状态: {0}'.format(qualification.text.strip()))
        return qualification.text.strip()
    except:
        print('{0}未成功提交，请检查!'.format(tomorrow))
        return False

def check():
    login(Info_Dict['账号'], Info_Dict['密码'])
    go_to_simso()
    go_to_check()
    state = check_today()
    return state

if __name__ == '__main__':
    global driver, Info_Dict
    print('''
    欢迎使用这个临时搭建的自动备案软件，本软件用于应对20210107以来出校政策，提供的功能包括：1.一键报备，2.审核状态检查，3.自动报备并跟踪审核结果。
    请将chromedriver.exe、MyInfo.txt两个文件与QuickCheck.exe放在同一目录下。了解技术细节的同学可以自行选用其它（无头）浏览器驱动。
    建议将本软件或脚本设置为开机自动运行（具体方法请根据自己的系统查询），以免忘记操作。
    首次运行前，请编辑MyInfo.txt并按示例格式填写你的个人账号及报备信息，其中“自动报备并跟踪审核结果”请填“是”或“否”，若为“是”，则软件启动后将自动进行报备并跟踪审核结果，
    每30min查询一次，直至审核状态为“通过”时自动结束进程。注意txt文件中冒号用英文输入。
    本软件目前只支持64位系统，脚本没有限制。
    ''')
    base = os.path.dirname(os.path.realpath(__file__))
    try:
        f = open(os.path.join(base,'MyInfo.txt'), mode='r', encoding='utf8')
        Info = f.readlines()
        Info_Dict = dict(map(lambda x:(x.strip().split(':')[0].strip(),x.strip().split(':')[1].strip()),Info))
        Auto = Info_Dict['自动报备并跟踪审核结果']
        if Auto == '是':
            auto = 1
        elif Auto == '否':
            auto = 0
        else:
            raise ValueError('“自动报备并跟踪审核结果”属性只能为“是”或“否”，请在MyInfo.txt中修改')
    except:
        print('MyInfo.txt填写有误，请检查')

    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(os.path.join(base,'chromedriver.exe'),chrome_options=chrome_options)
    if auto == 1:
        print('\n正在自动报备')
        try:
            submit()
        except:
            print('今日已进行过报备或自动报备失败，若后续显示的“提交状态”为“未提交”，请到门户检查')
        time.sleep(2)
        print('正在跟踪审核结果')
        
        while True:
            this_moment = time.strftime('%H:%M:%S')
            state = check()
            if state == '审核通过':
                print('{0}-已确认审核通过'.format(this_moment))
                driver.quit()
                break
            print('{0}-审核未通过'.format(this_moment))
            print('接下来每隔三十分钟检查一次审核状态')
            time.sleep(1800)
            '''try:
                print('{0}-仍在登录状态直接进行检查'.format(this_moment))
                state = check_today()
            except:
                print('{0}-已断开，重新登录进行检查'.format(this_moment))
                state = check()'''
            
    else:
        while True:
            choice = input('\n请输入对应的数字来选择你的操作：\n1.一键报备\n2.审核状态检查\n3.查看个人信息\n4.关闭应用\n\n')
            if choice == '1':
                try:
                    submit()
                except:
                    print('今日已进行过报备或自动报备失败，请到门户检查')
            elif choice == '2':
                check()
            elif choice == '3':
                print(Info_Dict)
            elif choice == '4':
                driver.quit()
                break
            time.sleep(1)
