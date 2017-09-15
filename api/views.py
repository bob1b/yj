from django import forms
from django.forms.models import model_to_dict
from django.http import HttpResponse
from django.core import serializers
from simple_rest import Resource

from .models import Customer, Ticket, Note, ActionItem, Users 
from simple_rest.response import RESTfulResponse
import json
import pprint

# TODO - @admin_required on all calls
# TODO - login/logout calls
# TODO - pagination


class getUsers(Resource):
    """ Get Users (return id, name, email) """

    @RESTfulResponse()
    def get(self, request, **kwargs):
        return Users.objects.all()


class getCallSummary(Resource):
    """ Get Call Summary (returns number of calls at each status) """

    @RESTfulResponse()
    def get(self, request, **kwargs):
        summ = {'pending':-1, 'ready for approval':-1, 'resolved':-1, 'reopened':-1}
        for idx, status in enumerate(summ):
            summ[status] = len(Ticket.objects.filter(status=status))
        return summ


class getActionItems(Resource):
    """ Get Action Items for logged in user / status (returns a list of due date / description / is_complete for all action items associated with the user from the JWT token) - optionally can be filtered by is_complete=true or false """

    @RESTfulResponse()
    def get(self, request, is_complete=None, **kwargs):
        user_id = 1
        ai = None
        if is_complete is not None and is_complete.lower() == "true":
            ai = ActionItem.objects.filter(rep_id=user_id, is_complete=True)
        elif is_complete is not None and is_complete.lower() == "false":
            ai = ActionItem.objects.filter(rep_id=user_id, is_complete=False)
        else:
            ai = ActionItem.objects.filter(rep_id=user_id)
        return ai


class ActionItemForm(forms.ModelForm):
    class Meta:
        model = ActionItem
        fields = ['rep_id', 'description', 'due_date']

class createActionItem(Resource):
    """ Create Action Item (takes rep_id for whom the action item will be created, description, due date, autopopulates created_by with the id of the user on the JWT token """

    @RESTfulResponse()
    def post(self, request):
        form = ActionItemForm(request.POST)

        if not form.is_valid():
            return {"status":"Failure", "message":"Missing one or more form values"}

        # TODO - add created_by user value
        new_action_item = form.save(commit=False)
        new_action_item.created_by = 1
        new_action_item.save()
        return {"status":"Success", "message":"Action item has been added"}


class resolveActionItem(Resource):
    """ Resolve Action Item (takes item id, sets is_complete=true) """

    @RESTfulResponse()
    def get(self, request, id):
        # ensure record exists and is_complete = False
        records = ActionItem.objects.filter(id=id, is_complete=False)
        if len(records) == 0:
            return {"status":"Failure", "message":"Action item #%d either does not exist " + \
                                                  "or has already been completed" % id}
        records[0].is_complete = True
        records[0].save()
        return {"status":"Success", "message":"Action has been marked as completed "}


class getTickets(Resource):
    """ Get Tickets (optional date range filter, optional status filter that can contain one or multiple statuses, if filter not supplied return all), returns all ticket fields, paged """

    @RESTfulResponse()
    def get(self, request, dateRange=None, status=None, **kwargs):
        """ dateRange=x,y
            dateRange=,y
            dateRange=x """
        tickets = Ticket.objects.filter()

        if dateRange is not None:
            dates = str(dateRange).split(',')
            dateStart = None
            dateEnd = None
            if len(dates) == 1:
                dateStart = dates[0]
            elif len(dates) > 1:
                dateStart = dates[0]
                dateEnd = dates[1]

            if dateStart == "":
                dateStart = None
            if dateEnd == "":
                dateEnd = None

            print "date range: %s to %s" % (dateStart, dateEnd)
            if dateStart:
                tickets = tickets.filter(created_date__gte=dateStart)
            if dateEnd:
                tickets = tickets.filter(created_date__lte=dateEnd)

        if status is not None:
            print "status: %s" % status
            pprint.pprint(status.split(','))
            tickets = tickets.filter(status__in=status.split(','))

        return tickets


class getTicketDetailByID(Resource):
    """ Get Ticket Detail by ID (returns ticket detail (ticket id, customer id, contact name, contact phone, rep id & rep name, subject, details, open date, resolved date, status) + all notes (id, datetime, rep name & id, text) for the ticket -- no pagination on the notes) """

    @RESTfulResponse()
    def get(self, request, id=None, **kwargs):
        if id is None:
            return {"status":"Failure", "message":"Ticket id is required"}

        records = Ticket.objects.filter(id=id)
        if len(records) == 0:
            return {"status":"Failure", "message":"No ticket with that ID"}

        ticket = model_to_dict(records.get())

        notes = Note.objects.filter(ticket_id=id)
        ticket['notes'] = []
        for note in notes:
            ticket['notes'].append(model_to_dict(note))

        return ticket


class getCustomerByID(Resource):
    """ Get Customer by ID (returns Customer ID, Customer Name, Phone number) """

    @RESTfulResponse()
    def get(self, request, id=None, **kwargs):
        if id is None:
            return {"status":"Failure", "message":"Customer id is required"}

        records = Customer.objects.filter(id=id)
        if len(records) == 0:
            return {"status":"Failure", "message":"No customer with that ID"}

        customer = model_to_dict(records.get())
        return customer
