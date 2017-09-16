from django.contrib import admin
from api.models import Customer, Ticket, Note, ActionItem, Token, Users

admin.site.register(Customer)
admin.site.register(Ticket)
admin.site.register(Note)
admin.site.register(ActionItem)
admin.site.register(Token)
admin.site.register(Users)
