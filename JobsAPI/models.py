from django.db import models

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
