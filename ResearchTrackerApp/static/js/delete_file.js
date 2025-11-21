document.addEventListener("DOMContentLoaded", function () {
  const container = document.getElementsByClassName("table")[0];
  container.addEventListener("click", function (event) {
    if (event.target.classList.contains("delete-research-link")) {
      event.preventDefault();
      const researchId = event.target.getAttribute("data-research-id");
      deleteResearch(researchId);
    }
  });

  function deleteResearch(researchId) {
    const confirmDeleteButton = document.getElementById("confirmDelete");

    confirmDeleteButton.addEventListener("click", function () {
      // Hide the modal
      delete_modal.classList.remove("show");
      delete_modal.style.display = "none";

      fetch(`/delete_file/${researchId}/`, {
        method: "POST",
        headers: {
          "X-CSRFToken": getCookie("csrftoken"),
        },
      })
        .then(function (response) {
          if (response.status === 200) {
            location.reload();
          } else {
            console.error("Failed to delete research");
          }
        })
        .catch(function (error) {
          console.error("Error:", error);
        });
    });
  }

  // Function to get CSRF token from cookies
  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
      const cookies = document.cookie.split(";");
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        // Search for the csrf token cookie
        if (cookie.startsWith(name + "=")) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }
});
