# encoding : utf-8
# @Author  : Steven Xu
# @Email   ：youzi5201@163.com

import pytest
import datetime
import os
from py._xmlgen import html

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
