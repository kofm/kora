from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver

from collect.models import Cart

@receiver(pre_save, sender=Cart)
# Signal to make inactive, i.e. active=False, all the other user's Cart
# instances when selecting a new Cart instance
def unique_cart_active(sender, instance, **kwargs):
    if instance.active:
        Cart.objects.filter(user=instance.user).exclude(pk=instance.pk).update(active=False)

@receiver(post_delete, sender=Cart)
def set_new_active_cart(sender, instance, **kwargs):
    if instance.active:
        cart = Cart.objects.filter(user=instance.user).exclude(pk=instance.pk).first()
        if cart:
            cart.active = True
            cart.save()
