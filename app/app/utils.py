from django.apps import apps
from django.utils.crypto import get_random_string
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer


def generate_code(app_label, model_name, unique_field, length=3):
    Model = apps.get_model(app_label, model_name)

    rand = get_random_string(length).upper()
    while Model.objects.filter(**{unique_field: rand}).exists():
        rand = get_random_string(length).upper()
    
    return rand


class CustomJsonRenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        response = renderer_context['response']
        if response.exception:
            res_data = {'status': False, 'errors': data}
        else:
            res_data = {'status': True, 'data': data}

        return super().render(res_data, accepted_media_type, renderer_context)


class PaginatorMixin:
    def paginate_results(self, queryset):
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
