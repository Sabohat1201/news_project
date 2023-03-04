from django.urls import path
from .views import news_list,news_detail,HomePagesView,contactPageView,LocalNewsView,ForeignNewsView,TechnologyNewsView,SportNewsView

urlpatterns = [
    path('',HomePagesView.as_view(), name='home'),
    path('news/', news_list, name="all_news_list"),
    path('news/<slug:news>/',news_detail,name="news_detail_page"),
    path('contact-us/',contactPageView.as_view(), name='contact_page'),
    path('local', LocalNewsView.as_view(),name="local_news_page"),
    path('foreign/',ForeignNewsView.as_view(), name="foreign_news_page"),
    path('technology/',TechnologyNewsView.as_view(),name="technology_news_page"),
    path('sport/',SportNewsView.as_view(),name="sport_news_page"),

]