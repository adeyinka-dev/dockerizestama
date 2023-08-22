from typing import Any, Dict
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic import DetailView, FormView
from django.views import View
from .models import Maintenance
from accommodations.models import Room
from .forms import MaintenanceForm, NoteForm, MaintenanceStatusForm


class NoteGet(DetailView):
    model = Maintenance
    template_name = "work_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = NoteForm()
        context["status_form"] = MaintenanceStatusForm(instance=self.object)
        return context


class PostNote(FormView):
    model = Maintenance
    form_class = NoteForm
    template_name = "work_detail.html"

    def get_maintenance(self):
        return Maintenance.objects.get(pk=self.kwargs["pk"])

    def post(self, request, *args, **kwargs):
        self.object = self.get_maintenance()
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        note = form.save(commit=False)
        note.maintenance = self.object
        note.author = self.request.user
        note.save()
        return super().form_valid(form)

    def get_success_url(self):
        maintenance = self.object
        return reverse("work_detail", kwargs={"pk": maintenance.pk})

    def post(self, request, *args, **kwargs):
        self.object = self.get_maintenance()

        # Check if status form was submitted
        status_form = MaintenanceStatusForm(request.POST, instance=self.object)
        if status_form.is_valid():
            status_form.save()
            return redirect(self.get_success_url())  # Redirect to the detail page

        # If status form wasn't submitted, continue with the note processing
        return super().post(request, *args, **kwargs)


class RepairDetailView(View):
    def get(self, request, *args, **kwargs):
        view = NoteGet.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = PostNote.as_view()
        return view(request, *args, **kwargs)


class RoomRepair(DetailView):
    model = Room
    template_name = "raise_repair.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = MaintenanceForm()
        return context

    def post(self, request, *args, **kwargs):
        form = MaintenanceForm(request.POST)
        if form.is_valid():
            maintenance = form.save(commit=False)
            maintenance.room = self.get_object()
            maintenance.save()
            return redirect("submit_success")
        return self.get(request, *args, **kwargs)
