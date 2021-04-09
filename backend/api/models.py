from django.db import models

class File(models.Model):
	id = models.AutoField(primary_key= True)
	b64 = models.TextField(blank=False, null=False)
	lastedit = models.DateTimeField(auto_now= True)
	image_class = models.TextField(blank = True, default = "")
	labels = models.TextField(blank = True, default= "")
	def __str__(self):
		return f"Image no.: {self.id}"
