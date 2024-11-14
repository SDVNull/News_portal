from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_protect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from django.contrib.auth.mixins import PermissionRequiredMixin
from unicodedata import category

from .filters import NewsFilter
from .forms import PostForm
from .models import Post, Category


class NewsList(ListView):
    model = Post
    ordering = '-time_in'
    template_name = 'news.html'
    context_object_name = 'news_list'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = NewsFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filterset"] = self.filterset
        return context


class NewsDetail(DetailView):
    model = Post
    template_name = 'news_detail.html'
    context_object_name = 'news_detail'


class PublicationCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('portal.add_post',)
    form_class = PostForm
    model = Post
    template_name = "publication_edit.html"

    def form_valid(self, form):
        _var = form.save(commit=False)
        if self.request.path.split('/')[1] == 'news':
            _var.field_choice = "NW"
        elif self.request.path.split('/')[1] == 'article':
            _var.field_choice = "AR"
        return super().form_valid(form)


class PublicationUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('portal.change_post',)
    form_class = PostForm
    model = Post
    template_name = 'publication_edit.html'

    def form_valid(self, form):
        _var = form.save(commit=False)
        if self.request.path.split('/')[1] == 'news':
            _var.field_choice = "NW"
        elif self.request.path.split('/')[1] == 'article':
            _var.field_choice = "AR"
        return super().form_valid(form)


class PublicationDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('portal.delete_post',)
    model = Post
    template_name = 'publication_delete.html'
    success_url = reverse_lazy('detail_news')


