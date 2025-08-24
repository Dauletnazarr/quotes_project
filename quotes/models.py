from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q, UniqueConstraint, F

class Source(models.Model):
    name = models.CharField(max_length=255, unique=True)
    type = models.CharField(
        max_length=50,
        choices=[('movie', 'Movie'), ('book', 'Book'), ('other', 'Other')],
        default='other'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

class Quote(models.Model):
    source = models.ForeignKey(Source, on_delete=models.CASCADE, related_name='quotes')
    text = models.TextField()
    text_normalized = models.TextField(editable=False)
    weight = models.PositiveIntegerField(default=1)
    views = models.PositiveIntegerField(default=0)
    likes = models.PositiveIntegerField(default=0)
    dislikes = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            UniqueConstraint(fields=['source', 'text_normalized'], name='uq_quote_source_textnorm'),
        ]

    def clean(self):
        self.text_normalized = ' '.join((self.text or '').lower().split())
        if self.weight < 1:
            raise ValidationError({'weight': 'Вес должен быть >= 1.'})
        if self.is_active and self.source_id:
            qs = Quote.objects.filter(source=self.source, is_active=True)
            if self.pk:
                qs = qs.exclude(pk=self.pk)
            if qs.count() >= 3:
                raise ValidationError('У источника уже есть 3 активные цитаты.')

    def save(self, *args, **kwargs):
        self.text_normalized = ' '.join((self.text or '').lower().split())
        super().save(*args, **kwargs)

    def __str__(self):
        return f'[{self.source}] {self.text[:60]}…'

class ViewEvent(models.Model):
    quote = models.ForeignKey(Quote, on_delete=models.CASCADE, related_name='view_events')
    session_key = models.CharField(max_length=40, blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)

class Vote(models.Model):
    LIKE = 1
    DISLIKE = -1
    VALUE_CHOICES = [(LIKE, 'Like'), (DISLIKE, 'Dislike')]

    quote = models.ForeignKey(Quote, on_delete=models.CASCADE, related_name='votes')
    session_key = models.CharField(max_length=40)
    value = models.SmallIntegerField(choices=VALUE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            UniqueConstraint(fields=['quote', 'session_key'], name='uq_vote_once_per_session_per_quote')
        ]
