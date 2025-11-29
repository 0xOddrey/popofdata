from .models import SiteSettings


def site_settings(request):
    try:
        settings = SiteSettings.objects.first()
    except:
        settings = None

    if not settings:
        settings = {
            'site_name': 'Pop-of-Data',
            'tagline': 'Data Science for Pop Culture',
            'hero_image': 'https://popofdata1.s3.amazonaws.com/static/img/pop_of_data.jpg',
            'favicon': 'https://popofdata1.s3.amazonaws.com/static/img/smallpop.png',
            'author_name': 'Audrey Taylor-Akwenye',
            'author_title': 'Data Scientist, Educator, Entrepreneur',
            'author_image': 'https://popofdata1.s3.amazonaws.com/static/img/IMG_0601.jpg',
            'twitter_url': 'https://twitter.com/audreyakwenye',
            'instagram_url': 'https://www.instagram.com/audreyakwenye',
            'github_url': 'https://github.com/audreyakwenye',
        }

    return {'site_settings': settings}
