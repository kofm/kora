# Template Tags

## Components

Template Tags that render UI components.
Found in `frontpage.templatetags.components`.

``` html
{% load components %}
```

### `list_page_header`

Render a standardized header for listing views.
The component displays a header consisting of:

* a title
* an optional subtitle
* an optional Create action button

Setting `modal` to True enables modal behaviour on to the Create button (See `modal_attrs` templatetag).

``` html
{% list_page_header "register.PlantVariety" title="Title Override" subtitle="Subtitle" modal=True %}
```

The tag renders `frontpage/partials/list_page_header.html`.

#### Parameters

* `model_label` (`str`, required)
  Django model label in the form `"app_label.ModelName"` or `"app_label.modelname"`
  (e.g. `"register.PlantVariety"`)

* `title` (`str`, optional)
  Override for the page title. Defaults to `model._meta.verbose_name_plural.title()`.

* `subtitle` (`str`, optional)
  Optional subtitle rendered below the title.

* `modal` (`bool`, optional, default `False`)
  Enable modal behavior for the Create action button.

#### Behavior

* The header title defaults to the model’s `verbose_name_plural` if not explicitly provided.
* The Create button is shown only if:
  * the current user has the model's `add` permission, and
  * the model defines a class method `get_create_url()`.
* When `modal=True`, modal-related attributes are added to the Create button.

This templatetag is a simple wrapper around the `ListPageHeader` dataclass. For advanced or view-specific customization, the dataclass can be instantiated directly in the view.

``` python
def a_view(request):
    header = ListPageHeader(
        page_title="Users",
        create_url=reverse("frontpage:user_create"),
        modal=True,
    )
	context = {"my_header": header}
	return TemplateResponse(request, "app/view.html", context)
```

Then, in the view just include the template:

``` html
{% include 'frontpage/partials/list_page_header.html' with header=my_header %}
```

### `detail_page_header`

The `detail_page_header` inclusion tag renders a standardized header for detail views.
It displays a title, optional subtitle, and Update/Delete action buttons.

``` html
{% load components %}
{% detail_page_header instance=object title="Custom Title" subtitle="Overview" subtitle_emphasis=True %}
```

The tag renders `frontpage/partials/detail_page_header.html`.

#### Behavior

* You need to pass a model instance as the first argument, the remaining named arguments are optional.
* The **title** defaults to `str(instance)` unless overridden.
* The **subtitle** is shown directly under the title, and can be emphasized by setting `subtitle_emphasis=True`
* The **update** and **delete** buttons are shown only if:
  * the model defines the methods `get_update_url` and `get_delete_url`
  * the user has the required permissions (`change_model` and `delete_model`)
* If a delete action exists but the object is **not deletable** (`instance.is_deletable == False`):
  * the delete button is rendered in a disabled state,
  * an info tooltip is shown with a configurable message (by defining the model `@property`: `cant_delete_msg`); the default message is "You can't remove this entry because it is associated to other data.".

#### Parameters

* `instance`: Object displayed on the detail page. Used to derive permissions, action URLs, and the default title.
* `title`: (`str`, optional) Custom page title. Defaults to `str(instance)`.
* `subtitle`: (`str`, optional) Optional subtitle rendered below the title.
* `subtitle_emphasis`: (`bool`, optional) If true, render the subtitle with emphasis (italic).
