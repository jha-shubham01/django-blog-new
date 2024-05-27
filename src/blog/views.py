from django.shortcuts import render
from django.views import generic

from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Post, StatusChoices


class PostList(generic.ListView):
    ordering = "-created_on"
    paginate_by = 10
    queryset = Post.objects.filter(status=StatusChoices.PUBLISH.value)
    template_name = "post_list.html"


class PostDraftList(LoginRequiredMixin, generic.ListView):
    login_url = reverse_lazy("login")
    queryset = Post.objects.filter(status=StatusChoices.DRAFT.value).order_by(
        "-created_on"
    )

    def get_queryset(self):
        return super().get_queryset().filter(author=self.request.user)
    


class PostArchivedList(LoginRequiredMixin, generic.ListView):
    login_url = reverse_lazy("login")
    queryset = Post.objects.filter(status=StatusChoices.ARCHIVE.value).order_by(
        "-created_on"
    )

    def get_queryset(self):
        return super().get_queryset().filter(author=self.request.user)


class PostDetail(generic.DetailView):
    queryset = Post.objects.all().order_by("-created_on")
    # template_name = 'post_detail.html'
