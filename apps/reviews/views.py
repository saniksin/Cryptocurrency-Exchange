from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView

from apps.reviews.forms import ReviewForm
from apps.reviews.models import Review


# Страница отзывов
class ReviewListView(ListView):
    model = Review
    template_name = 'reviews.html'
    context_object_name = 'reviews'
    ordering = ['-created_at']
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['has_reviewed'] = Review.objects.filter(user=self.request.user).exists()
        return context


# Форма для добавлени отзыва
@login_required
def add_review(request):
    # Проверяем, оставлял ли пользователь уже отзыв
    if Review.objects.filter(user=request.user).exists():
        messages.error(request, 'Вы уже оставляли отзыв!')
        return redirect('reviews')

    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.save()
            messages.success(request, 'Отзыв успешно добавлен!')
            return redirect('reviews')
    else:
        form = ReviewForm()
    return render(request, 'add_review.html', {'form': form})


# Удаление отзыва
@login_required
def review_delete(request, pk):
    review = get_object_or_404(Review, pk=pk)
    if request.user != review.user:
        messages.error(request, 'У вас нету прав на выполнение этой операции!')
        return HttpResponseForbidden("Вы не можете удалить этот отзыв!")
    review.delete()
    messages.error(request, 'Отзыв успешно удален!')
    return redirect('reviews')


# Редактирование отзыва
@login_required
def review_edit(request, pk):
    review = get_object_or_404(Review, pk=pk)
    if review.user != request.user:
        messages.error(request, 'У вас нету прав на выполнение этой операции!')
        return HttpResponseForbidden("Вы не можете редактировать этот отзыв!")
    if request.method == "POST":
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            messages.success(request, 'Отзыв успешно обновлен!')
            return redirect('reviews')
    else:
        form = ReviewForm(instance=review)
        if request.is_ajax():
            if review.text is not None:
                return JsonResponse({'text': review.text})
            else:
                return JsonResponse({'text': ''})
    return render(request, 'reviews.html', {'form': form, 'review': review})

