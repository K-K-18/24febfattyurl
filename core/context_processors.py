from django.conf import settings

from django.core.cache import cache

def site_stats(request):
    stats = cache.get('site_stats')
    if stats is None:
        from .models import Link
        from django.utils import timezone
        today = timezone.now().date()
        stats = {
            'total_links': Link.objects.count(),
            'links_today': Link.objects.filter(created_at__date=today).count(),
        }
        cache.set('site_stats', stats, 300)  # Cache 5 minutes
    return {
        'site_stats': stats,
        'site_url': (
            f"{request.scheme}://{request.site.domain}"
            if getattr(request, 'site', None) and getattr(request.site, 'domain', None)
            else request.build_absolute_uri('/').rstrip('/')
        ),
    }


def social_provider_status(request):
    google_provider = settings.SOCIALACCOUNT_PROVIDERS.get('google', {}).get('APP', {})
    github_provider = settings.SOCIALACCOUNT_PROVIDERS.get('github', {}).get('APP', {})

    return {
        'social_providers': {
            'google': bool(google_provider.get('client_id', '').strip()),
            'github': bool(github_provider.get('secret', '').strip()) and bool(github_provider.get('client_id', '').strip()),
        }
    }
