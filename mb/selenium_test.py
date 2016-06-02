from contextlib import closing
from selenium.webdriver import Chrome # pip install selenium
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import logging
logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s')
log = logging.getLogger()
log.setLevel(logging.DEBUG)
logging.getLogger('selenium.webdriver.remote.remote_connection').setLevel(logging.INFO)

url = 'https://clients.mindbodyonline.com/classic/home?studioid=-99'
with closing(Chrome()) as browser:
    log.debug('loading app!')
    browser.get(url)
    #Wait for initial page load
    WebDriverWait(browser, timeout=10).until(EC.presence_of_element_located((By.NAME,'mainFrame')))
    log.debug('main loaded!')

    browser.switch_to.frame('mainFrame')
    WebDriverWait(browser, timeout=10).until(EC.presence_of_element_located((By.ID,'requiredtxtUserName')))
    log.debug('frame loaded!')

    # login to app
    browser.find_element_by_id('requiredtxtUserName').send_keys('Siteowner')
    browser.find_element_by_id('requiredtxtPassword').send_keys('apitest1234')
    browser.find_element_by_id('btnLogin').click()
    WebDriverWait(browser, timeout=10).until(EC.presence_of_element_located((By.NAME,'mainFrame')))
    browser.switch_to.frame('mainFrame')
    WebDriverWait(browser, timeout=10).until(EC.presence_of_element_located((By.ID,'manager-tools')))
    log.debug('logged in!')

    #Go to client record
    browser.get('https://clients.mindbodyonline.com/asp/adm/adm_clt_profile.asp?id=100014533')
    WebDriverWait(browser, timeout=10).until(EC.presence_of_element_located((By.ID,'clienttypes')))
    log.debug('client loaded!')

    #Go to Client Types
    browser.execute_script('setupCltTypes()')
    WebDriverWait(browser, timeout=10).until(EC.presence_of_element_located((By.NAME,'updateType')))
    log.debug('client types loaded!')

    #Check off types
    elem = browser.find_element_by_xpath(".//*[contains(text(), 'Pool Only')]")
    if not browser.find_element_by_name(elem.get_attribute('for')).is_selected():
        elem.click()
    browser.find_element_by_name('updateType').click()
    WebDriverWait(browser, timeout=10).until(EC.presence_of_element_located((By.ID,'clienttypes')))
    log.debug('client types saved!')

    browser.execute_script('logOut()')
    log.debug('logged out!')