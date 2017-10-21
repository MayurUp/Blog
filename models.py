from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse
from django.db.models.signals import pre_save
from django.utils.text import slugify
from django.utils import timezone
from django.contrib.auth.models import User
# Create your models here.

#Post.objects.all()
#Post.objects.create(user=user, title="Some time")

class Category(models.Model):
	name = models.CharField(max_length=500)
	slug = models.SlugField(unique=True)

class Meta:
		ordering = ('name')
		verbose_name = 'category'
		verbose_name_plural = 'categories'

def __str__(self):
	return self.name

def __unicode__(self):
	return self.name

class PostManager(models.Manager):
	def active(self, *argr, **kwargs ):
		#Post.objects.all() = super(PostManager, self).all()
		return super(PostManager, self).filter(draft=False).filter(publish__lte=timezone.now())


def upload_location(instance, filename):
	return "%s/%s" %(instance.id, filename)

class Post(models.Model):
	category = models.ForeignKey(Category)
	user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
	image = models.ImageField(upload_to=upload_location, null=True, blank=True)
	slug = models.SlugField(unique=True)
	#height_Field = models.IntegerField(default=0)
	#width_Field = models.IntegerField(default=0)
	title = models.CharField(max_length=500)
	content = models.TextField()
	seo_title = models.CharField(max_length=250)
	seo_discription = models.CharField(max_length=160)

	updated = models.DateTimeField(auto_now=True, auto_now_add=False)
	timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
	draft = models.BooleanField(default=True)
	publish = models.DateTimeField(auto_now=False, auto_now_add=True)

	objects = PostManager()

	def __unicode__(self):
		return self.title

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse("posts:detail", kwargs={"slug": self.slug})
		#return "/posts/%s/" %(self.id)

	class Meta:
		ordering = ["-timestamp", "-updated"]



def create_slug(instance, new_slug=None):
	slug = slugify(instance.title)
	if new_slug is not None:
		qs - Post.objects.filter(slug=slug).order_by("-id")
		exits = qs.exits()
		if exits:
			new_slug = '%s-%s' %(slug, qs.first().id)
			return create_slug(instance, new_slug=new_slug)
		return slug

def pre_save_post_receiver(sender, instance, *args, **kwargs):

	if not instance.slug:
		instance.slug = create_slug(instance)

	'''slug = slugify(instance.title)
	exits = Post.objects.filter(slug=slug).exits()
	if exits:
		slug = "%s-%s" %(slugify(instance.title), instance.id)

	instance.slug = slug'''

pre_save.connect(pre_save_post_receiver, sender=Post)