from django.views import View, generic

from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from blog.forms import CommentForm
from .models import Category, Post, StatusChoices


class PostList(generic.ListView):
    # model = Post
    # queryset = Post.objects.filter(status=StatusChoices.PUBLISH.value).order_by(
    #     "-created_on"
    # )
    queryset = Post.objects.filter(status=StatusChoices.PUBLISH.value)
    # template_name = "post_list.html"
    ordering = "-created_on"
    paginate_by = 10


class PostDraftList(LoginRequiredMixin, generic.ListView):
    login_url = reverse_lazy("login")
    ordering = "-created_on"
    queryset = Post.objects.filter(status=StatusChoices.DRAFT.value)

    def get_queryset(self):
        return super().get_queryset().filter(author=self.request.user)


class PostArchivedList(LoginRequiredMixin, generic.ListView):
    login_url = reverse_lazy("login")
    ordering = "-created_on"
    queryset = Post.objects.filter(status=StatusChoices.ARCHIVE.value)

    def get_queryset(self):
        return super().get_queryset().filter(author=self.request.user)


# Just get Post Details
# class PostDetail(generic.edit.FormMixin, generic.DetailView):
#     # template_name = 'post_detail.html'
#     model = Post
#     extra_context = {"categories": Category.objects.all()}


# One way
# class PostDetail(generic.edit.FormMixin, generic.DetailView):
#     model = Post
#     extra_context = {
#         "categories": Category.objects.all(),
#         "form": CommentForm(),
#     }
#     form_class = CommentForm

#     def get_success_url(self):
#         return reverse("author-detail", kwargs={"pk": self.object.pk})

#     def post(self, request, *args, **kwargs):
#         if not request.user.is_authenticated:
#             return HttpResponseForbidden()
#         self.object = self.get_object()
#         form = self.get_form()
#         if form.is_valid():
#             return self.form_valid(form)
#         else:
#             return self.form_invalid(form)

#     def form_valid(self, form):
#         # Here, we would record the user's interest using the message
#         # passed in form.cleaned_data['message']
#         return super().form_valid(form)


class PostDetail(generic.DetailView):
    model = Post
    extra_context = {"categories": Category.objects.all(), "form": CommentForm()}


class CommentFormView(LoginRequiredMixin, generic.FormView):
    # template_name = "blog/post_detail.html
    # model = Comment
    form_class = CommentForm
    success_url = "#"


class PostDetailCommentView(View):
    def get(self, request, *args, **kwargs):
        view = PostDetail.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = CommentFormView.as_view()

        # Save the data
        form = CommentForm(request.POST)
        form.instance.author = request.user
        form.instance.post = Post.objects.get(pk=self.kwargs["pk"])
        if form.is_valid():
            form.save()
        return view(request, *args, **kwargs)
