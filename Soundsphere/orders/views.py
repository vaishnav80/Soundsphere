import io
from django.shortcuts import render,redirect
from checkout.models import Orders
from cart.models import *
from checkout.models import Orders,items,shiped_address
from admin_panel.models import Product
from wallet.models import Wallet,Wallet_transaction
from admin_panel.views import active_admin
from wallet.views import active_user
from datetime import date, timezone
from django.http import HttpResponse
from django.core.paginator import Paginator
from reportlab.lib.pagesizes import A4 # type: ignore
from reportlab.lib import colors # type: ignore
from reportlab.lib.units import inch # type: ignore
from reportlab.lib.styles import getSampleStyleSheet # type: ignore
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph,Image, Spacer # type: ignore
from io import BytesIO
from reportlab.pdfgen import canvas # type: ignore
from openpyxl import Workbook # type: ignore
from reportlab.lib import colors # type: ignore
from django.utils.dateparse import parse_date
from django.db.models import Sum,Count
from datetime import date, timedelta
from django.db.models import *
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle # type: ignore
from datetime import datetime
from reportlab.lib.enums import TA_CENTER, TA_RIGHT # type: ignore

@active_admin
def admin_order(req):
    order = Orders.objects.all().order_by('-id')
    today = date.today()
    for i in order:
        if i.order_date != today and i.confirm == False:
            i.status = 'canceled'
            i.save()
    context= {
        'order' : order
    }
    return render(req,'admin_orders.html',context)

@active_admin
def order_manage(req,id):
    obj = items.objects.filter(order_id = id)
    address = Orders.objects.get(id = id)
    context = {
        'obj':obj,
        'address':address
    }
    return render(req,'ordermanage.html',context)

@active_admin
def change_order_status(req,id,status):
    order = Orders.objects.get(id = id)
    dummy_amount =0
    if status == 'canceled':
        obj = items.objects.filter(order_id = id)
        if not order.payment == 'Cash On Delivery':
            for i in obj:
                if i.product_status == True:
                    obj5 = Product.objects.get(name = i.product)
                    obj5.stock = obj5.stock + i.qty
                    obj5.save()
                    dummy_amount = dummy_amount + i.qty*i.rate

                order.status = status
                order.save()
                wallet = Wallet.objects.get(user_id = order.user_id) 
                a = dummy_amount-order.discount
                a = a + order.delivery
                wallet.balance += a
                wallet.save()
                wallet_transaction = Wallet_transaction(wallet_id = wallet , description = 'Order canceled by admin',amount = a ,balance = wallet.balance,order_id =order )
                wallet_transaction.save()

            return redirect(admin_order)
        else:
            for i in obj:
                if i.product_status == True:
                    obj5 = Product.objects.get(name = i.product)
                    obj5.stock = obj5.stock + i.qty
                    obj5.save()

                order.status = status
                order.save()
            return redirect(admin_order)
    else:
        order.status = status
        order.save()
        return redirect(admin_order)
    



def invoice(request,id):
    # Initialize buffer and PDF document
    obj = Orders.objects.get(id = id)
    product = items.objects.filter(order_id = id)
    today = datetime.now()
    buffer = io.BytesIO()
    pdf = SimpleDocTemplate(buffer, pagesize=A4)
    elements = []
    image_path = 'assets\images\soundsphere-removebg-preview.png'
    img = Image(image_path, width=100, height=50) 
    elements = []
    data = [[img, ''],  # Image in the first cell, empty space in the second cell
            ['', '']] 
    table = Table(data, colWidths=[400, 100]) 
    elements = [table, Spacer(1, 5)]
    
    styles = getSampleStyleSheet()

    # Title
    title_style = styles['Title']
    title_style.alignment = TA_CENTER
    elements.append(Paragraph("Invoice", title_style))
    elements.append(Spacer(1, 12))

    # Company and Customer Info
    company_info = "Sold By: SoundSphere Private Limited,<br/>Ship-from Address: L-169, 13th Cross, 15th Main, Sector - 6, HSR Layout, BANGALORE, KARNATAKA, 560102, IN-KA<br/>GSTIN: 29AABCJ9421C1ZP"
    elements.append(Paragraph(company_info, styles['Normal']))
    elements.append(Spacer(1, 12))

    # Customer Info Table
    customer_info = [
        ["Order ID:", id],
        ["Order Date:", obj.order_date],
        ["Invoice Date:",today ],

    ]
    customer_table = Table(customer_info)
    customer_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.whitesmoke),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
    ]))
    elements.append(customer_table)
    elements.append(Spacer(2, 12))

    # Bill To and Ship To
    bill_ship_to = f"Ship To:<br/>{obj.address_id.name} <br/>   {obj.address_id.address},<br/>{obj.address_id.city},{obj.address_id.state}<br/>{obj.address_id.pincode},<br/> Phone:{obj.address_id.phone}<br/>"
    elements.append(Paragraph(bill_ship_to, styles['Normal']))
    elements.append(Spacer(1, 12))

    # Table Header with Two Lines
    table_data = [
        [
            Paragraph("Product", styles['Normal']),
            Paragraph("Title", styles['Normal']),
            Paragraph("Qty", styles['Normal']),
            Paragraph("Amount ", styles['Normal']),
            Paragraph("Discounts/<br/>Coupons ", styles['Normal']),
            Paragraph("Total ", styles['Normal'])
        ],
    ]
    for i in product:
        j = Product.objects.get(name = i.product)
        table_data.append(   
        [
            Paragraph(i.product, styles['Normal']),
            Paragraph(j.description, styles['Normal']),
            i.qty,
            f"{i.total_rate}.00",
            f"{i.total_rate-i.rate}.00",
            f"{int(i.rate)*i.qty}.00"
        ])
    

    # Adjust column widths
    col_widths = [1.8 * inch, 3 * inch, 0.7 * inch, 0.9 * inch, 0.9 * inch, 0.9 * inch]
    table = Table(table_data, colWidths=col_widths)

    # Add style to the table
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.whitesmoke),  # Header background color
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),  # Header text color
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),  # Center-align header text
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Bold font for header
        ('FONTSIZE', (0, 0), (-1, 0), 9),  # Font size for header
        ('BACKGROUND', (0, 1), (-1, 1), colors.white),  # Background color for rows
        ('ALIGN', (0, 1), (-1, -1), 'CENTER'),  # Center-align text
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),  # Font for text in rows
        ('FONTSIZE', (0, 1), (-1, -1), 9),  # Font size for text in rows
        ('VALIGN', (0, 1), (-1, -1), 'TOP'),  # Align text at the top of each cell
        ('LINEBELOW', (0, 1), (-1, 1), 1, colors.black),  # Add line below the first row
        ('LINEABOVE', (0, -1), (-1, -1), 1, colors.black),  # Add line above the total row
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),  # Grid lines
    ]))

    # Add the table to the document
    elements.append(table)

    # Total section
    total_data = [["Total", f"{obj.total}.00"]]
    total_table = Table(total_data, colWidths=[6 * inch, 1 * inch])
    total_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
    ]))
    elements.append(total_table)
    elements.append(Spacer(1, 12))
    total_data = [["Coupon", f"{obj.discount}.00"]]
    total_table = Table(total_data, colWidths=[6 * inch, 1 * inch])
    total_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
    ]))
    elements.append(total_table)
    elements.append(Spacer(1, 12))
    total_data = [["Delivery Charge",f"{obj.delivery}.00"]]
    total_table = Table(total_data, colWidths=[6 * inch, 1 * inch])
    total_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
    ]))
    elements.append(total_table)
    elements.append(Spacer(1, 12))

    # Grand Total section
    grand_total_data = [["Grand Total", f"{obj.grand_total}.00"]]
    grand_total_table = Table(grand_total_data, colWidths=[6 * inch, 1 * inch])
    grand_total_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 14),
    ]))
    elements.append(grand_total_table)
    total_data = [[""]]
    total_table = Table(total_data, colWidths=[6 * inch, 1 * inch])
    total_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
    ]))
    
    elements.append(total_table)
    total_data = [["SoundSphere Private Limited"]]
    total_table = Table(total_data, colWidths=[6 * inch, 1 * inch])
    total_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
    ]))
    elements.append(total_table)
    elements.append(Spacer(1, 12))

    # Build the PDF
    pdf.build(elements)
    pdf_value = buffer.getvalue()
    buffer.close()

    response = HttpResponse(pdf_value, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="report.pdf"'

    return response