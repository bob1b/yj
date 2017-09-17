from django import forms
from django.forms.models import model_to_dict
from django.http import HttpResponse
from django.core import serializers
from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
import python_jwt as jwt
import Crypto.PublicKey.RSA as RSA
from simple_rest import Resource
from .models import Customer, Ticket, Note, ActionItem, Token
from simple_rest.response import RESTfulResponse
import datetime
import json
import pprint

# TODO - djangoadmin tweaks
# TODO - code cleanup
# TODO - homepage documentation

STATUSES =  ['pending', 'ready for approval', 'resolved', 'reopened']

class do_login(Resource):

    @RESTfulResponse()
    def get(self, request, **kwargs):
        try:
            username = request.GET.get('username')
            email_address = request.GET.get('email')
            print "logging in - %s:%s" % (username, email_address)
            user = User.objects.get(username=username, email=email_address)
            pprint.pprint(user)
        except Exception as e:
            return {"status":"Failure", "message":("unable to login: %s" % str(e))}

        if user is not None:
            # this is needed when not using authenticate()
            user.backend = 'django.contrib.auth.backends.ModelBackend'

            login(request, user)

            # generate JWT
            key = RSA.generate(2048)
            payload = { 'foo': user.username + user.email };
            token = jwt.generate_jwt(payload, key, 'PS256', datetime.timedelta(minutes=24*60))

            # delete any existing Token records for this user
            Token.objects.filter(user_id=user.id).delete()

            # save token in Token table with user_id
            token_record = Token.objects.create(user_id=user.id, jwt=token)

            return {"status":"Success",
                    "message":"User has been validated",
                    "user_id":user.id,
                    "name":user.username,
                    "email_address":user.email,
                    "JWT":token}

        return {"status":"Failure", "message":"Invalid credentials"}

class do_logout(Resource):
    @RESTfulResponse()
    def get(self, request, **kwargs):
        try:
            logout(request)
        except Exception as e:
            return {"status":"Failure", "message":"An error occurred when logging out: %s" % str(e)}

        return {"status":"Success", "message":"Logged out"}


def get_rep_id(user):
    if user is None:
        return -1
    return user.id

def validate_jwt(request, user_id):
    token = None
    if 'HTTP_AUTHORIZATION' not in request.META:
        return (False, {"status":"Failure", "message":"Missing JWT"})

    token = request.META['HTTP_AUTHORIZATION']

    token_records = Token.objects.filter(user_id=user_id, jwt=token)
    if len(token_records) == 0:
        return (False, {"status":"Failure", "message":"Invalid JWT value"})

    return (True, {})


class getUsers(Resource):
    """ Get Users (return id, name, email) """

    perPage = 10

    @RESTfulResponse()
    def get(self, request, **kwargs):
        rep_id = get_rep_id(request.user)
        if rep_id < 0:
            return {"status":"Access denied", "message":"User must log in"}
        (valid, ret_val) = validate_jwt(request, request.user.id)
        if not valid:
            return ret_val

        page_number = 1
        if request.GET.get('page') is not None:
            page_number = request.GET.get('page')
        p = Paginator(User.objects.all(), self.perPage)
        users = None
        try:
            users = p.page(page_number)
        except:
            print "Error getting page %s, reverting to page 1" % str(page_number)
            page_number = 1
            users = p.page(page_number)

        return { 'page_number':int(page_number),
                 'num_pages':p.num_pages,
                 'data':[model_to_dict(u) for u in users.object_list] }


class getCallSummary(Resource):
    """ Get Call Summary (returns number of calls at each status) """

    @RESTfulResponse()
    def get(self, request, **kwargs):
        rep_id = get_rep_id(request.user)
        if rep_id < 0:
            return {"status":"Access denied", "message":"User must log in"}
        (valid, ret_val) = validate_jwt(request, request.user.id)
        if not valid:
            return ret_val

        summ = {'pending':-1, 'ready for approval':-1, 'resolved':-1, 'reopened':-1}
        for idx, status in enumerate(summ):
            summ[status] = len(Ticket.objects.filter(status=status))
        return summ


class getActionItems(Resource):
    """ Get Action Items for logged in user / status (returns a list of due date / description / is_complete for all action items associated with the user from the JWT token) - optionally can be filtered by is_complete=true or false """

    perPage = 10

    @RESTfulResponse()
    def get(self, request, **kwargs):
        rep_id = get_rep_id(request.user)
        if rep_id < 0:
            return {"status":"Access denied", "message":"User must log in"}
        (valid, ret_val) = validate_jwt(request, request.user.id)
        if not valid:
            return ret_val

        is_complete = request.GET.get('is_complete') or ""
        is_complete = is_complete.lower()

        page_number = 1
        if request.GET.get('page') is not None:
            page_number = request.GET.get('page')

        ai = None
        if is_complete == "true":
            ai = ActionItem.objects.filter(rep_id=rep_id, is_complete=True)
        elif is_complete == "false":
            ai = ActionItem.objects.filter(rep_id=rep_id, is_complete=False)
        else:
            ai = ActionItem.objects.filter(rep_id=rep_id)

        p = Paginator(ai, self.perPage)
        page = None
        try:
            page = p.page(page_number)
        except:
            print "Error getting page %s, reverting to page 1" % str(page_number)
            page_number = 1
            page = p.page(page_number)

        return { 'page_number':int(page_number),
                 'num_pages':p.num_pages,
                 'data':[model_to_dict(ai) for ai in page.object_list] }


class ActionItemForm(forms.ModelForm):
    class Meta:
        model = ActionItem
        fields = ['rep_id', 'description', 'due_date']

class createActionItem(Resource):
    """ Create Action Item (takes rep_id for whom the action item will be created, description, due date, autopopulates created_by with the id of the user on the JWT token """

    @RESTfulResponse()
    def post(self, request):
        rep_id = get_rep_id(request.user)
        if rep_id < 0:
            return {"status":"Access denied", "message":"User must log in"}
        (valid, ret_val) = validate_jwt(request, request.user.id)
        if not valid:
            return ret_val

        form = ActionItemForm(request.POST)

        if not form.is_valid():
            return {"status":"Failure", "message":"Missing one or more form values"}

        new_action_item = form.save(commit=False)
        new_action_item.created_by = rep_id
        new_action_item.save()
        return {"status":"Success", "message":"Action item has been added"}


class resolveActionItem(Resource):
    """ Resolve Action Item (takes item id, sets is_complete=true) """

    @RESTfulResponse()
    def get(self, request, id):
        rep_id = get_rep_id(request.user)
        if rep_id < 0:
            return {"status":"Access denied", "message":"User must log in"}
        (valid, ret_val) = validate_jwt(request, request.user.id)
        if not valid:
            return ret_val

        # ensure record exists and is_complete = False
        records = ActionItem.objects.filter(id=id, is_complete=False)
        if len(records) == 0:
            return {"status":"Failure",
                    "message":("Action item #%s either does not exist or has already been completed") % str(id)}
        records[0].is_complete = True
        records[0].save()
        return {"status":"Success", "message":"Action has been marked as completed "}


class getTickets(Resource):
    """ Get Tickets (optional date range filter, optional status filter that can contain one or multiple statuses, if filter not supplied return all), returns all ticket fields, paged """

    perPage = 10

    @RESTfulResponse()
    def get(self, request, dateRange=None, status=None, **kwargs):
        """ dateRange=x,y
            dateRange=,y
            dateRange=x """
        rep_id = get_rep_id(request.user)
        if rep_id < 0:
            return {"status":"Access denied", "message":"User must log in"}
        (valid, ret_val) = validate_jwt(request, request.user.id)
        if not valid:
            return ret_val

        tickets = Ticket.objects.filter()

        page_number = 1
        if request.GET.get('page') is not None:
            page_number = request.GET.get('page')

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

        p = Paginator(tickets, self.perPage)
        page = None
        try:
            page = p.page(page_number)
        except:
            print "Error getting page %s, reverting to page 1" % str(page_number)
            page_number = 1
            page = p.page(page_number)

        return { 'page_number':int(page_number),
                 'num_pages':p.num_pages,
                 'data':[model_to_dict(t) for t in page.object_list] }

        return tickets


class getTicketDetailByID(Resource):
    """ Get Ticket Detail by ID (returns ticket detail (ticket id, customer id, contact name, contact phone, rep id & rep name, subject, details, open date, resolved date, status) + all notes (id, datetime, rep name & id, text) for the ticket -- no pagination on the notes) """

    @RESTfulResponse()
    def get(self, request, id=None, **kwargs):
        rep_id = get_rep_id(request.user)
        if rep_id < 0:
            return {"status":"Access denied", "message":"User must log in"}
        (valid, ret_val) = validate_jwt(request, request.user.id)
        if not valid:
            return ret_val

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
        rep_id = get_rep_id(request.user)
        if rep_id < 0:
            return {"status":"Access denied", "message":"User must log in"}
        (valid, ret_val) = validate_jwt(request, request.user.id)
        if not valid:
            return ret_val

        if id is None:
            return {"status":"Failure", "message":"Customer id is required"}

        records = Customer.objects.filter(id=id)
        if len(records) == 0:
            return {"status":"Failure", "message":"No customer with that ID"}

        customer = model_to_dict(records.get())
        return customer


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['rep_id', 'status', 'created_date', 'last_modified_date', 'resolved_date', \
                  'customer_id', 'contact_name', 'contact_phone', 'subject', 'details']

class addTicket(Resource):
    """ Add Ticket (takes customer id, contact name, contact phone, subject, details, autopopulate datetime & rep id from the JWT logged in user) """

    @RESTfulResponse()
    def post(self, request):
        rep_id = get_rep_id(request.user)
        if rep_id < 0:
            return {"status":"Access denied", "message":"User must log in"}
        (valid, ret_val) = validate_jwt(request, request.user.id)
        if not valid:
            return ret_val

        values = request.POST.dict()
        values['rep_id'] = rep_id
        values['status'] ="pending"
        values['created_date'] = datetime.datetime.now()
        values['last_modified_date'] = datetime.datetime.now()
        values['resolved_date'] = ""
        form = TicketForm(values)

        if not form.is_valid():
            return {"status":"Failure", "message":"Missing one or more form values"}


        new_action_item = form.save()
        return {"status":"Success", "message":"Ticket has been added"}


class updateTicketStatus(Resource):
    """ Update Ticket Status (takes ticket ID, new status - autopopulate lastmod time) """

    @RESTfulResponse()
    def get(self, request, id=None, new_status=None, **kwargs):
        rep_id = get_rep_id(request.user)
        if rep_id < 0:
            return {"status":"Access denied", "message":"User must log in"}
        (valid, ret_val) = validate_jwt(request, request.user.id)
        if not valid:
            return ret_val

        if new_status is None:
            return {"status":"Failure", \
                    "message":"Missing a status value; value should be one of these [%s]" % \
                        ", ".join(STATUSES)}

        new_status = new_status.lower()
        if new_status is None or new_status not in STATUSES:
            return {"status":"Failure", \
                    "message":"Invalid status; value should be one of these [%s]" % \
                        ", ".join(STATUSES)}
        if id is None:
            return {"status":"Failure", "message":"Ticket id is required"}

        try:
            ticket = Ticket.objects.get(id=id)
        except:
            return {"status":"Failure", "message":"No ticket found with ID %s" % id}

        ticket.status = new_status
        ticket.last_modified_date = datetime.datetime.now()
        if new_status == "resolved":
            ticket.resolved_date = datetime.datetime.now()
        ticket.save()

        return {"status":"Success", "message":"Ticket has been updated"}


class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['ticket_id', 'rep_id', 'note_text', 'created_date']

class addNoteToTicket(Resource):

    @RESTfulResponse()
    def post(self, request):
        rep_id = get_rep_id(request.user)
        if rep_id < 0:
            return {"status":"Access denied", "message":"User must log in"}
        (valid, ret_val) = validate_jwt(request, request.user.id)
        if not valid:
            return ret_val

        values = request.POST.dict()
        if 'note_text'not in values:
            return {"status":"Failure", "message":"Missing note_text"}
        if 'ticket_id' not in values:
            return {"status":"Failure", "message":"Missing ticket_id"}

        try:
            ticket = Ticket.objects.get(id=values['ticket_id'])
        except:
            return {"status":"Failure", "message":"No ticket found with ID %s" % \
                                                  values['ticket_id']}

        new_note_vals = { 'note_text':values['note_text'],
                          'ticket_id':values['ticket_id'],
                          'rep_id':rep_id,
                          'created_date':datetime.datetime.now() }
        form = NoteForm(new_note_vals)

        newNote = form.save() #commit=False)
        return {"status":"Success", "message":"Note has been added"}
