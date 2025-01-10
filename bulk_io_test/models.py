from django_extensions.db.models import (
    TitleDescriptionModel,
    TimeStampedModel,
    ActivatorModel,
)


class Comment(TitleDescriptionModel, TimeStampedModel, ActivatorModel):

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Comment"
        verbose_name_plural = "Comments"
