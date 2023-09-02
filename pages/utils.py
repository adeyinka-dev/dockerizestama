from django.core.mail import send_mail


def send_signup_notification_email(user, room):
    hostel_email = room.hostel.email
    if not hostel_email:  # If hostel does not have an email
        print("No email provided for hostel.")
        return  # Exit the function

    subject = "New Tenant Signup"
    message = (
        f"Alert! A new tenant has just signed up and occupied Room {room.room_number}."
    )

    try:
        send_mail(
            subject,
            message,
            from_email="elizaluxhomes@gmail.com",
            recipient_list=[hostel_email],
            fail_silently=True,
        )
    except Exception as e:
        print(f"Unexpected error occurred while sending email: {e}")
