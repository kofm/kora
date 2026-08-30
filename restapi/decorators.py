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


def document_idempotent_target_create(serializer_class):
    return extend_schema_view(
        create=extend_schema(
            description=(
                "Creates a target idempotently. Returns `201` when created, or `200` when an identical target "
                "already exists."
            ),
            responses={200: serializer_class, 201: serializer_class},
        ),
        bulk=extend_schema(
            description=(
                "Creates targets atomically and idempotently. Returns `201` when at least one target is created, "
                "or `200` when all requested targets already exist. Results preserve request order."
            ),
            request=serializer_class(many=True),
            responses={200: serializer_class(many=True), 201: serializer_class(many=True)},
        ),
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
