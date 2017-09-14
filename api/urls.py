from django.conf.urls import patterns, include, url

from .views import Users

urlpatterns = patterns('',
    url(r'^getUsers/?$', Users.as_view()),
    url(r'^getCallSummary/?$', Users.as_view()),
    url(r'^getActionItems/?$', Users.as_view()),
    url(r'^createActionItem/?$', Users.as_view()),
    url(r'^resolveeActionItem/?$', Users.as_view()),
    url(r'^getTickets/?$', Users.as_view()),
    url(r'^getTicketDetailByID/?$', Users.as_view()),
    url(r'^getCustomerByID/?$', Users.as_view()),
    url(r'^addTicket/?$', Users.as_view()),
    url(r'^updateTicketStatus/?$', Users.as_view()),
    url(r'^addNoteToTIcket/?$', Users.as_view()),
)
