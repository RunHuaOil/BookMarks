from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ImageCreateForm
from django.shortcuts import get_object_or_404
from .models import Image
from django.http import JsonResponse
from common.decorators import ajax_required
from django.views.decorators.http import require_POST
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from actions.utils import create_action
import logging
import redis
from django.conf import settings

# connect to redis
r = redis.StrictRedis(host=settings.REDIS_HOST,
                      port=settings.REDIS_PORT,
                      db=settings.REDIS_DB)


@login_required()
def image_create(request):
    if request.method == 'POST':
        form = ImageCreateForm(data=request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            new_item = form.save(commit=False)
            new_item.user = request.user
            new_item.save()
            create_action(request.user, '添加图片', new_item)
            messages.success(request, '图片分享成功')
            return redirect(new_item.get_absolute_url())
    else:
        form = ImageCreateForm(data=request.GET)
    return render(request, 'images/image/create.html', {'section': 'images', 'form': form})


def image_detail(request, id, slug):
    image = get_object_or_404(Image, id=id, slug=slug)
    # logging.debug(image.image.url)
    # 图片被看过的数量
    total_views = r.incr('image:{}:views'.format(image.id))
    r.zincrby('image_ranking', image.id, 1)
    # 在 image_ranking 这个有序集合中，增加 image.id 这个成员的分数，增加 1
    # （假如image_ranking这个有序集合不存在，相当于zadd命令，会创建相应的集合和成员）
    return render(request, 'images/image/detail.html', {'section': 'images', 'image': image,
                                                        'total_views': total_views})


@ajax_required
@login_required
@require_POST
def image_like(request):
    image_id = request.POST.get('id')
    action = request.POST.get('action')
    if image_id and action:
        try:
            image = Image.objects.get(id=image_id)
            if action == 'like':
                image.users_like.add(request.user)
                create_action(request.user, '喜欢图片', image)
            else:
                image.users_like.remove(request.user)
            return JsonResponse({'status': 'ok'})

        except:
            pass
    return JsonResponse({'status': 'ko'})


@login_required()
def image_list(request):
    images = Image.objects.all()
    paginator = Paginator(images, 8)
    page = request.GET.get('page')
    try:
        images = paginator.page(page)
    except PageNotAnInteger:
        images = paginator.page(1)
    except EmptyPage:
        if request.is_ajax():
            return HttpResponse('')
        images = paginator.page(paginator.num_pages)

    if request.is_ajax():
        return render(request, 'images/image/list_ajax.html', {'section': 'images', 'images': images})

    return render(request, 'images/image/list.html', {'section': 'images', 'images': images})


@login_required
def image_ranking(request):
    # 返回 image 的 id 降序列表前十个id, id 为 bytes 类型
    image_ranking_list = r.zrange('image_ranking', 0, -1, desc=True)[:10]
    # 把 bytes 列表 转为 int 类型的 id 列表
    image_ranking_ids = [int(id_item) for id_item in image_ranking_list]
    # 取回来的 Image 对象是无序排列的
    image_list_rank = list(Image.objects.filter(id__in=image_ranking_ids))
    # image_list_rank 的每个对象带入 x，以x.id在 image_ranking_ids有序列表中匹配自己的索引位置，以此来排序
    image_list_rank.sort(key=lambda x: image_ranking_ids.index(x.id))

    return render(request, 'images/image/ranking.html',
                  {'section': 'images_rank', 'image_list_rank': image_list_rank})
