from django.conf.urls import patterns, include, url

from .views import getUsers, getCallSummary, getActionItems, createActionItem, resolveActionItem
from .views import getTickets

urlpatterns = patterns('',
    url(r'^getUsers/?$', getUsers.as_view()),
    url(r'^getCallSummary/?$', getCallSummary.as_view()),
    url(r'^getActionItems/?$', getActionItems.as_view()),
    url(r'^getActionItems/is_complete=(?P<is_complete>\w+)/?$', getActionItems.as_view()),
    url(r'^createActionItem/?$', createActionItem.as_view()),
    url(r'^resolveActionItem/id=(?P<id>\d+)/?$', resolveActionItem.as_view()),
    url(r'^getTickets/?$', getTickets.as_view()),
    url(r'^getTickets/dateRange=(?P<dateRange>[\w\d,-]+)?$', getTickets.as_view()),
    url(r'^getTickets/status=(?P<status>[\w\d,]+)?$', getTickets.as_view()),
    url(r'^getTickets/dateRange=(?P<dateRange>[\w\d,]+)/status=(?P<status>[\w\d,]+)?$', getTickets.as_view()),

    url(r'^getTicketDetailByID/?$', getUsers.as_view()),
    url(r'^getCustomerByID/?$', getUsers.as_view()),
    url(r'^addTicket/?$', getUsers.as_view()),
    url(r'^updateTicketStatus/?$', getUsers.as_view()),
    url(r'^addNoteToTIcket/?$', getUsers.as_view()),
)
