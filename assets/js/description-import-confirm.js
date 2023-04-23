import "../scss/tom-select.scss";
import TomSelect from "tom-select";

const varietiesData = JSON.parse(
  document.getElementById("varieties-data").textContent
);

document.querySelectorAll(".ts").forEach((el) => {
  const initialValue = el.value;
  const inputVarietyID = el.parentElement.nextElementSibling;

  let settings = {
    options: varietiesData,
    valueField: "pk",
    labelField: "name",
    searchField: ["name"],
    items: [ inputVarietyID.value, ],
    maxItems: 1,
    selectOnTab: true,
    create: true,
    onItemAdd: function (value, $item) {
      if (this.userOptions.hasOwnProperty(value)) {
        console.log("created");
        inputVarietyID.value = '';
      } else {
        console.log("Selected");
        inputVarietyID.value = value;
      }
    },
    render: {
      option: function (data, escape) {
        var option;
        if (data.breeder__name) {
          option =
            "<div>" +
            '<span class="title">' +
            escape(data.name) +
            "</span>" +
            '<span class="url">' +
            escape(data.breeder__name) +
            "</span>" +
            "</div>";
        } else {
          option =
            "<div>" +
            '<span class="title">' +
            escape(data.name) +
            "</span>" +
            '<span class="url">&nbsp;</span>' +
            "</div>";
        }
        return option;
      },
    },
  };
  var tomSelectInstance = new TomSelect(el, settings);
  // Check if the <input/> value is in the varietiesData obj
  const found = varietiesData.find((element) => element.pk == el.value);
  // Otherwise add it
  if (!found) {
    console.log(initialValue);
    tomSelectInstance.addOption({ pk: initialValue, name: initialValue }, true);
    tomSelectInstance.addItem(initialValue, true);
  }
});
