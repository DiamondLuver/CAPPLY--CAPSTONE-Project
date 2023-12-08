from django.shortcuts import render
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import render, redirect
from django.contrib.auth.forms import SetPasswordForm
from .forms import EditUserForm, EditProfileForm
from django.http import HttpResponse, HttpResponseRedirect
from .forms import CVForm,ModeratorRequestForm
from django.template.loader import render_to_string
from django.core.files.storage import FileSystemStorage
from xhtml2pdf import pisa
from django.contrib import messages

# EDIT PROFILE
def edit_profile(request):
    if request.method == 'POST':
        form = EditUserForm(request.POST, instance=request.user) 
        profile_form = EditProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid() and profile_form.is_valid():
            user = form.save()
            profile_form.save()
            update_session_auth_hash(request, user)
            return redirect('profile')
    else:
        form = EditUserForm(instance=request.user)
        profile_form =EditProfileForm(instance=request.user.profile)
    context = {
        'form': form,
        'profile_form':profile_form
    }
    return render(request, 'user/profile_edit.html', context)

# CHANGE PASSWORD
def change_password(request):
    if request.method == 'POST':
        password_form = SetPasswordForm(user=request.user, data=request.POST)
        
        if password_form.is_valid():
            password_form.save()
            update_session_auth_hash(request, request.user)
            return redirect('profile')
    else:
        password_form = SetPasswordForm(user=request.user)
    
    context = {
        'password_form': password_form,
    }
    return render(request, 'user/change_password.html', context)


from django.template.loader import get_template
import weasyprint
from PIL import Image
import os
from django.conf import settings

# CREATE CV TO PDF
def generate_cv_pdf(request):

    if request.method == 'POST':
        form = CVForm(request.POST, request.FILES)
        if form.is_valid():
                        
            full_name = form.cleaned_data['full_name']
            email = form.cleaned_data['email']
            phone_number = form.cleaned_data['phone_number']
            address = form.cleaned_data['address']
            summary = form.cleaned_data['summary']
            institution_name = form.cleaned_data['institution_name']
            degree_earned = form.cleaned_data['degree_earned']
            field_of_study = form.cleaned_data['field_of_study']
            dates_of_attendance = form.cleaned_data['dates_of_attendance']
            company_name = form.cleaned_data['company_name']
            job_title = form.cleaned_data['job_title']
            employment_dates = form.cleaned_data['employment_dates']
            responsibilities = form.cleaned_data['responsibilities']
            achievements = form.cleaned_data['achievements']
            
            skills = form.cleaned_data['skills']
            certifications = form.cleaned_data['certifications']
            
            project_name = form.cleaned_data['project_name']
            purpose = form.cleaned_data['purpose']
            role = form.cleaned_data['role']
            technologies_used = form.cleaned_data['technologies_used']
            
            awards = form.cleaned_data['awards']
            languages = form.cleaned_data['languages']
            interests = form.cleaned_data['interests']
            references = form.cleaned_data['references']
            image_file = form.cleaned_data['image_file']

            fss = FileSystemStorage()
            file = fss.save(image_file.name, image_file)
            image_url = fss.url(file)

            image_url_with_scheme = f"{request.scheme}://{request.get_host()}{image_url}"
            
            
            # img = Image.open('media/'+image_file.name)
            # left = 100
            # top = 100
            # right = 400
            # bottom = 400
            # cropped_image = img.crop((left, top, right, bottom))
            # cropped_file_path = os.path.join(settings.MEDIA_ROOT, 'cropped_image.jpg')

            # cropped_image.save(cropped_file_path)

            
            context = {
                'full_name': full_name,
                'email': email,
                'phone_number': phone_number,
                'address': address,
                'summary': summary,
                'institution_name': institution_name,
                'degree_earned': degree_earned,
                'field_of_study': field_of_study,
                'dates_of_attendance': dates_of_attendance,
                'company_name': company_name,
                'job_title': job_title,
                'employment_dates': employment_dates,
                'responsibilities': responsibilities,
                'achievements': achievements,
                'skills': skills,
                'certifications': certifications,
                'project_name': project_name,
                'purpose': purpose,
                'role': role,
                'technologies_used': technologies_used,
                'awards': awards,
                'languages': languages,
                'interests': interests,
                'references': references,
                'image_url': image_url_with_scheme
            }
            # img = Image.open(image_url_with_scheme)
            # left = 100
            # top = 100
            # right = 400
            # bottom = 400
            # cropped_image = img.crop((left, top, right, bottom))
            # cropped_image.save(cropped_file_path)


            template = get_template('cv/cv_template.html')
            html = template.render(context)
            
            pdf = weasyprint.HTML(string=html).write_pdf(stylesheets=[weasyprint.CSS(string='@page { margin: 0;page-break-after: always; margin-top:10mm;  }')])

            
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="form_submission.pdf"'
            response.write(pdf)
            # html_string = render_to_string('cv/cv_template.html', context)

            # response = HttpResponse(content_type='application/pdf')
            # response['Content-Disposition'] = 'attachment; filename="form_submission.pdf"'

            # pisa.CreatePDF(html_string, dest=response)
            return response
        else:
            form = CVForm()
    else:
        form = CVForm()

    return render(request, 'cv/cv_form.html', {'form': form})

from django.shortcuts import render, redirect
from .forms import CreateUserForm
from django.contrib.auth.models import User

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import CreateUserForm
from django.contrib.auth.models import User, auth




# MODERATOR REQUEST
def moderator_request_view(request):
    if request.method == 'POST':
        form = ModeratorRequestForm(request.POST)
        if form.is_valid():
            moderator_request = form.save(commit=False)
            moderator_request.user = request.user
            moderator_request.save()
            messages.success(request, 'Your request has been submitted successfully.')
            return HttpResponseRedirect(request.META['HTTP_REFERER']) 
    else:
        form = ModeratorRequestForm()
    
    return render(request, 'user/moderator_request.html', {'form': form, 'message':messages})