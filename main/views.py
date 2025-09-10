from django.shortcuts import render, redirect, get_object_or_404
from main.forms import NewsForm
from main.models import News
from django.http import HttpResponse
from django.core import serializers
from .models import News
# Create your views here.
def show_main(request):
    news_list = News.objects.all()  # fetch all news from DB
    context = {
        'npm': '2406365396',
        'name': 'Muhammad Rifqi Al Ghani',
        'class': 'KKI',
        'news_list': news_list
    }
    return render(request, "main.html", context)

def create_news(request):
    form = NewsForm(request.POST or None)

    if form.is_valid() and request.method == "POST":
        form.save()
        return redirect('main:show_main')

    context = {'form': form}
    return render(request, "create_news.html", context)

def show_news(request, news_id):
    news = get_object_or_404(News, pk=news_id)
    context = {'news': news}
    return render(request, "news_detail.html", context)


def show_xml(request):
    news_list = News.objects.all()
    xml_data = serializers.serialize("xml", news_list)
    return HttpResponse(xml_data, content_type="application/xml")

def show_json(request):
    news_list = News.objects.all()
    json_data = serializers.serialize("json", news_list)
    return HttpResponse(json_data, content_type="application/json")



def show_xml_by_id(request, news_id):
    news_item = News.objects.filter(pk=news_id)
    if news_item.exists():
        xml_data = serializers.serialize("xml", news_item)
        return HttpResponse(xml_data, content_type="application/xml")
    else:
        return HttpResponse(status=404)


def show_json_by_id(request, news_id):
    try:
        news_item = News.objects.get(pk=news_id)
        json_data = serializers.serialize("json", [news_item]) 
        return HttpResponse(json_data, content_type="application/json")
    except News.DoesNotExist:
        return HttpResponse(status=404)

#return render(request, "main.html", context) is used to render the main.html view using the render function. The render function takes three arguments:
#request: This is an HTTP request object sent by the user.
#main.html: This is the name of the template file that will be used to render the view.
#context: This is the dictionary containing data that will be passed to the view for dynamic rendering.