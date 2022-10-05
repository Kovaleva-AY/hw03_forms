from django.core.paginator import Paginator

POSTS_NUMBER = 10


def get_page_context(request, queryset):
    paginator = Paginator(queryset, POSTS_NUMBER)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return {
        'paginator': paginator,
        'page_number': page_number,
        'page_obj': page_obj,
    }
