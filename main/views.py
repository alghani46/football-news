from django.shortcuts import render

# Create your views here.
def show_main(request):
    context = {
        'npm': '2406365396',
        'name': 'Muhammad Rifqi Al Ghani',
        'class': 'KKI'
    }
    return render(request, "main.html", context)

def create_news(request):
    form = NewsForm(request.POST or None)

    if form.is_valid() and request.method == "POST":
        form.save()
        return redirect('main:show_main')

    context = {'form': form}
    return render(request, "create_news.html", context)

def show_news(request, id):
    news = get_object_or_404(News, pk=id)
    news.increment_views()

    context = {
        'news': news
    }

    return render(request, "news_detail.html", context)



#return render(request, "main.html", context) is used to render the main.html view using the render function. The render function takes three arguments:
#request: This is an HTTP request object sent by the user.
#main.html: This is the name of the template file that will be used to render the view.
#context: This is the dictionary containing data that will be passed to the view for dynamic rendering.