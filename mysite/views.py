from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.core.files.storage import FileSystemStorage

from mysite import models
from mysite.models import Contact
from mysite.models import PostJob
from mysite.models import Apply_job

from django.contrib.auth.decorators import login_required



def index(request):
    return render(request, "mysite/index.html")


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return render(request, 'mysite/index.html')
        else:
            messages.info(request, 'Invalid Credentials')
            return redirect('login')
            # return redirect('/')

    else:
        return render(request, 'mysite/login.html')


def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        # phone = request.POST['phone']
        # address = request.POST['address']
        # linkedin_id = request.POST['linkedin_id']
        # github_id = request.POST['github_id']

        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'Username Already Taken!')
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'Email Taken!')
                return redirect('register')
            else:
                user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username,
                                                email=email, password=password1)
                user.save()
                messages.info(request, 'User Created!')
                return redirect('login')
        else:
            messages.info(request, 'Password is not matching!')
            return redirect('register')
        return redirect('/')

    else:
        return render(request, 'mysite/register.html')


def logout(request):
    auth.logout(request)
    return redirect('/')


def about(request):
    return render(request, 'mysite/about.html')


def job_single(request, id):
    job_query = PostJob.objects.get(id=id)
    context = {
        'q': job_query,
    }
    return render(request, "mysite/job-single.html", context)


def job_listings(request):
    all_jobs = PostJob.objects.all()
    context = {'job_listings': all_jobs}

    return render(request, "mysite/job-listings.html", context)


def post_job(request):
    if request.method == "POST":
        title = request.POST['title']
        company_name = request.POST['company_name']
        employment_status = request.POST['employment_status']
        vacancy = request.POST['vacancy']
        gender = request.POST['gender']
        if 'details' in request.POST:
            details = request.POST['details']
        else:
            details = False
        # details = request.POST.get['details', False]
        if 'responsibilities' in request.POST:
            responsibilities = request.POST['responsibilities']
        else:
            responsibilities = False
        # responsibilities = request.POST['responsibilities']
        experience = request.POST['experience']
        other_benefits = request.POST['other_benefits']
        job_location = request.POST['job_location']
        salary = request.POST['salary']
        application_deadline = request.POST['application_deadline']
        ins = PostJob(title=title, company_name=company_name, employment_status=employment_status, vacancy=vacancy, gender=gender, details=details,
                      responsibilities=responsibilities, experience=experience, other_benefits=other_benefits, job_location=job_location, salary=salary, application_deadline=application_deadline)
        ins.save()
        print("The data has been added into database!")
    return render(request, 'mysite/post-job.html')


def contact(request):
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        #phone = request.POST['phone']
        if 'phone' in request.POST:
            phone = request.POST['phone']
        else:
            phone = False

        if 'subject' in request.POST:
            subject = request.POST['subject']
        else:
            subject = False

        if 'desc' in request.POST:
            desc = request.POST['desc']
        else:
            desc = False

        #desc = request.POST['desc']
        #print(name, email, phone, subject, desc)
        ins = Contact(name=name, email=email, phone=phone, subject=subject, desc=desc)
        ins.save()
        print("Data has been save in database!")
    return render(request, "mysite/contact.html")


def applyjob(request):
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        portfolio = request.POST['portfolio']
        cv = request.FILES['cv']
        coverletter = request.POST['coverletter']

        # fs = FileSystemStorage
        # fs.save(cv.name, cv)

        ins = Apply_job(name=name, email=email, portfolio=portfolio, cv=cv, coverletter=coverletter)
        ins.save()
        print("The Data is saved into database!")
    return render(request, "mysite/applyjob.html")



# def fileUpload(request):
#     if request.method == 'POST':
#         uploaded_file = request.FILES['document']
