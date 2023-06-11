from django.db import models
from django.urls import reverse
from django.conf import settings
from django.utils import timezone


# Create your models here.
class Contact(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=111, default="")
    phone = models.CharField(max_length=12, default="")
    subject = models.TextField(max_length=100)
    desc = models.TextField(max_length=300)

    def __str__(self):
        return self.name + " - " + self.email


JOB_TYPE = (
    ('Part Time', 'Part Time'),
    ('Full Time', 'Full Time'),
    ('Freelance', 'Freelancer'),
)

CATEGORY = (
    ('Web Design', 'Web Design'),
    ('Graphic Design', 'Graphic Design'),
    ('Web Developing', 'Web Developing'),
    ('Software Engineering', 'Software Engineering'),
    ('HR', 'HR'),
    ('Marketing', 'Marketing'),
)

GENDER = (
    ('Male', 'Male'),
    ('Female', 'Female'),
    ('Both', 'Both'),
)

CANDIDATE_GENDER = (
    ('Male', 'Male'),
    ('Female', 'Female'),
)


# For post a job
class PostJob(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                             null=True, editable=False, blank=True)
    title = models.CharField(max_length=100)
    company_name = models.CharField(max_length=200)
    employment_status = models.CharField(choices=JOB_TYPE, max_length=10)
    vacancy = models.CharField(max_length=10, null=True)
    gender = models.CharField(choices=GENDER, max_length=30, null=True)
    details = models.TextField()
    responsibilities = models.TextField()
    experience = models.CharField(max_length=100)
    other_benefits = models.CharField(max_length=100)
    job_location = models.CharField(max_length=120)
    salary = models.CharField(max_length=20, null=True, blank=True)
    # image = models.ImageField(blank=True, upload_to='media', null=True)
    application_deadline = models.DateTimeField(null=True, blank=True)

    # published_on = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("mysite/job-single.html", args=[self.id])


class Apply_job(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    gender = models.CharField(choices=CANDIDATE_GENDER, max_length=30, default='Male')
    experience = models.FloatField(default=0.0)
    # portfolio = models.CharField(max_length=50)
    cv = models.FileField(default="")
    coverletter = models.CharField(max_length=100)
    company_name = models.CharField(max_length=100)
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.name
