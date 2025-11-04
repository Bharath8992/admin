# billing/utils.py
from io import BytesIO
from urllib.request import urlopen
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Table, TableStyle, Spacer, Image
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch


def generate_pdf(
    bill,
    logo_url="https://cura-therapy-center.netlify.app/images/logo.png",
    scanner_url="https://i.pinimg.com/736x/f6/fb/c4/f6fbc4deadbcc5287d59fff163191cee.jpg",
    hero_url="https://img.freepik.com/free-vector/green-wave-abstract-background_52683-70245.jpg"
):
    """
    Generates a premium Cura Therapy Centre bill PDF
    with logo, hero image, scanner/QR, and branded layout.
    """

    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        topMargin=0.5 * inch,
        bottomMargin=0.5 * inch,
        leftMargin=0.5 * inch,
        rightMargin=0.5 * inch,
    )

    styles = getSampleStyleSheet()

    # --- Custom Styles ---
    company_style = ParagraphStyle(
        'CompanyStyle',
        parent=styles['Heading1'],
        fontSize=20,
        alignment=1,
        fontName='Helvetica-Bold',
        textColor=colors.HexColor("#05652D"),
        spaceAfter=8
    )

    address_style = ParagraphStyle(
        'AddressStyle',
        parent=styles['Normal'],
        fontSize=10,
        alignment=1,
        textColor=colors.HexColor("#333333")
    )

    bill_title_style = ParagraphStyle(
        'BillTitleStyle',
        parent=styles['Heading2'],
        fontSize=16,
        alignment=1,
        fontName='Helvetica-Bold',
        textColor=colors.HexColor("#0B8043"),
        spaceBefore=8,
        spaceAfter=12
    )

    table_text_style = ParagraphStyle(
        'TableTextStyle',
        parent=styles['Normal'],
        fontSize=9,
        alignment=0
    )

    total_style = ParagraphStyle(
        'TotalStyle',
        parent=styles['Heading2'],
        fontSize=14,
        fontName='Helvetica-Bold',
        alignment=2,
        textColor=colors.HexColor("#05652D")
    )

    footer_style = ParagraphStyle(
        'FooterStyle',
        parent=styles['Normal'],
        fontSize=8,
        alignment=1,
        textColor=colors.HexColor("#555555")
    )

    story = []

    # --- Hero Banner (Top Background Image) ---
    try:
        hero_stream = urlopen(hero_url)
        hero_img = Image(hero_stream, width=7.5 * inch, height=1.5 * inch)
        hero_img.hAlign = 'CENTER'
        story.append(hero_img)
        story.append(Spacer(1, 8))
    except Exception as e:
        print(f"⚠️ Unable to load hero image: {e}")

    # --- Logo ---
    try:
        logo_stream = urlopen(logo_url)
        logo = Image(logo_stream, width=1.4 * inch, height=1.4 * inch)
        logo.hAlign = 'CENTER'
        story.append(logo)
        story.append(Spacer(1, 10))
    except Exception as e:
        print(f"⚠️ Unable to load logo: {e}")

    # --- Company Header ---
    story.append(Paragraph("Cura Therapy Centre", company_style))
    story.append(Paragraph(
        "CMC Eye Hospital Road, Dinakaran Stopping, Opp. New Fresh Market,<br/>"
        "Near Bajaj Showroom, First Floor Above MedPlus, Arni Road, Vellore",
        address_style
    ))
    story.append(Spacer(1, 15))

    # --- Bill Info ---
    story.append(Paragraph(f"BILL #{bill.bill_number}", bill_title_style))
    story.append(Paragraph(f"Date: {bill.created_at.strftime('%d-%m-%Y %H:%M')}", address_style))
    story.append(Spacer(1, 15))

    # --- Customer Info ---
    customer_info = [
        ["<b>Bill To:</b>", f"{bill.customer.name}<br/>"
                            f"Mobile: {bill.customer.mobile}<br/>"
                            f"Email: {bill.customer.email or 'N/A'}"]
    ]
    customer_table = Table(customer_info, colWidths=[1.5 * inch, 4.5 * inch])
    customer_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LINEBELOW', (0, 0), (-1, 0), 0.5, colors.HexColor("#B5D4B2")),
    ]))
    story.append(customer_table)
    story.append(Spacer(1, 15))

    # --- Services Table ---
    services_data = [['ITEM', 'DESCRIPTION', 'QTY', 'PRICE', 'TAX', 'AMOUNT']]

    for bill_service in bill.billservice_set.all():
        amount = bill_service.price * bill_service.quantity
        services_data.append([
            "Service",
            bill_service.service.name,
            str(bill_service.quantity),
            f"₹{bill_service.price:.2f}",
            "5%",
            f"₹{amount:.2f}"
        ])

    table = Table(
        services_data,
        colWidths=[1 * inch, 2.7 * inch, 0.6 * inch, 0.8 * inch, 0.6 * inch, 1 * inch]
    )
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#05652D")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#A5CFA0")),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('ALIGN', (2, 1), (-1, -1), 'RIGHT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1),
         [colors.whitesmoke, colors.HexColor("#F1F8F1")]),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('TOPPADDING', (0, 0), (-1, 0), 8),
    ]))
    story.append(table)
    story.append(Spacer(1, 25))

    # --- Total Section ---
    story.append(Paragraph(f"Total: ₹{bill.total_amount:.2f}", total_style))
    story.append(Spacer(1, 15))

    # --- Notes ---
    notes_text = (
        "<b>Thank you for choosing Cura Therapy Centre.</b><br/>"
        "We appreciate your trust and look forward to serving you again.<br/>"
        "For queries, contact <b>info@curaspa.com</b> or call +91-98765-43210."
    )
    story.append(Paragraph(notes_text, table_text_style))
    story.append(Spacer(1, 20))

    # --- Scanner / UPI QR Image ---
    try:
        scanner_stream = urlopen(scanner_url)
        scanner_img = Image(scanner_stream, width=2 * inch, height=2 * inch)
        scanner_img.hAlign = 'CENTER'
        story.append(scanner_img)
        story.append(Spacer(1, 8))
        story.append(Paragraph("Scan to Pay", address_style))
    except Exception as e:
        print(f"⚠️ Unable to load scanner image: {e}")

    # --- Footer ---
    story.append(Spacer(1, 20))
    story.append(Paragraph("© 2025 Cura Therapy Centre — All Rights Reserved", footer_style))
    story.append(Paragraph("This is a computer-generated invoice.", footer_style))

    # --- Build PDF ---
    doc.build(story)
    buffer.seek(0)
    return buffer
