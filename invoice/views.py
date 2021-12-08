from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.template.loader import get_template
from django.http import HttpResponse
from django.views import View
from .models import LineItem, Invoice
from .forms import LineItemFormset, InvoiceForm
import decimal
import pdfkit
from . import utils
##To avoid surprising value from rounding of VAT values
Round = lambda x, n: eval('"%.'+str(int(n))+'f" % '+repr(int(x)+round(float('.'+str(float(x)).split('.')[1]),n)))

class InvoiceListView(View):
    def get(self, *args, **kwargs):
        invoices = Invoice.objects.all()
        context = {
            "invoices":invoices,
        }

        return render(self.request, 'invoice/invoice-list.html', context)
    
    def post(self, request):        
        # import pdb;pdb.set_trace()
        invoice_ids = request.POST.getlist("invoice_id")
        invoice_ids = list(map(int, invoice_ids))

        update_status_for_invoices = int(request.POST['status'])
        invoices = Invoice.objects.filter(id__in=invoice_ids)
        update_status_for_invoices_approval = int(request.POST['invoice_status'])
        # import pdb;pdb.set_trace()
        if update_status_for_invoices == 0:
            invoices.update(status=False)
        else:
            invoices.update(status=True)

        if update_status_for_invoices_approval == 0:
            invoices.update(invoice_status=0)
        elif update_status_for_invoices_approval == 1:
            invoices.update(invoice_status=1) 
        else:
            invoices.update(invoice_status=2)


        return redirect('invoice:invoice-list')

def createInvoice(request):
    """
    Invoice Generator page it will have Functionality to create new invoices, 
    this will be protected view, only admin has the authority to read and make
    changes here.
    """

    heading_message = 'Formset Demo'
    if request.method == 'GET':
        formset = LineItemFormset(request.GET or None)
        form = InvoiceForm(request.GET or None)
    elif request.method == 'POST':
        formset = LineItemFormset(request.POST)
        form = InvoiceForm(request.POST)
        
        if form.is_valid():
            invoice = Invoice.objects.create(invoice_no=utils.invoice_no(),
                    customer=form.data["customer"],
                    customer_email=form.data["customer_email"],
                    billing_address = form.data["billing_address"],
                    date=form.data["date"],
                    due_date=form.data["due_date"], 
                    message=form.data["message"],
                    )
            # invoice.save()
            
        if formset.is_valid():
            # import pdb;pdb.set_trace()
            # extract name and other data from each form and save
            total = 0
            for form in formset:
                service = form.cleaned_data.get('service')
                description = form.cleaned_data.get('description')
                quantity = form.cleaned_data.get('quantity')
                rate = form.cleaned_data.get('rate')
                if service and description and quantity and rate:
                    amount = float(rate)*float(quantity)
                    total += amount
                    LineItem(customer=invoice,
                            service=service,
                            description=description,
                            quantity=quantity,
                            rate=rate,
                            amount=amount).save()
            invoice.total_amount = total
            invoice.save()
            try:
                generate_PDF(request, id=invoice.id)
            except Exception as e:
                print(f"********{e}********")
            return redirect('/')
    context = {
        "title" : "Invoice Generator",
        "formset": formset,
        "form": form,
    }
    return render(request, 'invoice/invoice-create.html', context)


def view_PDF(request, id=None):
    invoice = get_object_or_404(Invoice, id=id)
    lineitem = invoice.lineitem_set.all()


    context = {
        "company": {
            "name": "Business Centre Limited",
            "address" :"8th Street, Plot 3, Industrial Area,",
            "floor":"2nd Floor, City Star Building",
            "box":"P.O Box 25364, Kampala, Uganda",
            "phone": "+256 4141 349755/312 262487",
            "fax": "256 414 349 755",
            "email": "bcl@bclug.com",
            "web": "www.bclug.com",
            
        },
        "invoice_no": invoice.invoice_no,
        "invoice_sub_total":invoice.total_amount,
        "tin": "1000044580",
        "vat": "29433-P",
      
        "VAT":Round(decimal.Decimal(invoice.total_amount)*decimal.Decimal(0.18),2),
        "invoice_total":Round(sum([float(Round(decimal.Decimal(invoice.total_amount)*decimal.Decimal(0.18),2)), float(invoice.total_amount)]),2),
        "customer": invoice.customer,
        "customer_email": invoice.customer_email,
        "date": invoice.date,
        "due_date": invoice.due_date,
        "billing_address": invoice.billing_address,
        "message": invoice.message,
        "lineitem": lineitem,
        "delivery": "3-4Days from date of  Order Receipt",
        "warranty": "1 Year against Manufacturer defects",
        "prices": "Valid for 30days from Invoice Date",

        "one": "100% Cash/Cheque/EFT/RTGS to Business Centre Ltd  within 30Days from Date of Complete Delivery",
        "two": "Goods remain the property of Business Centre Ltd, until fully paid for",
        "three": "Licences can be withdrawn without further Notice if payment dates are not adhered to",
        "four": "Payments exceeding 30 days will attract a 3% interest per month",

    }
    return render(request, 'invoice/pdf_template.html', context)

def generate_PDF(request, id):
    # Use False instead of output path to save pdf to a variable
    pdf = pdfkit.from_url(request.build_absolute_uri(reverse('invoice:invoice-detail', args=[id])), False)
    response = HttpResponse(pdf,content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="invoice.pdf"'

    return response


def change_status(request):
    return redirect('invoice:invoice-list')

def view_404(request,  *args, **kwargs):

    return redirect('invoice:invoice-list')