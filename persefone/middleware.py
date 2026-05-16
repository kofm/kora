# persefone/middleware.py
from pathlib import Path

from django.conf import settings
from pyinstrument import Profiler


class PyInstrumentMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not settings.DEBUG or request.GET.get("profile") != "1":
            return self.get_response(request)

        profiler = Profiler()
        profiler.start()

        response = self.get_response(request)

        # Usually already rendered by Django, but harmless for TemplateResponse checks
        if hasattr(response, "render") and not response.is_rendered:
            response.render()

        profiler.stop()

        text_report = profiler.output_text(
            unicode=True,
            color=False,
            show_all=True,
            timeline=True,
        )

        out = Path(settings.BASE_DIR) / "tmp" / "pyinstrument.txt"
        out.parent.mkdir(exist_ok=True)
        out.write_text(text_report, encoding="utf-8")

        print("\n" + "=" * 80)
        print("PYINSTRUMENT REPORT")
        print("=" * 80)
        print(text_report)
        print("=" * 80)
        print(f"Saved to: {out}")
        print("=" * 80 + "\n")

        return response
