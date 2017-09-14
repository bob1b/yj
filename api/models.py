from django.db import models

class Customer(models.Model):
    id = models.AutoField(primary_key=True) # (PK)
    full_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=30)

class Ticket(models.Model):
    id = models.AutoField(primary_key=True) # (PK)
    customer_id = models.IntegerField() # (FK to Customers table)
    contact_name = models.CharField(max_length=100) # (may or may not be customer's name)
    contact_phone = models.CharField(max_length=30) # (may or may not be customer's phone)
    rep_id = models.IntegerField() # (FK to Users)
    created_date = models.DateField() # (set during ticket creation)
    resolved_date = models.DateField() # (should be populated when status is set to 'Resolved')
    last_modified_date = models.DateField() # (autoupdate)
    subject = models.CharField(max_length=200)
    details = models.CharField(max_length=500)
    status = models.CharField(max_length=30) # (set to 'pending' for new tickets, possible values are pending, ready for approval, resolved, reopened)

class Note(models.Model):
    id = models.AutoField(primary_key=True) # (PK)
    ticket_id = models.IntegerField() # (FK to Ticket)
    rep_id = models.IntegerField() # (FK to users)
    note_text = models.CharField(max_length=500)
    created_date = models.DateField()

class ActionItem(models.Model):
    id = models.AutoField(primary_key=True) # (PK)
    rep_id = models.IntegerField() # (FK to users)
    created_by = models.IntegerField() # (FK to users)
    description = models.CharField(max_length=500)
    due_date = models.DateField()
    is_complete = models.BooleanField(default=False)

class Users(models.Model):
    id = models.AutoField(primary_key=True) # (PK)
    name = models.CharField(max_length=100)
    email_address = models.CharField(max_length=100)
