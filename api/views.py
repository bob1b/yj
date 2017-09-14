from django.http import HttpResponse
from django.core import serializers

from simple_rest import Resource

from .models import Customer, Ticket, Note, ActionItem, Users 


class Contacts(Resource):

    def get(self, request, contact_id=None, **kwargs):
        json_serializer = serializers.get_serializer('json')()
        if contact_id:
            contacts = json_serializer.serialize(Contact.objects.filter(pk=contact_id))
        else:
            contacts = json_serializer.serialize(Contact.objects.all())
        return HttpResponse(contacts, content_type='application/json', status=200)

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
