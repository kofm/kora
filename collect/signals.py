from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver

from collect.models import Cart


@receiver(pre_save, sender=Cart)
# Signal to make inactive, i.e. is_active=False, all the other user's Cart
# instances when selecting a new Cart instance
def unique_cart_active(sender, instance, **kwargs):
    if instance.is_active:
        Cart.objects.filter(user=instance.user_id).exclude(pk=instance.pk).update(is_active=False)


@receiver(post_delete, sender=Cart)
def set_new_active_cart(sender, instance, **kwargs):
    if instance.is_active:
        cart = Cart.objects.filter(user=instance.user_id).exclude(pk=instance.pk).first()
        if cart:
            cart.is_active = True
            cart.save()
