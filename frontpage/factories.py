from django.contrib.auth.models import Group, User
from django.utils.timezone import now
from factory.declarations import LazyAttribute, LazyFunction, Sequence
from factory.django import DjangoModelFactory
from factory.faker import Faker
from factory.helpers import post_generation


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    username = Sequence(lambda n: f"user{n}")
    first_name = Faker("first_name")
    last_name = Faker("last_name")
    email = LazyAttribute(lambda obj: "%s@example.com" % obj.username)
    is_staff = False
    is_superuser = False
    is_active = True
    date_joined = LazyFunction(now)

    @post_generation
    def password(self, create, extracted, **kwargs):
        if not create:
            return
        raw_password = extracted or "pass"
        self.set_password(raw_password)
        self.save()

    @post_generation
    def groups(self, create, extracted, **kwargs):
        if not create or not extracted:
            return

        self.groups.add(*extracted)


class AdminFactory(UserFactory):
    is_staff = True


class GroupFactory(DjangoModelFactory):
    class Meta:
        model = Group

    name = Sequence(lambda n: "Group #%s" % n)
