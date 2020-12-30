from django.db import models
from profiles.models import Profile

# Create your models here.

class Question(models.Model):
    question = models.CharField(max_length=500)
    pub_date = models.DateTimeField('date published')
    liked = models.ManyToManyField(Profile, blank=True, related_name='liker')
    voted_users = models.ManyToManyField(Profile, blank=True, related_name='voter')
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='polls', blank=True, null=True)
    value = models.BooleanField(default=False)

    def __str__(self):
        return self.question

    def num_likes(self):
        return self.liked.all().count()

    def num_comments(self):
        return self.comment_set.all().count()

    def num_votes(self):
        return self.voted_users.all().count()

    def voters_all(self):
        return self.voted_users.all()

    def num_choice(self):
        return self.choice_set.all().count()

    def question_votes(self):
        q_votes = 0
        for choice in self.choice_set.all():
            q_votes = q_votes + choice.votes
        return q_votes

    def get_results_dict(self):
        res = []
        q = self.question_votes()
        for choice in self.choice_set.all():
            d = {}
            d['text'] = choice.choice_text
            d['num_votes'] = choice.votes
            if not q:
                d['percentage'] = 0
            else:
                d['percentage'] = round((choice.votes / q * 100), 2)
            res.append(d)

        return res

    class Meta:
        ordering = ('-created',)


class Choice(models.Model):
    question_text = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200, null=True, blank=True)
    votes = models.IntegerField(default=0)
    value = models.BooleanField(default=False)

    def __str__(self):
        return self.choice_text


class Comment(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, blank=True, null=True, related_name='comuser')
    question_text = models.ForeignKey(Question, on_delete=models.CASCADE)
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.pk)


LIKE_CHOICES = (
    ('Like', 'Like'),
    ('Unlike', 'Unlike'),
)


class Likee(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='likeuser')
    question_text = models.ForeignKey(Question, on_delete=models.CASCADE)
    value = models.CharField(choices=LIKE_CHOICES, max_length=8)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user}-{self.question_text}-{self.value}"
