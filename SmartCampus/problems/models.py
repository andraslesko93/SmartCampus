from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from datetime import datetime
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

class UserProfile(models.Model):
   
    user = models.OneToOneField(User)
    local_picture = models.ImageField(upload_to='profile_images', blank=True, default='profile_images/default.png')
    picture_url=models.URLField(blank=True)
    reputation = models.IntegerField(default=100)
    
    slug = models.SlugField(unique=True)
    def save(self, *args, **kwargs):
                super(UserProfile, self).save(*args, **kwargs)
                self.slug = slugify(self.user.username)+ "-" + str(self.id)
                super(UserProfile, self).save(*args, **kwargs)
    
    def __unicode__(self):
        return self.user.username
class Tag (models.Model):
    tag_text = models.CharField (max_length = 30)
    slug = models.SlugField(unique=False) 
    def save(self, *args, **kwargs):
                super(Tag, self).save(*args, **kwargs)
                self.slug = slugify(self.id)
                super(Tag, self).save(*args, **kwargs)
    def __unicode__(self):
        return u'%s' % (self.tag_text)     
class Problem(models.Model):
    title = models.CharField (max_length = 150)
    place = models.CharField (max_length = 50)
    desc = models.CharField (max_length = 2000)
    status = models.CharField (max_length = 11, default = "pending")
    rq_ppl =models.IntegerField (default = 1)
    added_at = models.DateTimeField('date published', default = datetime.now)
    bounty = models.IntegerField(default = 0, null=True)
    deadline= models.DateTimeField(blank = True, null=True)
    user = models.ForeignKey(User, null = True)
    tags = models.ManyToManyField(Tag, related_name='problems')
    slug = models.SlugField(unique=True)
    
    def save(self, *args, **kwargs):
                super(Problem, self).save(*args, **kwargs)
                self.slug = slugify(self.title) + "-" + str(self.id)
                super(Problem, self).save(*args, **kwargs)
    def __unicode__(self):
        return u'%s(%s)' % (self.title, self.place)
    
class Solution(models.Model):
    user_id = models.ForeignKey(User)
    problem_id = models.ForeignKey(Problem)
    desc = models.CharField (max_length = 300)
    served_ppl =models.IntegerField (default = 1)
    status = models.CharField (max_length = 10, default = "pending")
    added_at = models.DateTimeField (default = datetime.now)
    slug = models.SlugField(unique=True)
    def save(self, *args, **kwargs):
                super(Solution, self).save(*args, **kwargs)
                self.slug = slugify(self.id)
                super(Solution, self).save(*args, **kwargs)

class Ignore(models.Model):
    timestamp = models.DateTimeField (default = datetime.now)
    user_id = models.ForeignKey(User, related_name ='user_id')
    ref_user_id = models.ForeignKey(User, related_name ='ref_user_id')

class Rating (models.Model):
    user = models.ForeignKey(User)
    rated_user =  models.ForeignKey(User, related_name ='rated_user')
    type = models.CharField (max_length = 10)
    reputation = models.IntegerField(default = 0)
    granted_reputation = models.IntegerField(default = 0, null = True)
    bounty = models.IntegerField(default = 0)
    timestamp = models.DateTimeField (default = datetime.now)
    status = models.CharField (max_length = 10, default = "waiting")
    solution = models.ForeignKey(Solution, related_name = 'rating_solutions', null = True)

class Notification (models.Model):
    status = models.CharField (max_length = 10, default = "unchecked")
    timestamp = models.DateTimeField (default = datetime.now)
    user = models.ForeignKey(User)
    content_type = models.ForeignKey(ContentType, null=True, related_name = 'content_type')
    object_id = models.PositiveIntegerField(null=True)
    obj = GenericForeignKey("content_type", "object_id")
    
class Confidence_Problem (Problem):
    min_rq_reputation = models.IntegerField(default = 0)
    
    