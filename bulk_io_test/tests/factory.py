import factory


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "auth.User"

    username = factory.Faker("user_name")
    email = factory.Faker("email")
    password = factory.Faker("password")


class CommentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "bulk_io_test.Comment"

    title = factory.Faker("word")
    description = factory.Faker("sentence")
    created = factory.Faker("date")


class PostFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "bulk_io_test.Post"

    title = factory.Faker("word")
    description = factory.Faker("sentence")
    comment = factory.SubFactory(CommentFactory)

    @factory.post_generation
    def likes(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for topping in extracted:
                self.likes.add(topping)
