from django.urls import path
from main.views import show_main
from main.views import show_main, create_news, show_news
app_name = 'main'

urlpatterns = [
    path('', show_main, name='show_main'),
    path('create-news/', create_news, name='create_news'),
    path('news/<str:id>', show_news, name='show_news'),
]



#Code Explanation:

#The urls.py file contains routing configurations for the main application.
#We import the path function from the django.urls module to define URL patterns.
#We import the show_main function from main.views to be called when a URL matches the defined pattern.
#app_name = 'main' is used to give a unique namespace to URLs in an application, making them easily distinguishable when there are many applications and endpoints in our Django project.
#urlpatterns is a list containing URLPattern objects returned by the path() function.
#In this example, there is only one route '' (root), which will call the show_main view.
#The optional argument name='show_main' allows us to easily reverse URLs using a path's name, not its hardcoded string.