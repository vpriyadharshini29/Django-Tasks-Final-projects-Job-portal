from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.shortcuts import redirect, render
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import logout, login
from django.contrib.auth.forms import UserCreationForm

from .models import Job, Application
from .forms import JobForm, ApplicationForm, JobSearchForm


# ✅ Job List with search + pagination
class JobListView(ListView):
    model = Job
    template_name = "jobs/job_list.html"
    context_object_name = "jobs"
    paginate_by = 5

    def get_queryset(self):
        queryset = Job.objects.all().order_by("-created_at")
        keyword = self.request.GET.get("keyword")
        location = self.request.GET.get("location")
        if keyword:
            queryset = queryset.filter(title__icontains=keyword)
        if location:
            queryset = queryset.filter(location__icontains=location)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_form"] = JobSearchForm(self.request.GET)
        return context


# ✅ Job Detail
class JobDetailView(DetailView):
    model = Job
    template_name = "jobs/job_detail.html"
    context_object_name = "job"


# ✅ Create Job
class JobCreateView(LoginRequiredMixin, CreateView):
    model = Job
    form_class = JobForm
    template_name = "jobs/job_form.html"

    def form_valid(self, form):
        form.instance.posted_by = self.request.user
        return super().form_valid(form)


# ✅ Update Job
class JobUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Job
    form_class = JobForm
    template_name = "jobs/job_form.html"

    def test_func(self):
        job = self.get_object()
        return self.request.user == job.posted_by


# ✅ Delete Job
class JobDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Job
    success_url = reverse_lazy("job_list")
    template_name = "jobs/job_confirm_delete.html"

    def test_func(self):
        job = self.get_object()
        return self.request.user == job.posted_by


# ✅ Apply for Job
class ApplyJobView(LoginRequiredMixin, CreateView):
    model = Application
    form_class = ApplicationForm
    template_name = "jobs/apply_form.html"

    def form_valid(self, form):
        form.instance.applicant = self.request.user
        form.instance.job_id = self.kwargs["pk"]
        response = super().form_valid(form)
        # send confirmation email
        send_mail(
            subject="Application Received",
            message=f"Your application for {form.instance.job.title} has been received.",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[self.request.user.email],
        )
        return response

    def get_success_url(self):
        return reverse_lazy("job_detail", kwargs={"pk": self.kwargs["pk"]})


# ✅ Custom Logout
def custom_logout(request):
    logout(request)
    return redirect("job_list")


# ✅ Signup
def signup_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # auto-login
            return redirect("job_list")
    else:
        form = UserCreationForm()
    return render(request, "registration/signup.html", {"form": form})
