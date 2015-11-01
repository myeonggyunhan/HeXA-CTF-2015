from django.db import models

# Notice board entry
class NoticeEntries(models.Model):
	title = models.CharField(max_length=50, null=False)
	description = models.TextField(null=False)
