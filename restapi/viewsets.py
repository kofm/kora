import json

from django.core.serializers.json import DjangoJSONEncoder
from django.http import StreamingHttpResponse
from drf_spectacular.utils import OpenApiResponse, OpenApiTypes, extend_schema
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.serializers import ValidationError


class BulkCreateActionMixin:
    @action(detail=False, methods=["post"], url_path="bulk", filter_backends=[], pagination_class=None)
    def bulk(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        self.perform_bulk_create(serializer)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def perform_bulk_create(self, serializer):
        serializer.save()


class JSONLExportMixin:
    jsonl_export_chunk_size = 1000
    jsonl_export_filename = None
    jsonl_export_serializer_class = None

    def get_jsonl_export_queryset(self):
        queryset = self.filter_queryset(self.get_queryset())

        if not queryset.ordered:
            queryset = queryset.order_by("pk")

        return queryset

    def get_jsonl_export_serializer_class(self):
        return self.jsonl_export_serializer_class or self.get_serializer_class()

    def get_jsonl_export_filename(self):
        if self.jsonl_export_filename:
            return self.jsonl_export_filename

        if hasattr(self, "basename"):
            return f"{self.basename}.jsonl"

        model = self.get_queryset().model
        return f"{model._meta.model_name}.jsonl"

    def iter_jsonl_export(self, queryset):
        serializer_class = self.get_jsonl_export_serializer_class()

        for obj in queryset.iterator(chunk_size=self.jsonl_export_chunk_size):
            serializer = serializer_class(
                obj,
                context=self.get_serializer_context(),
            )
            yield json.dumps(
                serializer.data,
                cls=DjangoJSONEncoder,
                ensure_ascii=False,
            )
            yield "\n"

    @extend_schema(
        description=("Export the full filtered result set as newline-delimited JSON."),
        responses={
            (200, "application/x-ndjson"): OpenApiResponse(
                response=OpenApiTypes.STR,
                description="Newline-delimited JSON stream.",
            )
        },
    )
    @action(detail=False, methods=["get"], url_path="export-jsonl")
    def export_jsonl(self, request, *args, **kwargs):
        queryset = self.get_jsonl_export_queryset()

        response = StreamingHttpResponse(
            self.iter_jsonl_export(queryset),
            content_type="application/x-ndjson; charset=utf-8",
        )
        response["Content-Disposition"] = f'attachment; filename="{self.get_jsonl_export_filename()}"'
        return response


class KoraViewSet(BulkCreateActionMixin, JSONLExportMixin, viewsets.ModelViewSet):
    pass


class ExcelImportActionMixin:
    excel_import_serializer_class = None
    excel_import_description = None

    def perform_excel_import_create(self, objs) -> int:
        raise NotImplementedError("The creation method for the `excel_import` action should be defined.")

    def excel_import(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            objs = serializer.save()
        except ValidationError as exc:
            errors = serializer.catch_row_serializer_errors(exc)
            return Response(errors, status.HTTP_400_BAD_REQUEST)

        if not objs:
            return Response({"imported_rows": 0}, status.HTTP_200_OK)

        created_count = self.perform_excel_import_create(objs)

        return Response({"imported_rows": created_count}, status.HTTP_201_CREATED)
