from django.http import HttpResponse
from datetime import datetime, timedelta
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, get_object_or_404, redirect

from mainapp.models import Post, UserComplaints, BlockedUser
from moderatorapp.forms import ComplainAction

"""
как работают разрешения в Django
https://webdevblog.ru/chto-nuzhno-znat-chtoby-upravlyat-polzovatelyami-v-django-admin/
"""


def moderator_index(request):
    if not request.user.is_staff:
        raise PermissionDenied()

    content = {'title': 'Модератор', 'last_posts': Post.get_new_post()}
    # запрос не рассмотренных жалоб
    new_complains = UserComplaints.objects.filter(moderator_id__isnull=True)
    content['new_complains'] = new_complains

    return render(request, 'moderatorapp/moder_index.html', context=content)


def moderation_complain(request, pk):
    if not request.user.is_staff:
        raise PermissionDenied()

    complain = get_object_or_404(UserComplaints, id=pk, moderator_id__isnull=True)

    if request.method == 'POST':
        form = ComplainAction(request.POST)
        if form.is_valid():
            user_block_date = None
            user_block_days = int(request.POST.get('user_block_days', 0))
            if user_block_days > 0:
                user_block_date = datetime.now() + timedelta(days=user_block_days)

            # закрытие жалобы
            complain.moderator = request.user
            complain.time_moderated = datetime.now()
            complain.save()

            # отчет в таблицу модерирования
            new_blocked = BlockedUser.objects.create(
                moderator=request.user,
                user=complain.bad_user,
                complaint=complain,
                reason_for_blocking=request.POST.get('reason', None)
            )
            if user_block_date:
                new_blocked.lock_date = user_block_date

            new_blocked.save()

            # снимаем с публикации (если есть комментарий то скрываем его, если нет, то статью)
            if request.POST.get('action_hide', False):
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
