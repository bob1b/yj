from django.conf.urls import patterns, include, url

from .views import Contacts

urlpatterns = patterns('',
    # Allow access to the contacts resource collection
    url(r'^contacts/?$', Contacts.as_view()),

    # Allow access to a single contact resource
    url(r'^contacts/(?P<contact_id>[0-9]+)/?$', Contacts.as_view()),
)
