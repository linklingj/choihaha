from django.db import models
from django.contrib.auth.models import User
from PIL import Image

class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	avatar = models.ImageField(default='default.jpg', upload_to='profile_images')
	bio = models.TextField(max_length=500, blank=True)

	def __str__(self):
		return self.user.username

	# resizing images
	def save(self, *args, **kwargs):
		super().save()
	
		img = Image.open(self.avatar.path)
		if img.height > 150 or img.width > 150:
			new_img = (150, 150)
			img.thumbnail(new_img)
			img.save(self.avatar.path)
