from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import DetailView
from apps.news.models import NewsPost, Like, Comment
from django.contrib.auth.decorators import login_required
from apps.news.forms import NewsPostForm, CommentForm
from django.views.generic.edit import CreateView
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect, HttpResponseForbidden, JsonResponse
from django.urls import reverse


# Создание новостных постов
class NewsPostCreateView(LoginRequiredMixin, CreateView):
    model = NewsPost
    form_class = NewsPostForm
    template_name = 'post_form.html'
    success_url = '/news/'

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            if self.request.user.is_staff:
                form.instance.author = self.request.user
                messages.success(self.request, 'Новость успешно добавлена!')
                return super().form_valid(form)
            else:
                messages.error(self.request, 'Вы должны быть администратором, чтобы создать пост.')
                return super().form_invalid(form)
        else:
            messages.error(self.request, 'Вы должны быть авторизированы, чтобы создать пост.')
            return super().form_invalid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Ошибка в форме.')
        return super().form_invalid(form)


# Пагинация на странице новостных постов
def news_list(request):
    news_list = NewsPost.objects.all().order_by('-created_at')
    paginator = Paginator(news_list, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'news_posts.html', {'page_obj': page_obj})


# Детальный просмотр новостных постов
class NewsPostDetailView(LoginRequiredMixin, DetailView):
    model = NewsPost
    template_name = 'news_post_detail.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.views += 1
        self.object.save()
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()

        user_commented = False
        if self.request.user.is_authenticated:
            user_commented = Comment.objects.filter(post=self.object, author=self.request.user).exists()
        
        context['user_commented'] = user_commented
        return context
    

# Cистема лайков
def like_view(request, pk):
    post = get_object_or_404(NewsPost, id=pk)
    user = request.user
    if user.is_authenticated:
        like, created = Like.objects.get_or_create(user=user, post_id=pk)
        if not created:
            like.delete()
    return HttpResponseRedirect(reverse('post_detail', args=[str(pk)]))


# Обработка комментариев
@login_required
def add_comment_to_post(request, pk):
    post = get_object_or_404(NewsPost, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user  
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'add_comment_to_post.html', {'form': form})


# Удаление комментария
@login_required
def comment_delete(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if request.user != comment.author:
        return HttpResponseForbidden("Вы не можете удалить этот комментарий")
    post_pk = comment.post.pk
    comment.delete()
    return redirect('post_detail', pk=post_pk)


# Обновление комментария
@login_required
def comment_edit(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if comment.author != request.user:
        return HttpResponseForbidden()

    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            # Выполняем перенаправление после сохранения комментария
            return redirect('post_detail', pk=comment.post.pk)
    else:
        form = CommentForm(instance=comment)
    return render(request, 'edit_comment.html', {'form': form})




