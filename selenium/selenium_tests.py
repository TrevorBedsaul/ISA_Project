import unittest
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import NoSuchElementException

class TestTemplate(unittest.TestCase):
    """Include test cases on a given url"""

    def setUp(self):
        """Start web driver"""
        self.driver = webdriver.Remote(
            command_executor='http://selenium-chrome:4444/wd/hub',
            desired_capabilities=DesiredCapabilities.CHROME)
        self.driver.implicitly_wait(2)

    def tearDown(self):
        """Stop web driver"""
        self.driver.quit()

    def test_book_link(self):
        """Find and click book title button"""
        try:
            self.driver.get('http://web:8000/')
            el = self.driver.find_element_by_class_name('lead')
            el.click()
            info = self.driver.find_element_by_class_name("starter-template")
            contains_title = "Winnie the Pooh" in info.get_attribute("innerHTML")
            self.assertTrue(contains_title)
        except NoSuchElementException as ex:
            self.fail(ex.msg)

    def test_login_logout(self):
        """Log in using web interface"""
        try:
            self.driver.get('http://web:8000/login')
            username = self.driver.find_element_by_id('id_username')
            username.send_keys("stevendicarlo2")
            password = self.driver.find_element_by_id('id_password')
            password.send_keys("Password1")
            submit = self.driver.find_element_by_class_name("btn-lg")
            submit.click()
            self.assertEqual(self.driver.title, "Homepage")

            logout = self.driver.find_element_by_partial_link_text("Logout")
            self.assertEqual(logout.get_attribute("href"), "http://web:8000/logout")
            logout.click()

            login_button = self.driver.find_element_by_partial_link_text("Login")
            self.assertEqual(login_button.get_attribute("href"), "http://web:8000/login")
        except NoSuchElementException as ex:
            self.fail(ex.msg)


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestTemplate)
    unittest.TextTestRunner(verbosity=2).run(suite)