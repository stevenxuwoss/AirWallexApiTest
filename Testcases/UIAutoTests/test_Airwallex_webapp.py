from selenium import webdriver
import time
import logging
import pytest
from Utils.webTable import WebTable
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

log = logging.getLogger(__name__)



def get_paymentDetail_by_item(browser,item):

    return browser.find_element_by_xpath("//dd[@data-test='%s']" %item).text

@pytest.fixture(scope="function")
def login(browser):
    email = "testing+ad@airwallex.com"
    password = "Abcde1234"

    log.info("scenario: open url https://staging.airwallex.com/.")

    browser.maximize_window()
    browser.get("https://staging.airwallex.com/")
    time.sleep(2)
    
    browser.find_element_by_link_text('Log in').click()

    time.sleep(2)

    log.info("scenario: begin login with email and password.")
    browser.find_element_by_id("email").send_keys(email)
    browser.find_element_by_id("password").send_keys(password)

    # <div class="css-x5bpve e172sq123">Log in</div>
    time.sleep(1)
    browser.find_element_by_xpath("//div[@class='css-x5bpve e172sq123' and text()='Log in']").click()
    time.sleep(5)
    log.info("scenario: end login with email and password.")

    yield 

    browser.quit()
    log.info("testcase end.")

class TestAirwallexWebapp():

    def test_payment(self,login,browser):
        # TODO: should add wait to delay not hard code.
        log.info("click left payment")
        wait = WebDriverWait(browser,10)
        #wait.until(EC.title_contains(""))
        #<a href="payments/new" title="Payments" data-test="primary_nav_payments" class="css-f7t2f1 e13v5c8a1"><div class="css-1sjf1hh e13v5c8a4"><svg width="16" height="16" viewBox="0 0 32 24" xmlns:xlink="http://www.w3.org/1999/xlink"><defs><path d="M24 8H8a4 4 0 0 1-4 4v8a4 4 0 0 1 4 4h16a4 4 0 0 1 4-4v-8a4 4 0 0 1-4-4zM2 4h28a2 2 0 0 1 2 2v20a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2zm14 18a6 6 0 1 1 0-12 6 6 0 0 1 0 12zm0-4a2 2 0 1 0 0-4 2 2 0 0 0 0 4z" id="8c27caa5-0095-44b4-a20f-a3161fd888b7"></path></defs><g transform="translate(0 -4)" fill="none" fill-rule="evenodd"><mask id="c37632c9-6da8-413f-a8f1-af2cf873d4b1" fill="#fff"><use xlink:href="#8c27caa5-0095-44b4-a20f-a3161fd888b7"></use></mask><g mask="url(#c37632c9-6da8-413f-a8f1-af2cf873d4b1)" fill="#fff"><path d="M32 0H0v32h32z"></path></g></g></svg></div></a>
        browser.find_element_by_xpath("//a[@href='payments/new']").click()
        log.info("switch to Payment activity")
        #<a href="/payments/activity/payments" data-test="payment_activity_tab" class="css-1uboekr e1b1b2023">Payment activity</a>
        browser.find_element_by_xpath("//a[@href='/payments/activity/payments']").click()
        log.info("click filter button")
        browser.find_element_by_xpath('//div[contains(text(), "Filters")]').click()
        time.sleep(1)
        #<input class="text-input" placeholder="Payment ID" name="paymentId" value="">
        log.info("filter with payment id ac919405-12a1-4dd5-ba21-fcdaf4dbb7f0")
        paymentId = "ac919405-12a1-4dd5-ba21-fcdaf4dbb7f0"
        browser.find_element_by_xpath("//input[@name='paymentId']").send_keys(paymentId)

        #<div class="css-x5bpve e172sq123">Apply filters</div>
        log.info("Apply filters")
        browser.find_element_by_xpath('//div[contains(text(), "Apply filters")]').click()
        # be careful: need to wait the result showing.
        time.sleep(2)
        # <table style="width: 100%;">
        table = WebTable(browser.find_element_by_xpath("//table[@style='width: 100%;']"))
        # First row data : ['', 'P190315-HT8799K', '2019-03-19', 'EUR', '€1,000.00', 'frank azs', 'Dispatched'] 
        #firstRowData = table.row_data(1)
        log.info("choice the SHORT REFERENCE")
        table.select_row(1,2)
        time.sleep(2)

        log.info("verify the details of payment id ac919405-12a1-4dd5-ba21-fcdaf4dbb7f0")

        expectedPaymentDetail = {
            "type": "PAYMENT",
            "accountId": "d439bbd5-5793-46a6-8143-c86a52b964bf",
            "paymentId": "ac919405-12a1-4dd5-ba21-fcdaf4dbb7f0",
            "requestId": "75a17e70-4704-11e9-864c-f777f9b06faf",
            "status": "Dispatched"
        }

        acturlPaymentDetail = {
            "type": get_paymentDetail_by_item(browser,'type_value'),
            "accountId": get_paymentDetail_by_item(browser,'account_id_value'),
            "paymentId": get_paymentDetail_by_item(browser,'payment_id_value'),
            "requestId": get_paymentDetail_by_item(browser,'request_id_value'),
            "status": get_paymentDetail_by_item(browser,'status_value')
        }

        assert acturlPaymentDetail==expectedPaymentDetail




        # log.info("No of rows : " + str(table.get_row_count()))
        # log.info("------------------------------------")
        # log.info("No of cols : " + str(table.get_column_count()))
        # log.info("------------------------------------")
        # log.info("Table size : " + str(table.get_table_size()))
        # log.info("------------------------------------")
        # log.info("First row data : "+ str(table.row_data(1)))
        # log.info("------------------------------------")
        # <div>No matches</div>









# # <div data-test="alert_hook" class="css-zi5vxs eu9qs7o3"><div class="css-1ttmxwr eu9qs7o4"><div class="css-1ttmxwr eu9qs7o5"><div class="css-1g8kwo4 etoevn70"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 32 32"><path fill="#FF4F42" fill-rule="evenodd" d="M16,0 C24.836556,0 32,7.163444 32,16 C32,24.836556 24.836556,32 16,32 C7.163444,32 -3.55271368e-15,24.836556 0,16 C0,7.163444 7.163444,0 16,0 Z M16,4 C9.372583,4 4,9.372583 4,16 C4,22.627417 9.372583,28 16,28 C22.627417,28 28,22.627417 28,16 C28,9.372583 22.627417,4 16,4 Z M16,18 C14.8954305,18 14,17.1045695 14,16 L14,10 C14,8.8954305 14.8954305,8 16,8 C17.1045695,8 18,8.8954305 18,10 L18,16 C18,17.1045695 17.1045695,18 16,18 Z M16,24 C14.8954305,24 14,23.1045695 14,22 C14,20.8954305 14.8954305,20 16,20 C17.1045695,20 18,20.8954305 18,22 C18,23.1045695 17.1045695,24 16,24 Z"></path></svg></div></div>Please check your credentials and try again.</div></div>
# alert_hook = driver.find_element_by_xpath("//div[@data-test='alert_hook']")
# print(alert_hook)



# # <a href="dashboard" title="Dashboard" data-test="primary_nav_dashboard" class="css-f7t2f1 e13v5c8a1"><div class="css-1sjf1hh e13v5c8a4"><svg width="16" height="16" viewBox="0 0 32 32" xmlns:xlink="http://www.w3.org/1999/xlink"><defs><path d="M15.09 19.025l2.976-7.012a2 2 0 1 1 3.682 1.563l-2.447 5.765c2.52.529 4.822 1.65 6.753 3.212A11.944 11.944 0 0 0 28 15.915l-.82.144a2 2 0 0 1-.694-3.939l.822-.145a11.987 11.987 0 0 0-2.17-3.754l-.535.638a2 2 0 0 1-3.064-2.571l.536-.639A11.921 11.921 0 0 0 18 4.166V5a2 2 0 1 1-4 0v-.834c-1.465.246-2.84.757-4.075 1.483l.536.639a2 2 0 0 1-3.064 2.571l-.535-.638a11.987 11.987 0 0 0-2.17 3.754l.822.145a2 2 0 0 1-.694 3.94L4 15.914V16c0 2.418.715 4.67 1.946 6.553a15.926 15.926 0 0 1 9.144-3.528zM16 32C7.163 32 0 24.837 0 16S7.163 0 16 0s16 7.163 16 16-7.163 16-16 16zm0-4c2.713 0 5.272-.904 7.335-2.5A11.958 11.958 0 0 0 16 23c-2.713 0-5.272.904-7.335 2.5A11.958 11.958 0 0 0 16 28z" id="1e5e14f2-2b96-4bc4-ae3a-a1ac8330bdfe"></path></defs><g fill="none" fill-rule="evenodd"><mask id="2901c0a5-b42d-4518-8209-e7a199908c47" fill="#fff"><use xlink:href="#1e5e14f2-2b96-4bc4-ae3a-a1ac8330bdfe"></use></mask><g mask="url(#2901c0a5-b42d-4518-8209-e7a199908c47)" fill="#fff"><path d="M32 0H0v32h32z"></path></g></g></svg></div></a>
# find_dashboard = driver.find_element_by_link_text('dashboard')
# assert find_dashboard
# #<div class="css-x5bpve e172sq123">testing+ad@airwallex.com</div>