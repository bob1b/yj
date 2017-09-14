from django.contrib import admin
from api.models import Customer, Ticket, ActionItem, Users

admin.site.register(Customer)
admin.site.register(Ticket)
admin.site.register(ActionItem)
admin.site.register(Users)
