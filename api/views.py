from django.http import HttpResponse
from django.core import serializers

from simple_rest import Resource

from .models import Customer, Ticket, Note, ActionItem, Users 
from simple_rest.response import RESTfulResponse

# TODO - @admin_required
class getUsers(Resource):

    @RESTfulResponse()
    def get(self, request, **kwargs):
        return Users.objects.all()


class getCallSummary(Resource):

    @RESTfulResponse()
    def get(self, request, **kwargs):
        summ = {'pending':-1, 'ready for approval':-1, 'resolved':-1, 'reopened':-1}
        for idx, status in enumerate(summ):
            summ[status] = len(Ticket.objects.filter(status=status))
        return summ


class getActionItems(Resource):

    @RESTfulResponse()
    def get(self, request, contact_id=None, **kwargs):
        return Users.objects.all()
