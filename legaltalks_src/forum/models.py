from django.db import models
from django.utils import timezone
from account.models import (
    Account,
    UserProfile
)
from django.template.defaultfilters import slugify
from django.urls import reverse

class Question(models.Model):
    BUSINESS_LAW            = 'Bu'
    CIVIL_LAW               = 'Ci'
    CONSTITUTIONAL_LAW      = 'Co'
    CONSUMER_LAW            = 'Cn'
    CRIMINAL_LAW            = 'Cr'
    FAMILY_LAW              = 'Fa'
    INTELLECTUAL_PROPERTY   = 'In'
    LABOUR                  = 'La'
    PROPERTY_LAW            = 'Pr'
    TAXATION                = 'Ta'

    CATEGORY_CHOICES = [
        (BUSINESS_LAW          , 'Business Law'          ),
        (CIVIL_LAW             , 'Civil Law'             ),
        (CONSTITUTIONAL_LAW    , 'Constitutional Law'    ),
        (CONSUMER_LAW          , 'Consumer Law'          ),
        (CRIMINAL_LAW          , 'Criminal Law'          ),
        (FAMILY_LAW            , 'Family Law'            ),
        (INTELLECTUAL_PROPERTY , 'Intellectual Property' ),
        (LABOUR                , 'Labour'                ),
        (PROPERTY_LAW          , 'Property Law'          ),
        (TAXATION              , 'Taxation'              ),
    ]

    question_title   = models.CharField(max_length=150) # by form
    question_body    = models.TextField() # by form
    is_anonymous     = models.BooleanField(default=False) # by form
    
    category = models.CharField( # by form
        max_length = 2, 
        choices = CATEGORY_CHOICES
    )

    author          = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='questions')
    upvotes         = models.ManyToManyField(Account, related_name='q_upvoters', blank=True)
    downvotes       = models.ManyToManyField(Account, related_name='q_downvoters', blank=True)
    date_asked      = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-date_asked']

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        return self
    def get_absolute_url(self):
        return reverse('forum:question-detail', kwargs={'question_id': self.pk})
    def answer_count(self):
        return len(self.answer_set.all())
    def votes(self):
        return len(self.upvotes.all()) - len(self.downvotes.all())

class Answer(models.Model):
    answer_for      = models.ForeignKey(Question, on_delete=models.CASCADE) # Override Save for form
    date_answered   = models.DateTimeField(default=timezone.now)
    answer_body     = models.TextField() # by form
    upvotes         = models.ManyToManyField(Account, related_name='a_upvoters', blank=True)
    downvotes       = models.ManyToManyField(Account, related_name='a_downvoters', blank=True)
    is_anonymous    = models.BooleanField(default=False) # by form
    answerer        = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='answers') # Override Save for form
    def votes(self):
        return len(self.upvotes.all()) - len(self.downvotes.all())