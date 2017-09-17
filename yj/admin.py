from django import forms
from django.contrib import admin
from api.models import Customer, Ticket, Note, ActionItem, Token


class CustomerAdmin(admin.ModelAdmin):
    list_display = ("id", "full_name", "phone")
    class Meta:
        model = Customer

class TicketAdmin(admin.ModelAdmin):
    list_display = ("id", "customer_id", "contact_name", "contact_phone", "rep_id", "created_date", "resolved_date", "last_modified_date", "subject", "details", "status")
    class Meta:
        model = Ticket

class NoteAdmin(admin.ModelAdmin):
    list_display = ("id", "ticket_id", "rep_id", "created_date", "note_text")
    class Meta:
        model = Note

class ActionItemAdmin(admin.ModelAdmin):
    list_display = ("id", "rep_id", "created_by", "description", "due_date", "is_complete")
    class Meta:
        model = ActionItem

class TokenAdmin(admin.ModelAdmin):
    list_display = ("id", "user_id", "jwt")
    class Meta:
        model = ActionItem

admin.site.register(Customer, CustomerAdmin)
admin.site.register(Ticket, TicketAdmin)
admin.site.register(Note, NoteAdmin)
admin.site.register(ActionItem, ActionItemAdmin)
admin.site.register(Token, TokenAdmin)
