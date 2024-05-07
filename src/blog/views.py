from django.shortcuts import render
from django.views import generic

from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Post


class PostList(generic.ListView):
    queryset = Post.objects.filter(status=1).order_by("-created_on")
    # template_name = 'post_list.html'


class PostDetail(generic.DetailView):
    queryset = Post.objects.all().order_by("-created_on")
    # template_name = 'post_detail.html'


class PostDraftList(LoginRequiredMixin, generic.ListView):
    login_url = reverse_lazy("login")
    queryset = Post.objects.filter(status=0).order_by("-created_on")

    def get_queryset(self):
        return super().get_queryset().filter(author=self.request.user)
