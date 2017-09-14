from django import forms
from django.http import HttpResponse
from django.core import serializers
from simple_rest import Resource

from .models import Customer, Ticket, Note, ActionItem, Users 
from simple_rest.response import RESTfulResponse

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

