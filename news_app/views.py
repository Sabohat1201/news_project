
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import (CreateView, DeleteView, ListView,
                                  TemplateView, UpdateView)
from hitcount.views import HitCountDetailView,HitCountMixin

from config.custom_permissions import OnlyLoggedSuperUser

from .forms import CommentForm, ContantForm
from .models import Category, News
from hitcount.utils import get_hitcount_model


@login_required()
def news_list(request):
   # news_list = News.objects.filter(status=News.Status.Published)
    news_list = News.published.all()
    context = {
        "news_list":news_list
    }
    return render(request, "news_list.html",context)



def news_detail(request,news):
    news = get_object_or_404(News, slug=news, status=News.Status.Published)
    context = {}
    #hitcount_logic
    hit_count = get_hitcount_model().objects.get_for_object(news)
    hits = hit_count.hits
    hitcontext = context['hitcount'] = {'pk': hit_count.pk}
    hit_count_response = HitCountMixin.hit_count(request, hit_count)
    if hit_count_response.hit_counted:
        hits = hits + 1
        hitcontext['hit_counted'] = hit_count_response.hit_counted
        hitcontext['hit_message'] = hit_count_response.hit_message
        hitcontext['total_hits'] = hits

    comments = news.comments.filter(active=True)
    comment_count = comments.count()
    new_comment = None
    if request.method == "POST":
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            #yangi comment obyektini yaratamiz lekin ma'lumotlar bazasiga(DB) saqlamaymiz
            new_comment = comment_form.save(commit=False)
            new_comment.news = news
            #izoh egasini so'rov yuborayotgan userga bog'ladik
            new_comment.user = request.user
            #ma'limotlar bazasiga saqlaymiz
            new_comment.save()
            comment_form = CommentForm()
    else:
        comment_form = CommentForm()
    context = {
        "news":news,
        "comments":comments,
        "comment_count":comment_count,
        "new_comment":new_comment,
        "comment_form":comment_form,
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

class HomePagesView(LoginRequiredMixin, ListView):
    model = News
    template_name = 'home.html'
    context_object_name = 'news'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['news_list'] = News.published.all().order_by('-publish_time')[:3]
        context['mahalliy_xabarlar'] = News.published.all().filter(category__name="Mahalliy").order_by("-publish_time")[:4]
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


class NewsUpdateView(OnlyLoggedSuperUser,UpdateView):
    model = News
    fields = ('title','body','image','category','status')
    template_name = "crud/news_edit.html"
    
class NewsDeleteView(OnlyLoggedSuperUser,DeleteView):
    model = News
    template_name = 'crud/news_delete.html'
    success_url = reverse_lazy("home_page")

class NewsCreateView(OnlyLoggedSuperUser,CreateView):
    model = News
    template_name = 'crud/news_create.html'
    fields = ('title','slug','body','image','category','status')
@login_required()
@user_passes_test(lambda u:u.is_superuser)
def admin_page_view(request):
    admin_users = User.objects.filter(is_superuser=True)

    context = {
        'admin_users':admin_users
    }
    return render(request,'pages/admin_page.html',context)
    
class SearchResultsList(ListView):
    model = News
    template_name = 'search_result.html'
    context_object_name = 'barcha_yangiliklar'

    def get_queryset(self):
        query = self.request.GET.get('q')
        return News.objects.filter(
            Q(title__icontains=query) | Q(body__icontains=query)
        )