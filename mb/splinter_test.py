import splinter
from time import sleep

url = 'https://clients.mindbodyonline.com/classic/home?studioid=-99'
browser = splinter.Browser('chrome')
# browser = splinter.Browser('phantomjs')
# browser.driver.set_window_size(1120, 550)
browser.visit(url)
sleep(3)
with browser.get_iframe('mainFrame') as iframe:
    iframe.find_by_name('requiredtxtUserName').first.fill(value='Siteowner')
    iframe.find_by_name('requiredtxtPassword').first.fill(value='apitest1234')
    iframe.find_by_id('btnLogin').first.click()

sleep(3)
browser.visit('https://clients.mindbodyonline.com/asp/adm/adm_clt_profile.asp?id=100014533')
# while browser.is_element_not_present_by_id('clienttypes',1):
#     pass
sleep(3)

browser.execute_script('setupCltTypes()')
# while browser.is_element_not_present_by_text('Pool Only',1):
#     pass
sleep(3)

browser.find_by_text('Pool Only').first.check()  #repeat for any boxes that need to be checked
browser.find_by_name('updateType').first.click()
browser.execute_script('logOut()')
browser.quit()


