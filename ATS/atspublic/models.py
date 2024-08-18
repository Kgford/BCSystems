from django.db import models
from django.contrib.auth.models import User

 
# Create your models here.
#https://www.skysilk.com/blog/2017/how-to-make-a-blog-with-django/#:~:text=Django%20Blog%201%20Installing%20Django.%20First%20login%20to,small%20handful%20of%20its%20functionality%20in%20this%20example.
class Visitor(models.Model):
    visitor = models.CharField('visitor', max_length=50, blank=True)
    email = models.CharField('email',max_length=50, blank=True)
    session_id = models.CharField('session_id',max_length=100, blank=True)
    client_id = models.CharField('client_id',max_length=200, blank=True)
    user_agent = models.CharField('user_agent',max_length=200, blank=True)
    visitor_ip = models.CharField('visitor_ip',max_length=100, blank=True)
    visitor_blocked = models.BooleanField("visitor_blocked",unique=False,null=True,default=False)
    email_blocked = models.BooleanField("email_blocked",unique=False,null=True,default=False)
    session_id_blocked = models.BooleanField("session_id_blocked",unique=False,null=True,default=False)
    client_id_blocked = models.BooleanField("client_id_blocked",unique=False,null=True,default=False)
    user_agent_blocked = models.BooleanField("user_agent_blocked",unique=False,null=True,default=False)
    visitor_ip_blocked = models.BooleanField("visitor_ip_blocked",unique=False,null=True,default=False)
    blocked_reason = models.CharField('blocked_reason',max_length=200, blank=True)
    email_add = models.CharField('email_add',max_length=200, blank=True)
    created_on = models.DateField(null=True)
    last_entry = models.DateField(null=True)
    def __str__(self):
        return "%s %s" % (self.visitor, self.email)


class Blog(models.Model):
   title = models.CharField(max_length=100, unique=True)
   slug = models.SlugField(max_length=100, unique=True)
   body = models.TextField()
   posted = models.DateTimeField(db_index=True, auto_now_add=True)
   category = models.ForeignKey('Category',on_delete=models.CASCADE,)
   def __str__(self):
        return "%s %s" % (self.title, self.category)
   
   def __unicode__(self):
       return '%s' % self.title
 
  
   def get_absolute_url(self):
       return ('view_blog_post', None, { 'slug': self.slug })
 
class Category(models.Model):
   title = models.CharField(max_length=100, db_index=True)
   slug = models.SlugField(max_length=100, db_index=True)
 
   def __unicode__(self):
       return '%s' % self.title
 
  
   def get_absolute_url(self):
       return ('view_blog_category', None, { 'slug': self.slug })