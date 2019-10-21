# encoding : utf-8
# @Author  : Steven Xu
# @Email   ：youzi5201@163.com
# @Description : test pytest PlugIns feature

import pytest
import time
import logging

log = logging.getLogger(__name__)

class TestDemo():

    @pytest.mark.skip(reason="this is skip test.")
    def test_skip_demo(self):
        pass

    @pytest.mark.skipif(1==1, reason="this is skipif test.")
    def test_skipif_demo(self):
        pass

    def test_assert_demo(self):
        assert 1==2

    # need plugins: pytest-rerunfailures
    # pip install pytest-rerunfailures
    @pytest.mark.flaky(reruns=5, reruns_delay=2)
    def test_reruns_demo(self):
        import random
        assert random.choice([True, False])
    # need plugins: pytest-timeout
    # pip install pytest-timeout
    #@pytest.mark.flaky(reruns=5, reruns_delay=2)
    # @pytest.mark.timeout(10)
    # def test_timeout_demo(self):
        
    #     import random

    #     time.sleep(15)
    #     assert random.choice([True, False])

    def test_assume_demo(self):
        log.info("test step1：test 》")
        pytest.assume(1>3,"should a > b")
        log.info("test step2: if run next assert")
        pytest.assume(2==2,"should =")

        pytest.assume(3==2,"should =")


if __name__ == "__main__":
    pytest.main(['test_demo1.py --html=report.html'])
