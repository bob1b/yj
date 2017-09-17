from django.conf.urls import patterns, include, url

from .views import getUsers, getCallSummary, getActionItems, createActionItem, resolveActionItem
from .views import getTickets, getTicketDetailByID, getCustomerByID, addTicket, updateTicketStatus
from .views import addNoteToTicket, do_login, do_logout

urlpatterns = patterns('',
    url(r'^login/?$', do_login.as_view()),
    url(r'^logout/?$', do_logout.as_view()),
    url(r'^getUsers/?$', getUsers.as_view()),
    url(r'^getCallSummary/?$', getCallSummary.as_view()),
    url(r'^getActionItems/?$', getActionItems.as_view()),
    url(r'^getActionItems/?$', getActionItems.as_view()),
    url(r'^createActionItem/?$', createActionItem.as_view()),
    url(r'^resolveActionItem/(?P<id>\d+)/?$', resolveActionItem.as_view()),
    url(r'^getTickets/?$', getTickets.as_view()),
    url(r'^getTicketDetailByID/(?P<id>[\d]+)?$', getTicketDetailByID.as_view()),
    url(r'^getCustomerByID/(?P<id>[\d]+)?$', getCustomerByID.as_view()),
    url(r'^addTicket/?$', addTicket.as_view()),
    url(r'^updateTicketStatus/(?P<id>[\d]+)/(?P<new_status>[\w]+)?$', updateTicketStatus.as_view()),
    url(r'^addNoteToTicket/?$', addNoteToTicket.as_view()),
)
