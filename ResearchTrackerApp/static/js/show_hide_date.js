
// Disable all date fields initially
const hideFields = document.querySelectorAll(".hide-field");
hideFields.forEach(function (dateField) {
  dateField.style.display = "none";
});

// Enable the date field based on the selected status
const statusField = document.getElementById("id_Status");
const journalSelect = document.getElementById("id_Journal_Type");

statusField.addEventListener("change", function () {
  var selectedStatus = this.value;
  hideFields.forEach(function (hideField) {
    hideField.style.display = "none";
    hideField.disabled = true;
  });
  if (selectedStatus === "Presented") {
    document.getElementById("datePresented").style.display = "block";
  }
  if (selectedStatus === "Ongoing") {
    document.getElementById("dateOngoing").style.display = "block";
    // document.getElementById("datePresented").style.display = "block";
  }
  if (selectedStatus === "Conducted") {
    document.getElementById("dateConducted").style.display = "block";
    // document.getElementById("datePresented").style.display = "block";
    // document.getElementById("dateOngoing").style.display = "block";
  }

  if (selectedStatus === "Published") {
    document.getElementById("datePublished").style.display = "block";
    // document.getElementById("dateOngoing").style.display = "block";
    // document.getElementById("dateConducted").style.display = "block";
    document.getElementById("ispnNo").style.display = "block";
    document.getElementById("publisherName").style.display = "block";
    document.getElementById("journalType").style.display = "block";
  }
});

journalSelect.addEventListener("change", (event) => {
  const selectedJournal = event.target.value;

  if (selectedJournal === "International") {
    document.getElementById("journalIndex").style.display = "block";
  } else {
    document.getElementById("journalIndex").style.display = "none";
  }
});
