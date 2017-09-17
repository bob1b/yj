from django.contrib import admin
from api.models import Customer, Ticket, Note, ActionItem, Token

admin.site.register(Customer)
admin.site.register(Ticket)
admin.site.register(Note)
admin.site.register(ActionItem)
admin.site.register(Token)
