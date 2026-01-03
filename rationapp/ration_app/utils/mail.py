from django.core.mail import EmailMultiAlternatives
from django.conf import settings

def send_ration_mail(
    customer_email,
    customer_name,
    request_id,
    shop_name,
    shop_address,
    pickup_start,
    pickup_end
):
    """Send ration approval email to the customer"""
    
    subject = f"✅ Ration Request Approved - #{request_id}"

    # Plain text (fallback)
    text_content = f"""
Dear {customer_name},

Your ration request #{request_id} has been approved.

Pickup location: {shop_name}, {shop_address}
Pickup window: {pickup_start} to {pickup_end}

Please bring your Ration Card and Aadhaar ID for verification.

Thank you for using the Public Distribution System (PDS).

Regards,
Department of Food & Civil Supplies
    """

    # HTML version
    html_content = f"""
    <html>
      <body style="font-family: Arial, sans-serif; background-color: #f9f9f9; padding: 20px;">
        <div style="max-width: 600px; margin: auto; background: white; border-radius: 10px; padding: 20px; box-shadow: 0 0 10px #ddd;">
          <h2 style="color: #2c7;">✅ Ration Request Approved</h2>
          <p>Dear <b>{customer_name}</b>,</p>
          <p>Your ration request <b>#{request_id}</b> has been successfully approved.</p>
          <p>
            <b>Pickup Location:</b> {shop_name}<br>
            <b>Address:</b> {shop_address}<br>
            <b>Pickup Window:</b> {pickup_start} to {pickup_end}
          </p>
          <p>Please bring your <b>Ration Card</b> and <b>Aadhaar ID</b> for verification at the counter.</p>
          <p>Thank you for using the <b>Public Distribution System (PDS)</b>.</p>
          <hr>
          <p style="font-size: 12px; color: gray;">This is an automated message. Please do not reply.</p>
        </div>
      </body>
    </html>
    """

    try:
        msg = EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[customer_email],
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        print(f"✅ Email sent successfully to {customer_email}")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")
