# billing/utils.py - Updated to match your image format
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch, mm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Spacer
from reportlab.lib import colors
from django.http import HttpResponse
import os

def generate_pdf(bill):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, 
                           topMargin=0.5*inch, 
                           bottomMargin=0.5*inch,
                           leftMargin=0.5*inch,
                           rightMargin=0.5*inch)
    styles = getSampleStyleSheet()
    
    # Create custom styles matching the image
    company_style = ParagraphStyle(
        'CompanyStyle',
        parent=styles['Normal'],
        fontSize=14,
        spaceAfter=6,
        alignment=1,  # Center
        fontName='Helvetica-Bold',
    )
    
    address_style = ParagraphStyle(
        'AddressStyle',
        parent=styles['Normal'],
        fontSize=10,
        spaceAfter=12,
        alignment=1,  # Center
    )
    
    bill_title_style = ParagraphStyle(
        'BillTitleStyle',
        parent=styles['Normal'],
        fontSize=16,
        spaceAfter=6,
        alignment=1,  # Center
        fontName='Helvetica-Bold',
        textColor=colors.black,
    )
    
    bill_subtitle_style = ParagraphStyle(
        'BillSubtitleStyle',
        parent=styles['Normal'],
        fontSize=12,
        spaceAfter=12,
        alignment=1,  # Center
        fontName='Helvetica-Bold',
    )
    
    table_header_style = ParagraphStyle(
        'TableHeaderStyle',
        parent=styles['Normal'],
        fontSize=9,
        fontName='Helvetica-Bold',
        alignment=1,  # Center
    )
    
    table_text_style = ParagraphStyle(
        'TableTextStyle',
        parent=styles['Normal'],
        fontSize=8,
        alignment=0,  # Left
    )
    
    table_number_style = ParagraphStyle(
        'TableNumberStyle',
        parent=styles['Normal'],
        fontSize=8,
        alignment=2,  # Right
    )
    
    notes_style = ParagraphStyle(
        'NotesStyle',
        parent=styles['Normal'],
        fontSize=9,
        alignment=0,  # Left
        spaceAfter=12,
    )
    
    total_style = ParagraphStyle(
        'TotalStyle',
        parent=styles['Normal'],
        fontSize=14,
        fontName='Helvetica-Bold',
        alignment=1,  # Center
        spaceAfter=6,
    )
    
    footer_style = ParagraphStyle(
        'FooterStyle',
        parent=styles['Normal'],
        fontSize=8,
        alignment=1,  # Center
        textColor=colors.grey,
    )
    
    # Build the PDF content
    story = []
    
    # Company Header (like in the image)
    story.append(Paragraph("CURA SPA & WELLNESS", company_style))
    story.append(Paragraph("123 Business Street<br/>City, State 12345<br/>India", address_style))
    
    # Horizontal line
    story.append(Spacer(1, 6))
    story.append(Paragraph("<hr/>", styles['Normal']))
    story.append(Spacer(1, 12))
    
    # Bill Title
    story.append(Paragraph(f"BILL #{bill.bill_number}", bill_title_style))
    story.append(Paragraph("CURA SPA & WELLNESS", bill_subtitle_style))
    story.append(Paragraph(f"Date: {bill.created_at.strftime('%d-%m-%Y %H:%M')}", address_style))
    
    # Customer Information
    customer_info = [
        [Paragraph("<b>Bill To:</b>", table_text_style), 
         Paragraph(f"{bill.customer.name}<br/>Mobile: {bill.customer.mobile}<br/>Email: {bill.customer.email or 'N/A'}", table_text_style)]
    ]
    
    customer_table = Table(customer_info, colWidths=[1.5*inch, 4*inch])
    customer_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ]))
    
    story.append(customer_table)
    story.append(Spacer(1, 15))
    
    # Services Table (matching the image format)
    services_data = [
        [
            Paragraph("<b>ITEMS</b>", table_header_style),
            Paragraph("<b>DESCRIPTION</b>", table_header_style),
            Paragraph("<b>QUANTITY</b>", table_header_style),
            Paragraph("<b>PRICE</b>", table_header_style),
            Paragraph("<b>TAX</b>", table_header_style),
            Paragraph("<b>AMOUNT</b>", table_header_style)
        ]
    ]
    
    for bill_service in bill.billservice_set.all():
        services_data.append([
            Paragraph("Service", table_text_style),
            Paragraph(bill_service.service.name, table_text_style),
            Paragraph(str(bill_service.quantity), table_number_style),
            Paragraph(f"₹{bill_service.price:.2f}", table_number_style),
            Paragraph("5%", table_number_style),
            Paragraph(f"₹{(bill_service.price * bill_service.quantity):.2f}", table_number_style)
        ])
    
    services_table = Table(services_data, colWidths=[0.8*inch, 2*inch, 0.6*inch, 0.8*inch, 0.6*inch, 1*inch])
    services_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('ALIGN', (2, 1), (5, -1), 'RIGHT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    
    story.append(services_table)
    story.append(Spacer(1, 20))
    
    # Horizontal line
    story.append(Paragraph("<hr/>", styles['Normal']))
    story.append(Spacer(1, 15))
    
    # Notes Section (like in the image)
    story.append(Paragraph("<b>NOTES:</b>", notes_style))
    story.append(Paragraph("Thank you for choosing CURA SPA & WELLNESS. We appreciate your business and look forward to serving you again. For any queries, please contact us at info@curaspa.com.", notes_style))
    story.append(Spacer(1, 15))
    
    # Horizontal line
    story.append(Paragraph("<hr/>", styles['Normal']))
    story.append(Spacer(1, 10))
    
    # Total Amount
    story.append(Paragraph(f"<b>₹{bill.total_amount:.2f}</b>", total_style))
    story.append(Spacer(1, 10))
    
    # Horizontal line
    story.append(Paragraph("<hr/>", styles['Normal']))
    story.append(Spacer(1, 10))
    
    # Footer
    story.append(Paragraph("Presented by CURA SPA & WELLNESS", footer_style))
    story.append(Paragraph("The owner and management of CURA SPA & WELLNESS certify that this bill represents the actual services provided and amounts due.", footer_style))
    
    # Build PDF
    doc.build(story)
    
    buffer.seek(0)
    return buffer