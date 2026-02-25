from allauth.account.signals import user_signed_up
from django.dispatch import receiver

from .models import Link


@receiver(user_signed_up)
def claim_pending_links(request, user, **kwargs):
    if request is None:
        return

    pending_link_ids = request.session.get('pending_link_ids', [])
    request.session.pop('pending_link_ids', None)

    if not isinstance(pending_link_ids, list):
        return

    valid_ids = []
    for link_id in pending_link_ids:
        try:
            valid_ids.append(int(link_id))
        except (TypeError, ValueError):
            continue

    if not valid_ids:
        return

    Link.objects.filter(
        id__in=valid_ids,
        user__isnull=True,
    ).update(user=user)
