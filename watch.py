#watch.py
import random
import time
from lxml import etree
from prettytable import PrettyTable
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By


def out(text):  # 格式输出
    print(time.strftime(f"[%Y-%m-%d %H:%M:%S]:{text}", time.localtime()))


def Watch(userName, password, classId):
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    # 屏蔽以开发者运行提示框
    options.add_experimental_option('useAutomationExtension', False)
    # 屏蔽保存密码提示框
    prefs = {'credentials_enable_service': False, 'profile.password_manager_enabled': False}
    options.add_experimental_option('prefs', prefs)
    # chrome 88 或更高版本的反爬虫特征处理
    options.add_argument('--disable-blink-features=AutomationControlled')
    # 浏览器对象
    preferences = {
        "webrtc.ip_handling_policy": "disable_non_proxied_udp",
        "webrtc.multiple_routes_enabled": False,
        "webrtc.nonproxied_udp_enabled": False
    }
    # 关闭webrtc 避免找到真实IP地址
    options.add_experimental_option("prefs", preferences)
    options.binary_location = r'Chrome\App\Chrome.exe'
    driver = webdriver.Chrome(service=Service(r'chromedriver.exe'), options=options)
    with open('stealth.min.js', mode='r', encoding='utf-8') as f:
        string = f.read()
    # 移除 selenium 中的爬虫特征
    driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {'source': string})
    driver.get('https://sso.icve.com.cn/sso/auth?mode=simple&source=2&redirect=https://user.icve.com.cn/cms/')
    time.sleep(1)
    driver.find_element(By.ID, 'userName').send_keys(userName)
    time.sleep(1)
    driver.find_element(By.ID, 'password11').send_keys(password)
    time.sleep(1)
    driver.find_element(By.ID, 'isTy').click()
    time.sleep(1)
    driver.find_element(By.CLASS_NAME, 'dl').click()
    time.sleep(1)
    try:
        driver.find_element(By.ID, 'close1').click()
        time.sleep(1)
        driver.find_element(By.ID, 'close2').click()
        time.sleep(1)
        driver.find_element(By.ID, 'close3').click()
        time.sleep(1)
        driver.find_element(By.ID, 'close4').click()
    except:
        out("预防性点击可能出现的提示框")
    time.sleep(4)
    if "* 校验登录状态" in driver.page_source:
        time.sleep(3)
        driver.find_element(By.ID, 'userCenterUrl').click()
        out("登录成功")
        driver.get(
            f"https://course.icve.com.cn/learnspace/sign/signLearn.action?template=blue&courseId={classId}&loginType=true&loginId={userName}&sign=0&siteCode=zhzj&domain=user.icve.com.cn")
        time.sleep(2)
        driver.switch_to.frame('mainContent')
        time.sleep(2)
        videotasker = etree.HTML(driver.page_source).xpath('//*[@completestate="0" and @itemtype="video"]/@onclick')
        doctasker = etree.HTML(driver.page_source).xpath('//*[@completestate="0" and @itemtype="doc"]/@onclick')
        vodall = len(etree.HTML(driver.page_source).xpath('//*[@itemtype="video"]/@onclick'))
        docall = len(etree.HTML(driver.page_source).xpath('//*[@itemtype="doc"]/@onclick'))

        table = PrettyTable(["视频已完成/全部", "文档已完成/全部", "总进度"])
        table.add_row([f"{vodall - len(videotasker)}/{vodall}", f"{docall - len(doctasker)}/{docall}",
                       '{:.2%}'.format((len(videotasker) + len(doctasker)) / (vodall + docall))])
        print(table)

        out("开始执行视频任务序列")
        for i in videotasker:
            time.sleep(2)
            driver.execute_script(i)
            while True:
                if 'id="mainFrame" name="mainFrame"' in driver.page_source:  # 利用死循环进入播放器框架 吐槽一下职教云辣鸡代码
                    driver.switch_to.frame('mainFrame')
                    break
            while True:
                time.sleep(random.randint(3, 7))
                look = driver.execute_script(
                    'return document.getElementById("screen_player_time_1").textContent')
                print(f'观看:{driver.execute_script("return document.title")} 已观看到{look}')
                time.sleep(10)  # 十秒输出
                if look == driver.execute_script(
                        'return document.getElementById("screen_player_time_2").textContent'):
                    out("观看完成,即将下一个")
                    driver.switch_to.parent_frame()
                    break
        out("开始执行文档任务序列")
        for i in doctasker:
            time.sleep(2)
            driver.execute_script(i)
            print(f'观看:{driver.execute_script("return document.title")}')
            time.sleep(7)
            out("观看完成,即将下一个")
        videotasker = etree.HTML(driver.page_source).xpath('//*[@completestate="0" and @itemtype="video"]/@onclick')
        doctasker = etree.HTML(driver.page_source).xpath('//*[@completestate="0" and @itemtype="doc"]/@onclick')
        vodall = len(etree.HTML(driver.page_source).xpath('//*[@itemtype="video"]/@onclick'))
        docall = len(etree.HTML(driver.page_source).xpath('//*[@itemtype="doc"]/@onclick'))

        if (len(videotasker) + len(doctasker)) == (vodall + docall):
            out("恭喜 本课全部观看完成 程序退出！")
            exit()
