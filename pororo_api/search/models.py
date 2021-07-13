from django.db import models


class Collection(models.Model):
    collection = models.CharField(blank=False, null=False, max_length=30)

    def __str__(self):
        return self.collection.name