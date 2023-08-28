from django.urls import reverse_lazy
from django.views.generic import TemplateView, FormView
from .forms import ClientCreationForm
from django.core.mail import send_mail, BadHeaderError


class StamaClient(FormView):
    template_name = "home/stama_signup.html"
    form_class = ClientCreationForm
    success_url = reverse_lazy("thanks")

    def form_valid(self, form):
        client = form.save()

        try:
            # Sending email notification to admin
            subject_to_admin = "New Client Registration"
            message_to_admin = (
                f"A new client, {client.email}, has registered their interest."
            )
            from_email = "elizaluxhomes@gmail.com"
            recipient_list_admin = ["makindeyink12@gmail.com"]

            send_mail(
                subject_to_admin,
                message_to_admin,
                from_email,
                recipient_list_admin,
                fail_silently=False,
            )

            # Sending email confirmation to client
            subject_to_client = "Thank you for registering with StamaPro"
            message_to_client = (
                "Dear client,\n\n"
                "Thank you for registering your interest with StamaPro. "
                "Our team will get back to you soon.\n\n"
                "Best regards,\n"
                "StamaPro Team"
            )
            recipient_list_client = [client.email]

            send_mail(
                subject_to_client,
                message_to_client,
                from_email,
                recipient_list_client,
                fail_silently=False,
            )

        except BadHeaderError:  # This checks for invalid headers
            # You can log the error here if needed
            pass
        except Exception as e:
            # Log the error or handle it as needed
            pass

        return super().form_valid(form)


class StamaHome(TemplateView):
    template_name = "home/stamapro_home.html"
