from django.db import models


# Create your models here.
class Department(models.Model):
    department_id = models.CharField(max_length=30, primary_key=True)
    department_name = models.CharField(max_length=30)

    def __str__(self):
        return str(self.department_id)


class User(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(primary_key=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    designation = models.CharField(max_length=30)
    password = models.CharField(max_length=80)
    is_admin = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return str(self.name)


class Posts(models.Model):
    title = models.CharField(max_length=30)
    notice_text = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.title)
