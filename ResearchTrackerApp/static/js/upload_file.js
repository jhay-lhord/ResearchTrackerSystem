const uploadButtons = document.querySelectorAll("#upload-btn");

uploadButtons.forEach(function (uploadButton) {
  uploadButton.addEventListener("click", function () {

    const researchId = uploadButton.getAttribute("data-research-id");
    const researchInput = document.getElementById("research-input");
    researchInput.value = researchId;
  });
});
