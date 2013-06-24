import factory

from django.contrib.auth.models import User
from django.contrib.comments.models import Comment
from django.contrib.sites.models import Site

from organizations.models import Organization, OrganizationUser,\
    OrganizationOwner

from publicweb.models import Decision, Feedback


class UserFactory(factory.DjangoModelFactory):
    FACTORY_FOR = User

    # Have factoryboy add a sequenced number, n, to username for uniqueness
    username = factory.Sequence(lambda n: 'user%s' % n)

class OrganizationFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Organization

class OrganizationUserFactory(factory.DjangoModelFactory):
    FACTORY_FOR = OrganizationUser

    user = factory.SubFactory(UserFactory)
    organization = factory.SubFactory(OrganizationFactory)

class OrganizationOwnerFactory(factory.DjangoModelFactory):
    FACTORY_FOR = OrganizationOwner

    organization = factory.SubFactory(OrganizationFactory)
    organization_user = factory.SubFactory(
        OrganizationUserFactory,
        organization=factory.SelfAttribute('..organization')
    )

class DecisionFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Decision

    organization = factory.SubFactory(OrganizationFactory)

class FeedbackFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Feedback

    decision = factory.SubFactory(DecisionFactory)

class SiteFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Site

class CommentFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Comment
    site = factory.SubFactory(SiteFactory)
