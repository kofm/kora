from drf_spectacular.utils import extend_schema, extend_schema_view

from restapi.serializers.generic import BaseSpreadsheetImportRequestSerializer, ExcelImportResponseSerializer


def document_bulk_create(serializer_class, *, name=None):
    summary = f"Bulk create {name}" if name else "Bulk create"

    return extend_schema_view(
        bulk=extend_schema(
            summary=summary,
            description=(
                "Create multiple objects from a JSON array."
                "Each item follows the same schema as the normal create endpoint."
            ),
            request=serializer_class(many=True),
            responses={201: serializer_class(many=True)},
        )
    )


def document_excel_import(*, name=None, description=None):
    summary = f"Import {name} from an Excel table" if name else "Import from an Excel table"

    def decorator(cls):
        cls.excel_import_description = description

        schema_decorator = extend_schema_view(
            excel_import=extend_schema(
                summary=summary,
                description=description,
                request={"multipart/form-data": BaseSpreadsheetImportRequestSerializer},
                responses=ExcelImportResponseSerializer,
            )
        )

        return schema_decorator(cls)

    return decorator
