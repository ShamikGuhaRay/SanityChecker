from selenium import webdriver
from getpass import getpass
from selenium.webdriver.common.keys import Keys
import string
import re
import time
from time import sleep
import pandas as pd
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
import requests
import logging
from datetime import datetime


logging.basicConfig(filename='C:\\OCI_Scripts\\tenant_id_check_run.log', level=logging.INFO,
                    format='%(levelname)s:%(message)s')
start = datetime.now()
current_time = start.strftime("%H:%M:%S")
print("Starting AT ", current_time)
logging.info('Starting AT  {}'.format(current_time))

#Load urls from CSV File
try:
 df = pd.read_csv('C:\\OCI_Scripts\\tenant_id_list.csv')
 tenantid = df['tenant_id'].tolist() #tenant_id is the column name
 logging.info('List of Tenant ids: {}'.format(tenantid))
except FileNotFoundError:
  print("tenant_id_list.csv is not placed in correct path - C:\OCI_Scripts\\")
  exit()

#driver = webdriver.Chrome("D:\\Web Drivers\\chromedriver.exe") #ChromeDriver
driver = webdriver.Firefox(executable_path="C:\\Web Drivers\\geckodriver.exe") #---> for Firefox
for id in tenantid:
  try:
    print("Loading", id)
    logging.info('Currently Loading: {}'.format(id))
    url="https://"+id+"-admin.occa.ocs.oraclecloud.com/occs-admin/"
    #Below regex code to extract tenant id from url, in case of iterating list of urls instead of tenant_ids --start--
    #test_string = url
    #pattern = "(?<=https://)[^-]+"
    #c = re.search("((?<=https://)[^-]+)", test_string)
    #a=c.group(1) regex code --end--
    a=id
    b=a[:-3]+a[-3].upper()+a[-2].upper()+a[-1].upper()
    password = b+"!!"
    passotp  = b
    username = "cod-ops_ww@oracle.com"
    driver.get(url)
    driver.maximize_window()
    driver.implicitly_wait(20)
    username_textbox = driver.find_element_by_id("cc-login-login")
    username_textbox.send_keys(username)
    password_textbox=  driver.find_element_by_id('cc-login-password')
    password_textbox.send_keys(password)
    otp_pass= driver.find_element_by_id("cc-login-passcode")
    otp_pass.send_keys(passotp)
    login_button= driver.find_element_by_xpath('//*[@id="ui-id-8"]')
    login_button.click()
  except TimeoutException:
     print("Check your net bandwidth while loading ", url)
     logging.error('Timedout Exception Occurred, could not load-> {}'.format(url))
  except NoSuchElementException:
     print("For URL:", url , "-->  Admin logins May have SSO Login template OR could be thrown 502 Gateway. Kindly review")
     logging.error('It May have SSO Login template OR Error could be 502 Bad Gateway. Kindly review -> {}'.format(url))
  except TypeError:
     print("Skipping row-->", url )
#Since Selenium-limiations cant load status code of mfa_login response, below condtion will check if the login is success or not.
  #sleep(5)
  try:
     find_dshbrd=driver.find_element_by_xpath('//*[@id="cc-page-home-section-title"]')
  except NoSuchElementException:
     print("Tool Has Failed to Load Homepage for ", url, "Kindly review manually.")
     logging.error('LOGGING FAILED FOR-> {}'.format(url))
  #sleep(2)
  for i in range(len(url)):
      driver.execute_script("window.open();")
      curWindowHndl = driver.current_window_handle
      logging.info('Current Window: {}'.format(curWindowHndl))
      wv = driver.switch_to.window(driver.window_handles[i - 1])
      #sleep(5)
      break

end = datetime.now()
end_time=end.strftime("%H:%M:%S")
print("Ending AT ", end_time)
logging.info('Ending AT  {}'.format(end_time))
