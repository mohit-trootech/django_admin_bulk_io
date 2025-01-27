from django_extensions.db.models import (
    TitleDescriptionModel,
    TimeStampedModel,
    ActivatorModel,
)
from django.db.models import (
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


class Post(TitleDescriptionModel):
    comment = ForeignKey(Comment, on_delete=CASCADE)
    likes = ManyToManyField("auth.User")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Post"
        verbose_name_plural = "Posts"

    @property
    def like_count(self):
        return self.likes.count()
