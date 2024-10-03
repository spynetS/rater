from django.contrib.auth.forms import User
from django.db import models

from movies.models import Movie
from accounts.models import Account
from django.utils import timezone
from datetime import timedelta

# Create your models here.

class Rating(models.Model):
    look = models.IntegerField(null=True)
    script = models.IntegerField(null=True)
    acting = models.IntegerField(null=True)
    soundtrack = models.IntegerField(null=True)
    bonus = models.IntegerField(null=True)
    overalscore = models.IntegerField(null=True)
    description = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)  # Automatically set at creation

    movie = models.ForeignKey(Movie,on_delete=models.CASCADE,null=True)

    user = models.ForeignKey(User,on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        # Call the superclass's save method
        super().save(*args, **kwargs)

        # Check for existing ratings with null movie and older than 1 hour
        one_hour_ago = timezone.now() - timedelta(hours=1)
        Rating.objects.filter(movie__isnull=True, created_at__lt=one_hour_ago).delete()

    def average(self):
        # Create a list of all the fields
        fields = [self.look, self.script, self.acting, self.soundtrack, self.bonus, self.overalscore]
        # Filter out None values
        valid_scores = [score for score in fields if score is not None]

        # If there are no valid scores, return None to indicate no average can be computed
        if len(valid_scores) == 0:
            return None

        # Calculate the average of non-null scores
        return sum(valid_scores) / (len(valid_scores)-1) # we dont divide with the bonus
