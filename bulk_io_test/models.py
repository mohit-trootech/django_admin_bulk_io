from django_extensions.db.models import (
    TitleDescriptionModel,
    TimeStampedModel,
    ActivatorModel,
)


class Comment(TitleDescriptionModel, TimeStampedModel, ActivatorModel):

    def __str__(self):
        return self.title
