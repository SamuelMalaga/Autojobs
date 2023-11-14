from django.db import models
from django.contrib.auth.models import User

class Job(models.Model):
    job_id = models.IntegerField(null=True)
    job_title = models.TextField(null=True)
    company_name = models.TextField(null=True)
    job_link = models.TextField()
    job_description = models.TextField(null=True)
    double_check = models.BooleanField(null=True)
    source = models.TextField(null=True)

    def __str__(self):
        return self.job_title


class WorkExperience(models.Model):
    # Opções para o campo 'exp_type'
    EXP_TYPE_CHOICES = [
        ('work', 'Work'),
        ('project', 'Project'),
        ('volunteer', 'Volunteer')
        # Adicione mais opções conforme necessário
    ]

    exp_type = models.CharField(max_length=10, choices=EXP_TYPE_CHOICES)
    exp_company = models.CharField(max_length=100)
    exp_description = models.TextField()
    exp_start_time = models.DateTimeField()
    exp_end_time = models.DateTimeField()
    exp_user = models.ForeignKey(User, on_delete=models.PROTECT, null=True)  # Chave estrangeira para o modelo User

    def __str__(self):
        return f"{self.exp_user} - {self.exp_company}"

class Education(models.Model):

    edu_institute = models.CharField(max_length=100)
    edu_description = models.TextField()
    edu_start_time = models.DateTimeField()
    edu_end_time = models.DateTimeField()
    edu_user = models.ForeignKey(User, on_delete=models.PROTECT, null=True)  # Chave estrangeira para o modelo User


class Language(models.Model):
    LNG_LEVEL_OPTIONS = [
        ('A1', 'A1 - Iniciante'),
        ('A2', 'A2 - Básico'),
        ('B1', 'B1 - Intermediario'),
        ('B2', 'B2 - Intermediário Avançado'),
        ('C1', 'C2 - Avançado'),
        ('C2', 'C2 - Fluente')
        # Adicione mais opções conforme necessário
    ]

    lng_name = models.CharField(max_length=100)
    lng_country = models.TextField()
    lng_proficiency_level = models.CharField(max_length=10, choices=LNG_LEVEL_OPTIONS)
    lng_user = models.ForeignKey(User, on_delete=models.PROTECT, null=True)


class Certification(models.Model):

    cert_name = models.CharField(max_length=200)
    cert_institute = models.CharField(max_length=100)
    cert_emmited_at = models.DateTimeField()
    cert_valid_until = models.DateTimeField()
    cert_user = models.ForeignKey(User, on_delete=models.PROTECT, null=True)

    def __str__(self):
        return f"{self.cert_user} - {self.cert_name}"

class Application(models.Model):
    APPL_STATUSES = [
        ('Screening', 'Triagem'),
        ('Interview', 'Entrevista'),
        ('Technical Interview', 'Entrevista técnica'),
        ('Inital interview', 'Entrevista inicial'),
        ('Techincal Assessment', 'Desafio técnico'),
        ('Proposal', 'Proposta'),
        ('Cancelled', 'Cancelada')
        # Adicione mais opções conforme necessário
    ]

    appl_status = models.CharField(max_length=20, choices=APPL_STATUSES)
    appl_closed_at = models.DateTimeField()
    appl_started_at = models.DateTimeField()
    appl_job = models.ForeignKey(Job, on_delete=models.PROTECT, null=True)
    appl_user = models.ForeignKey(User, on_delete=models.PROTECT)
    appl_resume = models.FileField(upload_to='media/uploads/', null=True, blank=True, default=None)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField()
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)








