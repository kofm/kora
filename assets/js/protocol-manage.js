import $ from 'jquery'
// This function adds a new trait dynamically
$("#add_trait").click(function () {
  // Get the number of actual total trait fields. Needed for processing
  // with Django
  var form_idx = $("#id_traits-TOTAL_FORMS").val();
  console.log(form_idx)
  // Get the html of empty formset and replace __prefix__ with the actual
  // number of forms. Since formset indexes start from 0, there is no need
  // to increment.
  var replacement = $("#empty_form")
    .html()
    .replace(/__prefix__/g, form_idx)
    .replace(/([a-z0-9_\-]*?)(-states-)(\d+)/g, "$1$20");
  // Append the html at the end of the form (which has id = form_set
  $("#form_set").append(replacement);
  // Increment the total number of forms
  $("#id_traits-TOTAL_FORMS").val(parseInt(form_idx) + 1);
});

// This function add a state dynamically WITHIN an existing trait field
// "on" is used to work also in dynamically generated elements
$(document.body).on("click", ".add_state", function () {
  // Store the actual number of states within the trait form
  var form_idx = $(this)
    .closest(".states")
    .find("input:hidden[name$='TOTAL_FORMS']")
    .val();
  // Select the last state within the form
  var prev_state = $(this)
    .parent(".card-body")
    .siblings(".list-group")
    .children(".state-form")
    .last();
  // Edit the html to increment the field number, using the total form
  // number; as before, since the index starts from 0 there is no need
  // to increment the value
  var new_state = prev_state
    .prop("outerHTML")
    .replace(/([a-z0-9_\-]*?)(-states-)(\d+)/g, "$1$2" + form_idx);
  // Append the html after the last state field
  prev_state.after(new_state);
  $(this)
    .parent(".card-body")
    .siblings(".list-group")
    .children(".state-form")
    .last()
    .find("input[id$='numeric_id']")
    .focus();
  // Increment the total number of fields (within the current trait field)
  $(this)
    .closest(".states")
    .find("input:hidden[name$='TOTAL_FORMS']")
    .val(parseInt(form_idx) + 1);
});
