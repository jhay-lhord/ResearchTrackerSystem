document
  .getElementById("uploadForm")
  .addEventListener("submit", function (event) {
    const fileInput = document.querySelector("#formFile");
    const fileError = document.querySelector("#file-error");
    if (!fileInput.files.length) {
      event.preventDefault(); // Prevent form submission
      fileError.textContent = "Please select a file.";
    } else {
      fileError.textContent = ""; 
    }
  });