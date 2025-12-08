# Template Tags

## Components

Template Tags that render UI components.
Found in `frontpage.templatetags.components`.

``` html
{% load components %}
```

### `list_page_header`

Render a standardized header for listing views.
It displays a title, an optional subtitle, and a Create action button.

The tag renders `frontpage/partials/list_page_header.html`.

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
