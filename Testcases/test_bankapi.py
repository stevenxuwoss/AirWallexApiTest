# encoding : utf-8
# @Author  : Steven Xu
# @Email   ：youzi5201@163.com

import pytest
import requests
import yaml
import random
import json
from Utils.randomUtils import RandomUtils
import logging

log = logging.getLogger(__name__)

# common area
url = 'http://preview.airwallex.com:30001/bank'

headers = {
    "Content-Type": "application/json"
}


'''
sample payload
    {
    "payment_method": "SWIFT",
    "bank_country_code": "US",
    "account_name": "John Smith",
    "account_number": "123",
    "swift_code": "ICBCUSBJ",
    "aba": "11122233A"
    }
sample 200 response:
    {
    "success": "Bank details saved"
    }
'''
def genAccountNumber(country = 'US'):
    if country == 'US':
        return RandomUtils.genRandomDigits(random.randint(1,17))
    if country == 'AU':
        return RandomUtils.genRandomDigits(random.randint(6,9))
    if country == 'CN':
        return RandomUtils.genRandomDigits(random.randint(8,20))


def getBankTestInfo(path):
    with open('Testdata/bankapiTestdata.yml','r') as f:
        return yaml.load(f, Loader=yaml.FullLoader)

class TestBankApi():

    def test_bankPaymentSWIFT(self):
        log.info('start test bank api payment with SWIFT')
        log.info('scenario 1: valid test data.')

        payload = {
            "payment_method": "SWIFT",
            "bank_country_code": "US",
            "account_name": "John Smith",
            "account_number": "123",
            "swift_code": "ICBCUSBJ",
            "aba": "11122233A"
        }

        data = json.dumps(payload).encode("utf-8")

        res = requests.post(url=url, data=data, headers=headers)

        assert res.status_code == 200, "Expected is 200, but actual status code {}".format(res.status_code)
        assert res.json().get('success') == 'Bank details saved', "Expected is 200, but actual status code {}".format(res.json().get('success'))

        log.info('scenario 2: no bank country code.')
        payload = {
            "payment_method": "SWIFT",
            "bank_country_code": "",
            "account_name": "John Smith",
            "account_number": "123",
            "swift_code": "ICBCUSBJ",
            "aba": "11122233A"
        }

        data = json.dumps(payload).encode("utf-8")

        res = requests.post(url=url, data=data, headers=headers)

        assert res.status_code == 400, "Expected is 400, but actual status code {}".format(res.status_code)
        assert res.json().get('error') == "'bank_country_code' is required, and should be one of 'US', 'AU', or 'CN'", "Expected error message is match, but actual error message is: {}".format(res.json().get('error'))

        log.info('End verify payment with SWIFT')

if __name__ == "__main__":
    pytest.main(['-q','test_bankapi.py','--html=report.html'])






