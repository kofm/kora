from django.core.paginator import Paginator


def paged_object_list_context(request, queryset, paginate_by):
    paginator = Paginator(queryset, paginate_by)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return {"page_obj": page_obj}
