from django.db import models
import uuid
from users.models import Profile

class Project(models.Model):
    owner = models.ForeignKey(Profile, null=True,blank=True, on_delete=models.SET_NULL)#profile connected to project model
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)  # This means the field can be empty in the database, and null can be submitted
    featured_image = models.ImageField(null=True, blank=True ,default='default.jpg')
    demo_link = models.CharField(max_length=2000, null=True, blank=True)
    source_link = models.CharField(max_length=2000, null=True, blank=True)
    tags = models.ManyToManyField('Tag', blank=True)
    vote_total = models.IntegerField(default=0 , null=True,blank=True) 
    vote_ratio = models.IntegerField(default=0 , null=True,blank=True) 
    created = models.DateField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)  # Primary key

    def __str__(self):
            return self.title ##for showing the string value and project whould be show by name
    #order of project   
    class Meta:
          ordering = ['-vote_ratio','-vote_total','title']
    #revier list
    @property
    def reviewers(self):
          queryset = self.review_set.all().values_list('owner__id', flat=True)#flat=True simple list of id
          return queryset      
    #vote count
    @property 
    def getVoteCount(self):
          reviews = self.review_set.all()
          upVotes = reviews.filter(value='up').count() 
          totalVotes = reviews.count()
          ratio = (upVotes/totalVotes)*100
          self.vote_ratio = ratio
          self.vote_total = totalVotes
          self.save()




##review table
class Review(models.Model):
     VOTE_TYPE = (
           ('up', 'Up Vote'),#(actual value , string version choice)
           ('down' , 'Down Vote')
     )
     owner = models.ForeignKey(Profile, on_delete=models.CASCADE ,null=True ,blank=True)
     project = models.ForeignKey(Project, on_delete=models.CASCADE) ## if project delete it will delete review to
     body = models.TextField(null=True, blank=True)
     value = models.CharField(max_length=200 ,choices=VOTE_TYPE)
     created = models.DateField(auto_now_add=True)
     id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)  # Primary key
     class Meta:
           unique_together = [['owner', 'project']] #so that owner cant do review its own project
     def __str__(self):
            return self.value

class  Tag(models.Model):
    name = models.CharField(max_length=200)
    created = models.DateField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)  # Primary key
    def __str__(self):
            return self.name