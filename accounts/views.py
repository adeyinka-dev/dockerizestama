from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import TenantCreationForm
from accommodations.models import Room


class SignUpView(CreateView):
    form_class = TenantCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/auth.html"

    def form_valid(self, form):
        tenant = form.save(commit=False)
        room_id = form.cleaned_data["room_id"]
        room = Room.objects.get(room_id=room_id)
        room.tenant = tenant
        room.status = Room.OCCUPIED
        room.save()

        tenant.save()
        return super().form_valid(form)
