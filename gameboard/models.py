from account.models import Account
from django.db import models
from time import time

def get_upload_file_name(instance, filename):
        return "uploaded_files/%s" % filename

# TODO: OneToOne may be better instead of using username
class SolverListModel(models.Model):
	username = models.CharField(max_length=30, null=False)
        problem_id = models.PositiveSmallIntegerField(null=False)
	breakthru_point = models.PositiveSmallIntegerField(default=0, null=False)

class Categories(models.Model):
        title = models.CharField(max_length=40, null=False)
	color = models.CharField(max_length=20, null=False)

class LogEntries(models.Model):
	account = models.ForeignKey(Account, null=True)
	description = models.CharField(max_length=100)
	time = models.DateTimeField(auto_now_add=True, auto_now=False)		

# It store CTF problem entry
class Entries(models.Model):
        # problem title
        title = models.CharField(max_length=50, null=False)

        # problem description
        description = models.TextField(null=False)

        # count solver
        solver_count = models.PositiveSmallIntegerField(default=0, null=True)

        # problem points
        point = models.PositiveSmallIntegerField(default=1, null=False)

        # problem answer it save md5 value of answer
        answer = models.CharField(max_length=32, null=False)

        # problem file
	problem_file = models.FileField(upload_to=get_upload_file_name)

        # It save problem solver, so we can know who solve this problem
        solver_list = models.ManyToManyField(SolverListModel)

        # Problem Type -> Reversing, System, Web, Network, Crypto ...
        category = models.ForeignKey(Categories)

	# Problem can be deactivated when CTF is over or other reasons ...
	is_active = models.BooleanField(default=True)
