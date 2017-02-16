from django.db import models


class Item(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.FileField(null=True,blank=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    created = models.DateTimeField(auto_now=False, auto_now_add=True)
    author = models.CharField(max_length=200, null=True)

def __str__(self):
    return '%s' % (self.title)


class Comment(models.Model):
    name = models.CharField(max_length=200)
    body = models.TextField()
    pub_date = models.DateTimeField('date published')
    itemz = models.ForeignKey(Item)

    def __str__(self):
        return '%s' % (self.name)
