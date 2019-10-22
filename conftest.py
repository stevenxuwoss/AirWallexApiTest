# encoding : utf-8
# @Author  : Steven Xu
# @Email   ：youzi5201@163.com

import pytest
import datetime
import os
from py._xmlgen import html
from selenium import webdriver

def pytest_configure(config):
    if config.getoption('--html'):
        path_list = list(os.path.split(config.option.htmlpath))
        #path_list.insert(-1, datetime.datetime.now().strftime('%Y%m%d-%H%M%S')) # create folder with time
        path_list.insert(-1, datetime.datetime.now().strftime('%Y%m%d')) # one day one report
        config.option.htmlpath = os.path.join(*tuple(path_list))
    
@pytest.mark.optionalhook
def pytest_html_results_summary(prefix, summary, postfix):
    prefix.extend([html.p("Tester: Steven Xu")])
    prefix.extend([html.p("Email: youzi5201@163.com")])
    prefix.extend([html.p("Host Url: http://preview.airwallex.com:30001")])


# =============================UIAutomation==============================
driver = None

@pytest.mark.hookwrapper
def pytest_runtest_makereport(item):
    """
    当测试失败的时候，自动截图，展示到html报告中
    :param item:
    """
    pytest_html = item.config.pluginmanager.getplugin('html')
    outcome = yield
    report = outcome.get_result()
    extra = getattr(report, 'extra', [])

    if report.when == 'call' or report.when == "setup":
        xfail = hasattr(report, 'wasxfail')
        if (report.skipped and xfail) or (report.failed and not xfail):
            file_name = report.nodeid.replace("::", "_")+".png"
            screen_img = _capture_screenshot()
            if file_name:
                html = '<div><img src="data:image/png;base64,%s" alt="screenshot" style="width:600px;height:300px;" ' \
                       'οnclick="window.open(this.src)" align="right"/></div>' % screen_img
                extra.append(pytest_html.extras.html(html))
        report.extra = extra

def _capture_screenshot():
    '''
    screenshot save as base64
    :return:
    '''
    return driver.get_screenshot_as_base64()

@pytest.fixture(scope='session', autouse=True)
def browser():
    global driver
    if driver is None:
        driver =webdriver.Chrome(executable_path="externals\chromedriver")
    return driver
