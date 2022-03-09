const storageSelect = document.getElementById("storage-select");
const storagePositionSelect = document.getElementById(
  "storage-position-select"
);

storageSelect.addEventListener("change", async function () {
  const url = storagePositionSelect
    .getAttribute("data-url")
    .replace("0", storageSelect.value);
  const response = await fetch(url, {
    headers: {
      Accept: "application/json",
    },
  });

  const storagePositionObjects = await response.json();
  storagePositionSelect.length = 0;
  storagePositionObjects.forEach(
    (element) =>
      (storagePositionSelect.options[storagePositionSelect.length] = new Option(
        element.name,
        element.id
      ))
  );
});
