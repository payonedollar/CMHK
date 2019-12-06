import sys
sys.path.insert(1, '../')
import config
import pytest
import time
import json
import random
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys

from ipaddress import IPv4Address
from pyairmore.request import AirmoreSession
from pyairmore.services.device import DeviceService
from pyairmore.services.messaging import MessagingService


class TestCMHK_DBS_MASTER():
	
	PIN_CODE = ""

	def setup_method(self, method):
		if ( lower(config.core['broswer']) == "firefox")
			self.driver = webdriver.Firefox()
		else if ( lower(config.core['broswer']) == "chrome")
			self.driver = webdriver.Chrome()
		self.vars = {}

	def teardown_method(self, method):
		self.driver.quit()
	
	def waitForPasscodeLabel(self, method):
	
		global PIN_CODE
		
		session = AirmoreSession(IPv4Address(str(config.core['airmore_server'])))  # also you can put your port as int, airmore's port default is 2333	
		session.is_server_running  # True
		session.request_authorization()  # True if accepted, False if denied

		service = MessagingService(session)
		messages = service.fetch_message_history()

		pattern = "For your online transaction, please use this MasterCard SecureCode One-Time Password: (\w{4})-(\d{6})"

		for msg in messages:
			group = re.findall(pattern, msg.content)
			if len(group) > 0 and len(group[0]) > 0:
				if group[0][0] == str(self.driver.find_element(By.CSS_SELECTOR , "#pwdpage > table:nth-child(2) > tbody:nth-child(1) > tr:nth-child(3) > td:nth-child(1) > table:nth-child(3) > tbody:nth-child(1) > tr:nth-child(9) > td:nth-child(2) > span:nth-child(2)").text):
					PIN_CODE = str(group[0][1])
					return True
		
		return False
  
	def test_CMHK_DBS_MASTER(self):
		self.driver.get("https://1cm.hk.chinamobile.com/bill/index.html")
		self.driver.set_window_size(1309, 914)
		WebDriverWait(self.driver, 30).until(expected_conditions.element_to_be_clickable((By.ID, "BillPayment_msisdn")))
		self.driver.find_element(By.ID, "BillPayment_msisdn").click()
		self.driver.find_element(By.ID, "BillPayment_msisdn").send_keys(str(config.core['msisdn']))

		WebDriverWait(self.driver, 30).until(expected_conditions.element_to_be_clickable((By.ID, "BillPayment_amount")))
		self.driver.find_element(By.ID, "BillPayment_amount").click()
		self.driver.find_element(By.ID, "BillPayment_amount").send_keys("1")

		WebDriverWait(self.driver, 30).until(expected_conditions.element_to_be_clickable((By.NAME, "yt0")))
		self.driver.find_element(By.NAME, "yt0").click()

		WebDriverWait(self.driver, 30).until(expected_conditions.element_to_be_clickable((By.CSS_SELECTOR, ".paybutton_master")))
		self.driver.find_element(By.CSS_SELECTOR, ".paybutton_master").click()

		WebDriverWait(self.driver, 30).until(expected_conditions.element_to_be_clickable((By.ID, "cardNo2")))
		self.driver.find_element(By.ID, "cardNo2").click()
		self.driver.find_element(By.ID, "cardNo2").send_keys(str(config.dbs_black_world_master['cardNo']))

		WebDriverWait(self.driver, 30).until(expected_conditions.element_to_be_clickable((By.ID, "epMonth2")))
		self.driver.find_element(By.ID, "epMonth2").click()
		dropdown = self.driver.find_element(By.ID, "epMonth2")
		dropdown.find_element(By.XPATH, "//option[. = " + str(config.dbs_black_world_master['epMonth']) + "]").click()
		self.driver.find_element(By.ID, "epMonth2").click()

		WebDriverWait(self.driver, 30).until(expected_conditions.element_to_be_clickable((By.ID, "epYear2")))
		self.driver.find_element(By.ID, "epYear2").click()
		dropdown = self.driver.find_element(By.ID, "epYear2")
		dropdown.find_element(By.XPATH, "//option[. = " + str(config.dbs_black_world_master['epYear']) + "]").click()
		self.driver.find_element(By.ID, "epYear2").click()

		WebDriverWait(self.driver, 30).until(expected_conditions.element_to_be_clickable((By.ID, "cardHolder2")))
		self.driver.find_element(By.ID, "cardHolder2").click()
		self.driver.find_element(By.ID, "cardHolder2").send_keys(str(config.dbs_black_world_master['cardHolder']))

		WebDriverWait(self.driver, 30).until(expected_conditions.element_to_be_clickable((By.NAME, "securityCode2")))
		self.driver.find_element(By.NAME, "securityCode2").click()
		self.driver.find_element(By.NAME, "securityCode2").send_keys(str(config.dbs_black_world_master['securityCode']))

		WebDriverWait(self.driver, 30).until(expected_conditions.element_to_be_clickable((By.NAME, "submitBut")))
		self.driver.find_element(By.NAME, "submitBut").click()
		self.driver.switch_to.alert.accept()

		WebDriverWait(self.driver, 120).until(self.waitForPasscodeLabel)
		WebDriverWait(self.driver, 30).until(expected_conditions.element_to_be_clickable((By.NAME, "completepin")))
		self.driver.find_element(By.NAME, "completepin").click()
		self.driver.find_element(By.NAME, "completepin").send_keys(PIN_CODE)
		self.driver.find_element(By.CSS_SELECTOR, "tr:nth-child(10) input").click()

		WebDriverWait(self.driver, 60).until(expected_conditions.element_to_be_clickable((By.CSS_SELECTOR, ".paymentBtn:nth-child(1)")))
		self.driver.find_element(By.CSS_SELECTOR, ".paymentBtn:nth-child(1)").click()
		self.driver.close()

