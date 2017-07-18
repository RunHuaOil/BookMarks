from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from .models import Image
import logging


@receiver(m2m_changed, sender=Image.users_like.through)
def users_like_changed(sender, instance, **kwargs):
    instance.total_likes = instance.users_like.count()
    instance.save(update_fields=['total_likes'])
    # logging.debug(instance.total_likes)
    # logging.debug('收到信号！')
