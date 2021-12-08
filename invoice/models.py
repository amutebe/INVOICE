from django.db import models
import datetime
from django.contrib.auth.models import User
from django.conf import settings

# Create your models here.
class approval_status(models.Model):

    description=models.CharField("Approval status", max_length=50,null=True,blank=True)
    
    def __str__(self):
        return self.description


class verificationstatus(models.Model):

    description=models.CharField("Approval status", max_length=50,null=True,blank=True)
    
    def __str__(self):
        return self.description
class Invoice(models.Model):
    invoice_no=models.TextField()
    customer = models.CharField(max_length=100)
    customer_email = models.EmailField(null=True, blank=True)
    billing_address = models.TextField(null=True, blank=True)
    date = models.DateField()
    due_date = models.DateField(null=True, blank=True)
    message = models.TextField(default= "this is a default message.")
    total_amount = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)
    status = models.BooleanField(default=False)
    entered_by = models.ForeignKey(settings.AUTH_USER_MODEL,null=True, blank=True, related_name='invoiceinterested_entered_by',on_delete=models.CASCADE)
    date_today=models.DateField("Date created:",default=datetime.datetime.now)
    invoice_status=models.ForeignKey(approval_status, on_delete=models.CASCADE,null=True,verbose_name='Status:')
    rejected=models.TextField("Reason for rejecting:",null=True,blank=True, help_text='If rejected, please give a reason')
    approval_date=models.DateField("Date Approved:",null=True,blank=True)
    approved_by=models.ForeignKey(settings.AUTH_USER_MODEL,null=True, blank=True, related_name='invoiceApprov_by',on_delete=models.CASCADE)
    qmsstatus=models.ForeignKey(verificationstatus, on_delete=models.CASCADE,null=True,verbose_name='Verification Status:')
    verification_failed=models.TextField("Reason for rejecting:",null=True,blank=True, help_text='If rejected, please give a reason')
    completion=models.DateField("Completion Date:",null=True,blank=True)
    scheduled=models.DateField("Rescheduled Date:",null=True,blank=True)


    def __str__(self):
        return str(self.customer)
    
    def get_status(self):
        return self.status

    # def save(self, *args, **kwargs):
        # if not self.id:             
        #     self.due_date = datetime.datetime.now()+ datetime.timedelta(days=15)
        # return super(Invoice, self).save(*args, **kwargs)

class LineItem(models.Model):
    customer = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    service = models.TextField()
    description = models.TextField()
    quantity = models.IntegerField()
    rate = models.DecimalField(max_digits=9, decimal_places=2)
    amount = models.DecimalField(max_digits=9, decimal_places=2)

    def __str__(self):
        return str(self.customer)
   