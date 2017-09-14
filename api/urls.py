from django.conf.urls import patterns, include, url

from .views import getUsers, getCallSummary, getActionItems, createActionItem

urlpatterns = patterns('',
    url(r'^getUsers/?$', getUsers.as_view()),
    url(r'^getCallSummary/?$', getCallSummary.as_view()),
    url(r'^getActionItems/?$', getActionItems.as_view()),
    url(r'^getActionItems/is_complete=(?P<is_complete>\w+)/?$', getActionItems.as_view()),
    url(r'^createActionItem/?$', createActionItem.as_view()),

    url(r'^resolveeActionItem/?$', getUsers.as_view()),
    url(r'^getTickets/?$', getUsers.as_view()),
    url(r'^getTicketDetailByID/?$', getUsers.as_view()),
    url(r'^getCustomerByID/?$', getUsers.as_view()),
    url(r'^addTicket/?$', getUsers.as_view()),
    url(r'^updateTicketStatus/?$', getUsers.as_view()),
    url(r'^addNoteToTIcket/?$', getUsers.as_view()),
)
