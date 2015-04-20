from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify

    
class UserProfile(models.Model):
   
    user = models.OneToOneField(User)
    picture = models.ImageField(upload_to='profile_images', blank=True, default='profile_images/default.png')
    slug = models.SlugField(unique=True)
    def save(self, *args, **kwargs):
                super(UserProfile, self).save(*args, **kwargs)
                self.slug = slugify(self.user.username)
                super(UserProfile, self).save(*args, **kwargs)
    
    def __unicode__(self):
        return self.user.username
    
    
class Problem(models.Model):
    title = models.CharField (max_length = 30)
    place = models.CharField (max_length = 30)
    desc = models.CharField (max_length = 300)
    tags = models.CharField (max_length = 50)
    status = models.CharField (max_length = 10)
    rq_ppl =models.IntegerField (default = 1)
    pub_date = models.DateTimeField('date published')
    deadline= models.DateTimeField(blank = True, null=True)
    user = models.ForeignKey(User, null = True)
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
    status = models.CharField (max_length = 10)
    slug = models.SlugField(unique=True)
    
    def save(self, *args, **kwargs):
                super(Solution, self).save(*args, **kwargs)
                self.slug = slugify(self.id)
                super(Solution, self).save(*args, **kwargs)

class Ignore(models.Model):
    user_id = models.ForeignKey(User, related_name ='user_id')
    ref_user_id = models.ForeignKey(User, related_name ='ref_user_id')

    
    