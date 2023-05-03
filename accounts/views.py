from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin

from accounts.forms import (LoginForm, ProfileEditForm, UserEditForm,
                            UserRegistrationForm)
from accounts.models import Profile
from django.contrib.auth.decorators import login_required

def user_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            print(data)
            user = authenticate(request,
                                username=data['username'],
                                password=data['password'])
            print(user)
            
            if user is not None:
                if user.is_active:
                    login(request,user)
                    return HttpResponse("Muaffaqiyatli login amalga oshirildi!")
                else:
                    return HttpResponse("Sizning profilingiz faol holatda emas")
            else:
                return HttpResponse("Login va parolda xatolik bor")
    else:
        form = LoginForm()
        context = {
            "form":form
        }
    return render(request,'registration/login.html',context)
@login_required()
def dashboard_view(request):
    user = request.user
    profile_info = Profile.objects.get(user=user)
    context = {
        "user":user,
        "profile":profile_info
    }
    return render(request,'pages/user_profile.html',context)

def user_register(request):
    if request.method == "POST":
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(
                user_form.cleaned_data["password"]
            )
            new_user.save()
            Profile.objects.create(user=new_user)
            context = {
                "new_user":new_user
            }
            return render(request,"account/register_done.html",context)
    else:
        user_form = UserRegistrationForm()
        context = {
            "user_form":user_form
        }
        return render(request,"account/register.html",context)

# class SignUpView(CreateView):
#     form_class = UserCreationForm
#     success_url = reverse_lazy('login')
#     template_name = 'account/register.html'
@login_required()
def edit_user(request):
    if request.method == "POST":
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile,
                                       data=request.POST,
                                       files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('user_profile')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request,'account/profile_edit.html',{"user_form":user_form,'profile_form':profile_form})

class EditUserView(LoginRequiredMixin,View):

    def get(self,request):
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
        return render(request,'account/profile_edit.html',{"user_form":user_form,'profile_form':profile_form})

    def post(self,request):
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile,
                                       data=request.POST,
                                       files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('user_profile')
