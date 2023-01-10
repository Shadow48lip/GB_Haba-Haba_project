from django.http import HttpResponse
from datetime import datetime, timedelta
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, get_object_or_404, redirect

from mainapp.models import Post, UserComplaints, BlockedUser, Comment
from moderatorapp.forms import ComplainAction

"""
как работают разрешения в Django
https://webdevblog.ru/chto-nuzhno-znat-chtoby-upravlyat-polzovatelyami-v-django-admin/
"""


def moderator_index(request):
    if not request.user.is_superuser and not request.user.is_staff:
        raise PermissionDenied()

    content = {'title': 'Модератор', 'last_posts': Post.get_new_post()}
    # запрос не рассмотренных жалоб
    new_complains = UserComplaints.objects.filter(moderator_id__isnull=True)
    content['new_complains'] = new_complains

    return render(request, 'moderatorapp/moder_index.html', context=content)


def moderation_complain(request, pk):
    """Рассмотрение заявок на модерацию"""
    if not request.user.is_superuser and not request.user.is_staff:
        raise PermissionDenied()

    complain = get_object_or_404(UserComplaints, id=pk, moderator_id__isnull=True)

    if request.method == 'POST':
        form = ComplainAction(request.POST)
        if form.is_valid():
            # расчёт даты конца блокировки, если блокируем
            user_block_date = None
            user_block_days = form.cleaned_data['user_block_days']
            if user_block_days > 0:
                user_block_date = datetime.now() + timedelta(days=user_block_days)

            # закрытие жалобы
            complain.moderator = request.user
            complain.time_moderated = datetime.now()
            complain.save()

            # отчёт в таблицу модерирования
            new_blocked = BlockedUser.objects.create(
                moderator=request.user,
                user=complain.bad_user,
                complaint=complain,
                reason_for_blocking=form.cleaned_data['reason'],
            )
            if user_block_date:
                new_blocked.lock_date = user_block_date

            new_blocked.save()

            # снимаем с публикации (если есть комментарий то скрываем его, если нет, то статью)
            if form.cleaned_data['action_hide']:
                if complain.comment:
                    print('скрываем комментарий')
                    complain.comment.is_published = False
                    complain.comment.save()

                else:
                    print('скрываем статью')
                    complain.post.is_published = False
                    complain.post.is_blocked = True
                    complain.post.save()

            # блокировка юзера
            if user_block_date:
                complain.bad_user.lock_date = user_block_date
                complain.bad_user.save()

            print(form.cleaned_data)

            return redirect('moderator:index')
    else:
        form = ComplainAction(initial={'user_block_days': 0})

    content = {
        'title': 'Обработка жалобы',
        'last_posts': Post.get_new_post(),
        'form': form,
        'complain': complain
    }

    return render(request, 'moderatorapp/moder_complaint.html', context=content)


def action_post(request, pk):
    """Статья.
    Модератор сам нашёл нарушения в статье на портале
    Создаётся новая заявка и сразу редирект на её рассмотрение.
    """
    if not request.user.is_superuser and not request.user.is_staff:
        raise PermissionDenied()

    post = get_object_or_404(Post, id=pk)

    new_complain = UserComplaints.objects.create(
        user=request.user,
        bad_user=post.author,
        post=post,
    )
    new_complain.save()

    return redirect('moderator:complain', pk=new_complain.id)


def action_comment(request, pk):
    """Комментарий.
    Модератор сам нашёл нарушения в комментарии на портале
    Создаётся новая заявка и сразу редирект на её рассмотрение.
    """

    if not request.user.is_superuser and not request.user.is_staff:
        raise PermissionDenied()

    comment = get_object_or_404(Comment, id=pk)

    new_complain = UserComplaints.objects.create(
        user=request.user,
        bad_user=comment.user,
        post=comment.post,
        comment=comment
    )
    new_complain.save()

    return redirect('moderator:complain', pk=new_complain.id)

