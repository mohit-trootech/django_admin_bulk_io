from django_extensions.db.models import (
    TitleDescriptionModel,
    TimeStampedModel,
    ActivatorModel,
)
from django.db.models import (
    Model,
    IntegerField,
    DateField,
    ForeignKey,
    ManyToManyField,
    CASCADE,
)


class Comment(TitleDescriptionModel, TimeStampedModel, ActivatorModel):
    created = DateField()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Comment"
        verbose_name_plural = "Comments"


class Like(Model):
    count = IntegerField(default=0)


class Post(TitleDescriptionModel):
    comment = ForeignKey(Comment, on_delete=CASCADE)
    likes = ManyToManyField("auth.User")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Post"
        verbose_name_plural = "Posts"
