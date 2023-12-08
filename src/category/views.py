import random
from sqlite3 import IntegrityError
import string
from bs4 import BeautifulSoup
from django.http import JsonResponse
import requests
from django.utils.text import slugify
from .models import Scholarship, Country
from django.core.paginator import Paginator
from django.shortcuts import render, redirect 
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404
from .models import Scholarship
from .models import FavoriteScholarship, Favorited, Comment, Reply, Level
from django.contrib.auth.decorators import login_required
from .forms import CommentForm, ReplyForm
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import ScholarshipForm
# SCRAPED

def scrape_data(request):
    add_to_model = True  
    results = []  # List to store the scraped objects
    for i in range(1, 3):
        web_link = f'https://www.idp.com/cambodia/search/scholarship/?studyLevel=%3Aundergraduate&page={i}'
        r = requests.get(web_link)
        soup = BeautifulSoup(r.content, 'lxml')
        lists = soup.find_all('div', class_='pro_wrap')
        
        for lst in lists:
            listing = lst.find_all('div', class_='pro_list_wrap')
            
            for info in listing:
                link = info.find('a', class_='prdct_lnk').get('href')
                more_info = 'https://www.idp.com' + link
                schools = info.find('div', class_='ins_cnt')
                school = schools.a.text.strip()
                country = schools.p.text.strip().split(',')[-1].strip()
                level = info.find('div', class_='media_txt').text.strip().split('Qualification')[-1].strip()
                deadline_element = info.find('div', class_='media_btm') 
                
                if deadline_element is not None:
                    deadline = deadline_element.text.strip()
                else:
                    deadline = None 
                    
                allowed_chars = ''.join((string.ascii_letters, string.digits))
                slug_combine = school + " " + ''.join(random.choice(allowed_chars) for _ in range(32))
                slug = slugify(slug_combine)
                
                
                # Create an object to store the scraped data
                obj = {
                    'more_info': more_info,
                    'school': school,
                    'country': country,
                    'level': level,
                    'deadline': deadline,
                    'slug': slug
                }
                
                results.append(obj)
    
                if add_to_model:
                    country_instance, created = Country.objects.get_or_create(name = country)
                    if created:
                        country_instance.name = country
                        country_instance.save()
                    model_instance = Scholarship(
                        more_info=more_info,
                        school=school,
                        country=country,
                        level=level,
                        deadline=deadline,
                        slug=slug
                    )
                    
                    model_instance.save()
                    
    if add_to_model:
        return JsonResponse({'message': 'Scrapping complete'})
    else:
        return JsonResponse({'message': 'Failed'})

# LIST SCHOLARSHIP
def list_scholarship(request):
    scholarships_lists = Scholarship.objects.all().order_by('?')
    country_lists = Country.objects.all()
    level_lists = Level.objects.all()
    
    # set up pagination
    p = Paginator(scholarships_lists.all(), 5)
    page = request.GET.get('page')
    scholarships = p.get_page(page)
    return render(request,'category/category.html',{'scholarships_lists': scholarships_lists,
    'scholarships': scholarships, 'country_lists': country_lists,'level_lists':level_lists})

# CREATE COMMENT
@login_required(login_url='login')
def create_comment(request, slug):
    scholarship = get_object_or_404(Scholarship, slug = slug)
    template_name = "category/scholarship_detail.html"
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.user = request.user
            new_comment.scholarship = scholarship
            new_comment.active = True
            new_comment.save()
            return redirect('scholarship_detail', slug=slug)
    else:
        form = CommentForm()
    
    context = {'comment_form': form}
    return render(request, template_name, context)

# CREATE REPLY
@login_required(login_url='login')
def create_reply(request, comment_id):
    comment = Comment.objects.get(id=comment_id)
    
    if request.method == 'POST':
        form = ReplyForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.user = request.user
            reply.comment = comment
            reply.active = True
            reply.save()
            return redirect('scholarship_detail', slug=comment.scholarship.slug)
    else:
        form = ReplyForm()
    context = {'reply_form':form}
    return render(request, 'category/scholarship_detail.html', context)

# SCHOLARSHIP DETAIL
def scholarship_detail(request,slug):
    scholarship = get_object_or_404(Scholarship, slug= slug)
    template_name = "category/scholarship_detail.html"
    comments = Comment.objects.filter(
        scholarship = scholarship,
        active=True)
    for comment in comments:
        replies = comment.reply_set.all()
        comment.replies = replies
    comment_form = CommentForm()
    reply_form = ReplyForm()
    favorited = False
    try:
        if request.user.is_authenticated:
            favorite = FavoriteScholarship.objects.get(scholarship_link=slug, user=request.user)
            favorited = True
    except FavoriteScholarship.DoesNotExist:
        pass
    context = {'reply_form':reply_form, 
               'comment_form':comment_form, 
               'comments':comments,
               'object':scholarship,
               'favorited':favorited}
    return render(request,template_name, context)

# SCHOLARSHIP CREATE 
def create_scholarship(request):
    if request.method == 'POST':
        form = ScholarshipForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(request.META['HTTP_REFERER']) 
    else:
        form = ScholarshipForm()
    return render(request, 'category/create_scholarship.html', {'form': form})

def update_scholarship(request, slug):
    scholarship = get_object_or_404(Scholarship, slug=slug)
    if request.method == 'POST':
        form = ScholarshipForm(request.POST, instance=scholarship)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(request.META['HTTP_REFERER']) 
    else:
        form = ScholarshipForm(instance=scholarship)
    return render(request, 'category/update_scholarship.html', {'form': form})
# # SCHOLARSHIP EDIT
# def scholarship_edit(request, slug):
#     scholarship = get_object_or_404(Scholarship,slug=slug)
#     if request.method == 'POST':
#         form = EditScholarshipForm(request.POST) 
#         request_edit_form = RequestScholarshipEditForm(request.POST)
#         if form.is_valid():
#             scholarship = form.save(commit=False)
#             edit_request = request_edit_form.save(commit=False)
#             edit_request.user = request.user
#             edit_request.scholarship = 
#             scholarship.save()
#             return redirect('profile')
#     else:
#         form = EditScholarshipForm() 
#         request_edit_form =RequestScholarshipEditForm()
#     context = {
#         'scholarship_form': form,
#         'request_edit_form':request_edit_form
#     }
#     return render(request, 'user/profile_edit.html', context)



# SHOW ALL COMMENT & REPLY
def comment_reply_list(request):
    comment_list = Comment.objects.filter(user = request.user)
    reply_list = Reply.objects.filter(user = request.user)
    context = {'reply_list':reply_list,
               'comment_list':comment_list}
    return render(request,'user/favorite.html',context)

from django.http import HttpResponseRedirect

def delete_comment(request, slug):
    try:
        scholarship = get_object_or_404(Scholarship, slug = slug)
        comment = get_object_or_404(Comment, scholarship = scholarship)
        comment.delete()
        message ='Comment Deleted'
    except:
        message ='Failed'
    return redirect('scholarship_detail', slug=comment.scholarship.slug)

def delete_reply(request, comment_id):
    try:
        comment = get_object_or_404(Comment, id = comment_id)
        reply = get_object_or_404(Reply, comment = comment)
        reply.delete()
    except:
        message='Failed'
    return redirect('scholarship_detail', slug=comment.scholarship.slug)

# FAVORITE view
# ADD TO FAVORITE
@login_required(login_url='login')
def add_to_favorite(request, slug):
    scholarship_get = get_object_or_404(Scholarship, slug=slug)
    try:
        created= FavoriteScholarship.objects.get_or_create(user=request.user, scholarship_school=scholarship_get.school, scholarship_link = scholarship_get.slug)
        if created:
            return HttpResponseRedirect(request.META['HTTP_REFERER']) 
        else:
            return HttpResponseRedirect(request.META['HTTP_REFERER']) 
    except IntegrityError:
        return redirect('home')

# SHOW ALL FAVORITE
def favorite_list(request):
    scholarship_favorite = FavoriteScholarship.objects.filter(user=request.user)
    return render(request,'user/favorite.html',{'scholarship_favorite':scholarship_favorite})

# DELETE FAVORITE
def favorite_delete(request, slug):
    try:
        favorite = get_object_or_404(FavoriteScholarship, scholarship_link=slug)
        favorite.delete()
    except:
        messages.info(request, 'Failed')
    return HttpResponseRedirect(request.META['HTTP_REFERER']) 
# ---------end of favorite view


# SEARCH USING COUNTRY TAG
def search_tag(request, country):
    scholarships_lists = Scholarship.objects.filter(country=country)
    country_lists = Country.objects.all()
    level_lists = Level.objects.all()
    p = Paginator(scholarships_lists, 5)
    page = request.GET.get('page')
    scholarships = p.get_page(page)
    context = {'scholarships':scholarships, 
               'country':country, 
               'country_lists':country_lists,
               'scholarships_lists':scholarships_lists,
               'level_lists':level_lists}
    return render(request,'category/scholarship_tag_result.html', context)

def search_tag_custom(request, type,category):
    if type == 'country':
        scholarships_lists = Scholarship.objects.filter(country__contains=category)
        lists = Country.objects.all()
    else:
        scholarships_lists = Scholarship.objects.filter(level__contains= category)
        lists = Level.objects.all()
    
    p = Paginator(scholarships_lists, 5)
    page = request.GET.get('page')
    scholarships = p.get_page(page)
    if type == 'country':
        context = {'scholarships':scholarships, 
                'country':category, 
                'country_lists':lists,
                'scholarships_lists':scholarships_lists }
    else:
        context = {'scholarships':scholarships, 
                'country':category, 
                'level_lists':lists,
                'scholarships_lists':scholarships_lists }
    return render(request,'category/scholarship_tag_result.html', context)


