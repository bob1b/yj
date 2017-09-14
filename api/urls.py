from django.conf.urls import patterns, include, url

from .views import getUsers

urlpatterns = patterns('',
    url(r'^getUsers/?$', getUsers.as_view()),
    url(r'^getCallSummary/?$', getUsers.as_view()),
    url(r'^getActionItems/?$', getUsers.as_view()),
    url(r'^createActionItem/?$', getUsers.as_view()),
    url(r'^resolveeActionItem/?$', getUsers.as_view()),
    url(r'^getTickets/?$', getUsers.as_view()),
    url(r'^getTicketDetailByID/?$', getUsers.as_view()),
    url(r'^getCustomerByID/?$', getUsers.as_view()),
    url(r'^addTicket/?$', getUsers.as_view()),
    url(r'^updateTicketStatus/?$', getUsers.as_view()),
    url(r'^addNoteToTIcket/?$', getUsers.as_view()),
)
