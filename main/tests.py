from django.test import TestCase, Client
from .models import News

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

#The Client class imported from django.test is used to simulate a client for unit testing purposes.
#The test_main_url_is_exist function checks whether the server gives a 200 (OK) response when the client accesses the endpoint (main page).
#The test_main_using_main_template function checks whether the main page returns status code 200 and is rendered using the main.html template.
#The test_nonexistent_page function tests that if the client accesses a URL that doesn't exist (e.g., /burhan_always_exists/), the Django application will return a 404 (Not Found) status code.
#The test_news_creation function tests creating a new News object with specific attributes (title, content, category, news_views, and is_featured). After the object is created, it checks the is_news_hot property, category, and is_featured.
#The test_news_default_values function tests the default values of the News model when only required fields (title and content) are filled, ensuring default category is "update", news_views is 0, is_featured is False, and is_news_hot is False.
#The test_increment_views function tests the functionality of the increment_views() method that increases views by 1.
#The test_is_news_hot_threshold function tests the threshold of the is_news_hot property, ensuring news with 20 views is not considered hot, while news with 21 views is considered hot.