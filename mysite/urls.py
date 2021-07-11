from django.urls import path, include
from django.contrib import admin
from . import views

# Django Admin header Customization
from .views import SearchView
admin.site.site_header = "Login for admin dashboard"
apps_name = 'mysite'

urlpatterns = [
    path('', views.index, name="index"),
    path("login.html", views.login, name="login"),
    path("register.html", views.register, name="register"),
    path("logout.html", views.logout, name="logout"),
    path("about.html", views.about, name="about"),
    path("job-listings.html", views.job_listings, name="job-listings"),
    path("job-single/<int:id>/", views.job_single, name="job_single"),
    path("post-job.html", views.post_job, name="post-job"),
    path("contact.html", views.contact, name="contact"),
    path("applyjob/<int:id>/", views.applyjob, name="applyjob"),
    path("ranking/<int:id>/", views.ranking, name="ranking"),
    path('search/', SearchView.as_view(), name='search'),

]
