
from django.test import TestCase, Client
from .models import News
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from django.contrib.auth.models import User
class MainTest(TestCase):
    def test_main_url_is_exist(self):
        response = Client().get('')
        self.assertEqual(response.status_code, 200)

    def test_main_using_main_template(self):
        response = Client().get('')
        self.assertTemplateUsed(response, 'main.html')

    def test_nonexistent_page(self):
        response = Client().get('/burhan_always_exists/')
        self.assertEqual(response.status_code, 404)

    def test_news_creation(self):
        news = News.objects.create(
          title="BURHAN FC WINS",
          content="BURHAN FC 1-0 PANDA BC",
          category="match",
          news_views=1001,
          is_featured=True
        )
        self.assertTrue(news.is_news_hot)
        self.assertEqual(news.category, "match")
        self.assertTrue(news.is_featured)
        
    def test_news_default_values(self):
        news = News.objects.create(
          title="Test News",
          content="Test content"
        )
        self.assertEqual(news.category, "update")
        self.assertEqual(news.news_views, 0)
        self.assertFalse(news.is_featured)
        self.assertFalse(news.is_news_hot)
        
    def test_increment_views(self):
        news = News.objects.create(
          title="Test News",
          content="Test content"
        )
        initial_views = news.news_views
        news.increment_views()
        self.assertEqual(news.news_views, initial_views + 1)
        
    def test_is_news_hot_threshold(self):
        # Test news with exactly 20 views (should not be hot)
        news_20 = News.objects.create(
          title="News with 20 views",
          content="Test content",
          news_views=20
        )
        self.assertFalse(news_20.is_news_hot)
        
        # Test news with 21 views (should be hot)
        news_21 = News.objects.create(
          title="News with 21 views", 
          content="Test content",
          news_views=21
        )
        self.assertTrue(news_21.is_news_hot)





class FootballNewsFunctionalTest(LiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Create single browser instance for all tests
        cls.browser = webdriver.Chrome()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        # Close browser after all tests complete
        cls.browser.quit()

    def setUp(self):
        # Create user for testing
        self.test_user = User.objects.create_user(
            username='testadmin',
            password='testpassword'
        )

    def tearDown(self):
        # Clean up browser state between tests
        self.browser.delete_all_cookies()
        self.browser.execute_script("window.localStorage.clear();")
        self.browser.execute_script("window.sessionStorage.clear();")
        # Navigate to blank page to reset state
        self.browser.get("about:blank")

    def login_user(self):
        """Helper method to login user"""
        self.browser.get(f"{self.live_server_url}/login/")
        username_input = self.browser.find_element(By.NAME, "username")
        password_input = self.browser.find_element(By.NAME, "password")
        username_input.send_keys("testadmin")
        password_input.send_keys("testpassword")
        password_input.submit()

    def test_login_page(self):
        # Test login functionality
        self.login_user()

        # Check if login is successful
        wait = WebDriverWait(self.browser, 120)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "h1")))
        h1_element = self.browser.find_element(By.TAG_NAME, "h1")
        self.assertEqual(h1_element.text, "Football News")

        logout_link = self.browser.find_element(By.PARTIAL_LINK_TEXT, "Logout")
        self.assertTrue(logout_link.is_displayed())

    def test_register_page(self):
        # Test register functionality
        self.browser.get(f"{self.live_server_url}/register/")

        # Check if register page opens
        h1_element = self.browser.find_element(By.TAG_NAME, "h1")
        self.assertEqual(h1_element.text, "Register")

        # Fill register form
        username_input = self.browser.find_element(By.NAME, "username")
        password1_input = self.browser.find_element(By.NAME, "password1")
        password2_input = self.browser.find_element(By.NAME, "password2")

        username_input.send_keys("newuser")
        password1_input.send_keys("complexpass123")
        password2_input.send_keys("complexpass123")
        password2_input.submit()

        # Check redirect to login page
        wait = WebDriverWait(self.browser, 120)
        wait.until(EC.text_to_be_present_in_element((By.TAG_NAME, "h1"), "Login"))
        login_h1 = self.browser.find_element(By.TAG_NAME, "h1")
        self.assertEqual(login_h1.text, "Login")

    def test_create_news(self):
        # Test create news functionality (requires login)
        self.login_user()

        # Go to create news page
        add_button = self.browser.find_element(By.PARTIAL_LINK_TEXT, "Add News")
        add_button.click()

        # Fill form
        title_input = self.browser.find_element(By.NAME, "title")
        content_input = self.browser.find_element(By.NAME, "content")
        category_select = self.browser.find_element(By.NAME, "category")
        thumbnail_input = self.browser.find_element(By.NAME, "thumbnail")
        is_featured_checkbox = self.browser.find_element(By.NAME, "is_featured")

        title_input.send_keys("Test News Title")
        content_input.send_keys("Test news content for selenium testing")
        thumbnail_input.send_keys("https://example.com/image.jpg")

        # Set category (select 'match' from dropdown)

        select = Select(category_select)
        select.select_by_value("match")

        # Check is_featured checkbox
        is_featured_checkbox.click()

        # Submit form
        title_input.submit()

        # Check if returned to main page and news appears
        wait = WebDriverWait(self.browser, 120)
        wait.until(EC.text_to_be_present_in_element((By.TAG_NAME, "h1"), "Football News"))
        h1_element = self.browser.find_element(By.TAG_NAME, "h1")
        self.assertEqual(h1_element.text, "Football News")

        # Check if news title appears on page
        wait.until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "Test News Title")))
        news_title = self.browser.find_element(By.PARTIAL_LINK_TEXT, "Test News Title")
        self.assertTrue(news_title.is_displayed())

    def test_news_detail(self):
        # Test news detail page

        # Login first because of @login_required decorator
        self.login_user()

        # Create news for testing
        news = News.objects.create(
            title="Detail Test News",
            content="Content for detail testing",
            user=self.test_user
        )

        # Open news detail page
        self.browser.get(f"{self.live_server_url}/news/{news.id}/")

        # Check if detail page opens correctly
        self.assertIn("Detail Test News", self.browser.page_source)
        self.assertIn("Content for detail testing", self.browser.page_source)

    def test_logout(self):
        # Test logout functionality
        self.login_user()

        # Click logout button - text is inside button, not link
        logout_button = self.browser.find_element(By.XPATH, "//button[contains(text(), 'Logout')]")
        logout_button.click()

        # Check if redirected to login page
        wait = WebDriverWait(self.browser, 120)
        wait.until(EC.text_to_be_present_in_element((By.TAG_NAME, "h1"), "Login"))
        h1_element = self.browser.find_element(By.TAG_NAME, "h1")
        self.assertEqual(h1_element.text, "Login")

    def test_filter_main_page(self):
        # Test filter functionality on main page
        #         
        # Create news for testing
        News.objects.create(
            title="My Test News",
            content="My news content",
            user=self.test_user
        )
        News.objects.create(
            title="Other User News", 
            content="Other content",
            user=self.test_user  # Same user for simplicity
        )

        self.login_user()

        # Test filter "All Articles"
        wait = WebDriverWait(self.browser, 120)
        wait.until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "All Articles")))
        all_button = self.browser.find_element(By.PARTIAL_LINK_TEXT, "All Articles")
        all_button.click()
        self.assertIn("My Test News", self.browser.page_source)
        self.assertIn("Other User News", self.browser.page_source)

        # Test filter "My Articles"  
        my_button = self.browser.find_element(By.PARTIAL_LINK_TEXT, "My Articles")
        my_button.click()
        self.assertIn("My Test News", self.browser.page_source)
#The Client class imported from django.test is used to simulate a client for unit testing purposes.
#The test_main_url_is_exist function checks whether the server gives a 200 (OK) response when the client accesses the endpoint (main page).
#The test_main_using_main_template function checks whether the main page returns status code 200 and is rendered using the main.html template.
#The test_nonexistent_page function tests that if the client accesses a URL that doesn't exist (e.g., /burhan_always_exists/), the Django application will return a 404 (Not Found) status code.
#The test_news_creation function tests creating a new News object with specific attributes (title, content, category, news_views, and is_featured). After the object is created, it checks the is_news_hot property, category, and is_featured.
#The test_news_default_values function tests the default values of the News model when only required fields (title and content) are filled, ensuring default category is "update", news_views is 0, is_featured is False, and is_news_hot is False.
#The test_increment_views function tests the functionality of the increment_views() method that increases views by 1.
#The test_is_news_hot_threshold function tests the threshold of the is_news_hot property, ensuring news with 20 views is not considered hot, while news with 21 views is considered hot.