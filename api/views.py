from django.http import HttpResponse
from django.core import serializers

from simple_rest import Resource

from .models import Customer, Ticket, Note, ActionItem, Users 
from simple_rest.response import RESTfulResponse

# TODO - @admin_required
class getUsers(Resource):

    @RESTfulResponse()
    def get(self, request, contact_id=None, **kwargs):
        return Users.objects.all()

    def post(self, request, *args, **kwargs):
        Contact.objects.create(
            fname=request.POST.get('fname'),
            lname=request.POST.get('lname'),
            phone_number=request.POST.get('phone_number'))
        return HttpResponse(status=201)

    def delete(self, request, contact_id):
        contact = Contact.objects.get(pk=contact_id)
        contact.delete()
        return HttpResponse(status=200)
