from contextlib import closing
from selenium.webdriver import Chrome # pip install selenium
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

from keys import mindbody

import logging
logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s')
# log = logging.getLogger()
log = logging.getLogger('MBImport')
# log.setLevel(logging.DEBUG)
log.setLevel(logging.INFO)
logging.getLogger('selenium.webdriver.remote.remote_connection').setLevel(logging.INFO)


class MBClientTypes:
    def __init__(self, site_id, client_types=None):
        self.client_types = client_types
        self.site_id = site_id

        self.main_url = 'https://clients.mindbodyonline.com/classic/home?studioid={}'.format(site_id)
        self.client_url = 'https://clients.mindbodyonline.com/asp/adm/adm_clt_profile.asp?id='

    def update_client_types(self, client_id, selected_types):
        with closing(Chrome()) as browser:
            # Load initial page
            log.debug('loading app!')
            browser.get(self.main_url)
            WebDriverWait(browser, timeout=10).until(EC.presence_of_element_located((By.NAME, 'mainFrame')))
            log.debug('main loaded!')

            browser.switch_to.frame('mainFrame')
            WebDriverWait(browser, timeout=10).until(EC.presence_of_element_located((By.ID, 'requiredtxtUserName')))
            log.debug('frame loaded!')

            # login to app
            browser.find_element_by_id('requiredtxtUserName').send_keys(mindbody[self.site_id]["USER_NAME"])
            browser.find_element_by_id('requiredtxtPassword').send_keys(mindbody[self.site_id]["USER_PASSWORD"])
            browser.find_element_by_id('btnLogin').click()
            WebDriverWait(browser, timeout=10).until(EC.presence_of_element_located((By.NAME, 'mainFrame')))
            browser.switch_to.frame('mainFrame')
            WebDriverWait(browser, timeout=10).until(EC.presence_of_element_located((By.ID, 'manager-tools')))
            log.debug('logged in!')

            # Go to client record
            browser.get(self.client_url + client_id)
            WebDriverWait(browser, timeout=10).until(EC.presence_of_element_located((By.ID, 'clienttypes')))
            log.debug('client loaded!')

            # Go to Client Types
            browser.execute_script('setupCltTypes()')
            WebDriverWait(browser, timeout=10).until(EC.presence_of_element_located((By.NAME, 'updateType')))
            log.debug('client types loaded!')

            # Check off types
            for client_type in selected_types:
                try:
                    elem = browser.find_element_by_xpath(".//*[contains(text(), '" + client_type + "')]")
                    if not browser.find_element_by_name(elem.get_attribute('for')).is_selected():
                        elem.click()
                except NoSuchElementException:
                    log.warn("Unable to locate Client Type '{}'".format(client_type))

            browser.find_element_by_name('updateType').click()
            WebDriverWait(browser, timeout=10).until(EC.presence_of_element_located((By.ID, 'clienttypes')))
            log.debug('client types saved!')

            browser.execute_script('logOut()')
            log.debug('logged out!')

    def clear_client_types(self, client_id):
        with closing(Chrome()) as browser:
            # Load initial page
            log.debug('loading app!')
            browser.get(self.main_url)
            WebDriverWait(browser, timeout=10).until(EC.presence_of_element_located((By.NAME, 'mainFrame')))
            log.debug('main loaded!')

            browser.switch_to.frame('mainFrame')
            WebDriverWait(browser, timeout=10).until(EC.presence_of_element_located((By.ID, 'requiredtxtUserName')))
            log.debug('frame loaded!')

            # login to app
            browser.find_element_by_id('requiredtxtUserName').send_keys('Siteowner')
            browser.find_element_by_id('requiredtxtPassword').send_keys('apitest1234')
            browser.find_element_by_id('btnLogin').click()
            WebDriverWait(browser, timeout=10).until(EC.presence_of_element_located((By.NAME, 'mainFrame')))
            browser.switch_to.frame('mainFrame')
            WebDriverWait(browser, timeout=10).until(EC.presence_of_element_located((By.ID, 'manager-tools')))
            log.debug('logged in!')

            # Go to client record
            browser.get(self.client_url + client_id)
            WebDriverWait(browser, timeout=10).until(EC.presence_of_element_located((By.ID, 'clienttypes')))
            log.debug('client loaded!')

            # Go to Client Types
            browser.execute_script('setupCltTypes()')
            WebDriverWait(browser, timeout=10).until(EC.presence_of_element_located((By.NAME, 'updateType')))
            log.debug('client types loaded!')

            # Uncheck types
            for client_type in self.client_types:
                elem = browser.find_element_by_xpath(".//*[contains(text(), '" + client_type + "')]")
                if browser.find_element_by_name(elem.get_attribute('for')).is_selected():
                    elem.click()
            browser.find_element_by_name('updateType').click()
            WebDriverWait(browser, timeout=10).until(EC.presence_of_element_located((By.ID, 'clienttypes')))
            log.debug('client types saved!')

            browser.execute_script('logOut()')
            log.debug('logged out!')


if __name__ == "__main__":
    all_client_types = ['Bootcamp Only',
                    'CrossFit',
                    'Kennewick High School',
                    'Pool Only',
                    'Professional Athlete',
                    'Southridge High School',
                    'Student']

    ct = MBClientTypes('-99', all_client_types)
    ct.clear_client_types('100014533')
    client_types = ['Bootcamp Only','Pool Only', 'Student']
    ct.update_client_types('100014533', client_types)
