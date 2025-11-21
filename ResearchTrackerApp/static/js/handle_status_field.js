document.addEventListener("DOMContentLoaded", function () {
  const updateFields = document.querySelectorAll(".update-date");
  const date_label = document.querySelector("#date_label");
  const journalSelect = document.getElementById("Journal_Type");
  const pubFields = document.querySelectorAll(".pub-field");
  const journalIndex = document.querySelector("#journalIndex");


  function hideFabFields() {
    journalIndex.style.display = "none"
    journalIndex.querySelectorAll('input').disabled = true
    pubFields.forEach((pubField) => {
      pubField.style.display = "none";
      if (pubField.querySelector('#date_Published')){
        pubField.querySelector('#date_Published').disabled = true
      }
    });
  }
  function showFabFields() {
    console.log("published")
    pubFields.forEach((pubField) => {
      pubField.style.display = "block";
      if (pubField.querySelector('#date_Published')){
        pubField.querySelector('#date_Published').disabled = false
      }
    });
  }

  function hideAndDisableFields() {
    updateFields.forEach((dateField) => {
      dateField.disabled = true;
      dateField.style.display = "none";
    });
  }

  function showDateField(dateFieldId, labelText) {
    date_label.textContent = labelText;
    document.getElementById(dateFieldId).style.display = "block";
    document.getElementById(dateFieldId).disabled = false;
  }

  // Initial setup
  hideAndDisableFields();
  hideFabFields();

  // Event listeners
  const statusField = document.getElementById("statusSelect");
  statusField.addEventListener("change", function () {
    const selectedStatus = this.value;
    hideAndDisableFields();
    hideFabFields();

    switch (selectedStatus) {
      case "Presented":
        showDateField("date_Presented", "Date Presented");
        break;
      case "Conducted":
        showDateField("date_Conducted", "Date Conducted");
        break;
      case "On-going":
        showDateField("date_Ongoing", "Date On-going");
        break;
      case "Published":
        showDateField("date_Published", "");
        showFabFields();
        break;
    }
  });

  journalSelect.addEventListener("change", (event) => {
    const selectedJournal = event.target.value;
    const journalIndexField = document.getElementById("journalIndex");

    journalIndexField.style.display =
      selectedJournal === "International" ? "block" : "none";
  });
});
