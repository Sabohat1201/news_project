from django.shortcuts import render,get_object_or_404

from .models import News, Category

from .forms import ContantForm
from django.http import HttpResponse
from django.views.generic import TemplateView,ListView


def news_list(request):
   # news_list = News.objects.filter(status=News.Status.Published)
    news_list = News.published.all()
    context = {
        "news_list":news_list
    }
    return render(request, "news_list.html",context)

def news_detail(request,news):
    news = get_object_or_404(News, slug=news, status=News.Status.Published)
    
    context = {
        "news":news
    }
    
    return render(request,"news_detail.html",context)

# def HomePagesView(request):
#     categories = Category.objects.all()
#     news_list = News.published.all().order_by('-publish_time')[:10]# bu boshidagi 10ta postni chiqar
#     local_one = News.published.filter(category__name="Mahalliy").order_by("-publish_time")[:1]
#     local_news = News.published.all().filter(category__name="Mahalliy")[1:6]
#     context = {
#         'news_list':news_list,
#         'categories':categories,
#         'local_one':local_one,
#         'local_news':local_news
#     }
    
#     return render(request,'home.html',context)

class HomePagesView(ListView):
    model = News
    template_name = 'home.html'
    context_object_name = 'news'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['news_list'] = News.published.all().order_by('-publish_time')[:]
        context['mahalliy_xabarlar'] = News.published.all().filter(category__name="Mahalliy").order_by("-publish_time")[:5]
        context['xorij_xabarlari'] = News.published.all().filter(category__name="Xorij").order_by("-publish_time")[:5]
        context['sport_xabarlari'] = News.published.all().filter(category__name="Sport").order_by("-publish_time")[:5]
        context['texnologik_xabarlar'] = News.published.all().filter(category__name="Texnologiya").order_by("-publish_time")[:5]

        return context

# def contactPageView(request):
#     print(request.POS)
#     form = ContantForm(request.POST or None)
#     if request.method == "POST" and form.is_valid():
#         form.save()
#         return HttpResponse("<h2> Biz bilan bog'langaningiz uchun tashakkur! ")
#     context = {
#         "form":form
#     }
    
#     return render(request,'conhtml', context)

class contactPageView(TemplateView):
    template_name = 'news/contact.html'

    def get(self,request,*args,**kwargs):
        form = ContantForm()
        context = {
            "form": form 

        }
        return render(request,'contact.html',context)
    def post(self,request,*args,**kwargs):
        form = ContantForm(request.POST)
        if request.method == "POST" and form.is_valid():
            print(form.data)
            form.save()
            return HttpResponse("<h2> Biz bilan bog'langaningiz uchun tashakkur! ")
        context = {
            "form":form
        }
        return render(request,'contact.html',context)
    
class LocalNewsView(ListView):
    model = News
    template_name = "mahalliy.html"
    context_object_name = 'mahalliy_yangiliklar'

    def get_queryset(self):
        news = self.model.published.all().filter(category__name="Mahalliy")
        return news

class ForeignNewsView(ListView):
    model = News
    template_name = "xorij.html"
    context_object_name = 'xorij_yangiliklari'

    def get_queryset(self):
        news = self.model.published.all().filter(category__name="Xorij")
        return news

class TechnologyNewsView(ListView):
    model = News
    template_name = "texnologiya.html"
    context_object_name = 'texnologik_yangiliklar'

    def get_queryset(self):
        news = self.model.published.all().filter(category__name="Texnologiya")
        return news

class SportNewsView(ListView):
    model = News
    template_name = "sport.html"
    context_object_name = 'sport_yangiliklari'

    def get_queryset(self):
        news = self.model.published.all().filter(category__name="Sport")
        return news
