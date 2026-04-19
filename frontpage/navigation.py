from django.template.loader import render_to_string


class BasePrevNextNav:
    prev_template_name = "frontpage/partials/prev_nav.html"
    next_template_name = "frontpage/partials/next_nav.html"

    def __init__(self, instance) -> None:
        assert hasattr(instance, "previous"), (
            f"The instance passed to {self.__class__.__name__} doesn't have a previous() method."
        )
        assert hasattr(instance, "next"), (
            f"The instance passed to {self.__class__.__name__} doesn't have a next() method."
        )
        self.previous = instance.previous()
        self.next = instance.next()

    def render_next(self):
        return render_to_string(self.next_template_name, {"next": self.next})

    def render_previous(self):
        return render_to_string(self.prev_template_name, {"prev": self.previous})
