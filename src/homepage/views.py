import uuid
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse
from category.models import Scholarship, Country
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from user.models import Profile
from user.forms import CreateUserForm
from django.contrib.sites.shortcuts import get_current_site  
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode  
from django.template.loader import render_to_string  
from user.utils import account_activation_token  
from django.core.mail import EmailMessage  
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from category.models import Level
# Create your views here.

def homepage(request):
    country_lists = Country.objects.all()
    return render(request,"homepage/home.html", {'country_lists':country_lists})


def register(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  
            user.is_active = False  
            user.save()  
             
            current_site = get_current_site(request)  
            mail_subject = 'Activation link has been sent to your email id'  
            message = render_to_string('user/email/acc_active_email.html', {  
                'user': user,  
                'domain': current_site.domain,  
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),  
                'token':account_activation_token.make_token(user),  
            })  
            to_email = form.cleaned_data.get('email')  
            email = EmailMessage(  
                        mail_subject, message, to=[to_email]  
            )  
            email.send()  
            # return HttpResponse('Please confirm your email address to complete the registration')
            message = 'Please confirm your email address to complete the registration'
            return render(request, 'user/response/response.html',{'message':message}) 
    else:                         
        form = CreateUserForm()
    return render(request, 'user/register.html', {'form': form})

def activate(request, uidb64, token):  
    User = get_user_model()  
    try:  
        uid = force_str(urlsafe_base64_decode(uidb64))  
        user = User.objects.get(pk=uid)  
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):  
        user = None  
    if user is not None and account_activation_token.check_token(user, token):  
        user.is_active = True  
        user.save()  
        message = 'Thank you for your email confirmation. Now you can login your account'
        # return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
        return render(request, 'user/response/response.html',{'message':message})  
    else:  
        message = 'Activation link is invalid!'
        return render(request, 'user/response/response.html',{'message':message})   




def login(request):
    message = '' 
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        try:
            user = auth.authenticate(username= username, password=password)
            if user.is_staff or user.is_superuser :
                auth.login(request, user)
                message = 'Login Successfully.'
                return redirect('admin/')
            elif user is not None:
                auth.login(request, user)
                message= 'Login Successfully.'
                return redirect('profile')
            else:
                message= 'Invalid Credentials.'
                return redirect('login')
        except:
            message='Check and login again'
            return render(request, "user/login.html", {'message':message})
    elif request.user.is_authenticated:
        return redirect('home')
    else:
        return render(request, "user/login.html", {'message':message})

def logout(request):
    auth.logout(request)
    
        
    return redirect('home')

@login_required
def profile(request):
    return render(request,"user/profile.html")

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
import os
from django.conf import settings
class UserDeleteView(LoginRequiredMixin, View):
    template_name = 'user/delete_confirmation.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        message = ''
        password = request.POST.get('confirm_password', '')
        user = request.user
        if user.check_password(password):
            profile = get_object_or_404(Profile, user = user)
            if profile.profile_pic:
                image_path = os.path.join(settings.MEDIA_ROOT, 'images/profile_pics',str(profile.profile_pic))
                if os.path.exists(image_path):
                    os.remove(image_path)
            profile.delete()
            user.delete()
            message = 'Your account has been deleted.'
            return render(request, 'user/login.html', {'message':message})
        else:
            message = 'Invalid password.'
            return render(request, 'user/delete_confirmation.html', {'message':message})

# For Category
def show_category(request):
    return render(request,"category/category.html")

from django.db.models import Q
# search
def search(request):
    if request.method == "POST":
        searched = request.POST['searched']
        
        scholarships_lists = Scholarship.objects.filter(
            Q(level__icontains=searched) |
            Q(school__icontains=searched) |
            Q(description__icontains=searched) |
            Q(link_web__icontains=searched) |
            Q(country__icontains=searched)
        ).all()
        country_lists = Country.objects.all()
        level_lists = Level.objects.all()
        context = {'searched':searched, 
                   'scholarships_lists':scholarships_lists,
                   'country_lists': country_lists,
                   'level_lists':level_lists}
        return render(request,'homepage/search.html', context)
                  
    else:
        return render(request, 'homepage/search.html', {})

#For aboutpage
def about(request):
    return render(request,"about/about.html")
#For contactus
def contact(request):
    return render(request,"contact/contact_us.html")
#For contactus
def contact_us(request):
    return render(request,"contact/contact_us.html")

def custom_404_view(request):
    return render(request, '404.html')

