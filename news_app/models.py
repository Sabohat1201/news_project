from django.db import models
from django.utils import timezone
from django.urls import reverse


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=News.Status.Published)

class Category(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name

class News(models.Model):

    class Status(models.TextChoices):
        Draft = "DF", "Draft"
        Published = "PB", "Published"
    
    title = models.CharField(max_length=300)
    slug = models.SlugField(max_length=250)
    body = models.TextField()
    image = models.ImageField(upload_to='news/images')
    category = models.ForeignKey(Category,
                                on_delete=models.CASCADE) 
    publish_time = models.DateTimeField(default=timezone.now)
    created_time = models.DateTimeField(auto_now_add=True) # avtomatik ravishda vaqtini qo'shib ketadi bu vaqtni biz o'zgartiromaymiz 
    updated_time = models.DateTimeField(auto_now=True) #buni biz xolagan vaqtda o'zgartirolamiz
    status = models.CharField(max_length=2,
                             choices=Status.choices,
                             default=Status.Draft
                             )

    objects = models.Manager() # default manager
    published = PublishedManager()

    class Meta:
        ordering = ["-publish_time"] # bu eng oxiri qo'shilgan yangilikni birinchi bo'lib ko'rsatadi

    def __str__(self): #bu bizga admin qismida ma'lumotlarni chiqarib beradi
        return self.title # har bir yangilikni sarlavhasi bilan ko'rsatgin
    
    def get_absolute_url(self):
        return reverse("news_detail_page", args=[self.slug])


class Contact(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField(max_length=150)
    message = models.TextField()

    def __str__(self):
        return self.email
    






























































































