from django.db import models
from django.contrib.auth.models import User

class Job(models.Model):
    job_id = models.AutoField(primary_key=True)
    job_title = models.TextField(blank=True, null=True)
    company_name = models.TextField(blank=True, null=True)
    job_link = models.TextField(blank=True, null=True)
    job_description = models.TextField(blank=True, null=True)
    double_check = models.BooleanField(db_column='double_check', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'jobs'


    def __str__(self):
        return f"{self.job_title} - {self.job_id}"

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
    exp_user = models.ForeignKey(User, on_delete=models.CASCADE)  # Chave estrangeira para o modelo User

    def __str__(self):
        return self.exp_company

