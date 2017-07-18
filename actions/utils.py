from django.contrib.contenttypes.models import ContentType
import datetime
from django.utils import timezone
from .models import Action
import logging


def create_action(user, verb, target=None):
    now = timezone.now()
    # logging.debug("create_action  {}".format(now))
    # 搜索一分钟内有没有 id verb 相同的 Action
    last_minute = now - datetime.timedelta(seconds=60)
    similar_actions = Action.objects.filter(user_id=user.id,
                                            verb=verb,
                                            created__gte=last_minute)

    if target:
        # 如果有 target, 检查是否有对 model 一样的操作,则不创建该 Action
        target_ct = ContentType.objects.get_for_model(target)
        similar_actions = similar_actions.filter(target_ct=target_ct,
                                                 target_id=target.id)

    if not similar_actions:
        # no existing actions found
        action = Action(user=user, verb=verb, target=target)
        action.save()
        return True
    return False
