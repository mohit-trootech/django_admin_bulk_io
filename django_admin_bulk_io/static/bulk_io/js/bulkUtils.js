/* Bulk IO Utils */
/**Constants */

// Bulk Export Form Submit
const actionToggle = "#action-toggle"
const selectedAction = "[name=_selected_action]"
/*
Handle Bulk Export Form Submit
 */
const bulkExportFormSubmit = async (event, url) => {
  event.preventDefault();
  const selectAll = document.querySelector(actionToggle);
  const allActions = document.querySelectorAll(selectedAction)

  /**Check if allActions Available */
  if (allActions) {
    const selectedActions = [...allActions].filter((item) => {
      return item.checked && item
    });
    if (selectedActions) {
      const selectedIds = [...selectedActions]
        .map((item) => {
          return item.value;
        })
        .join(",");
      bulkIOPostRequest(url, { selectedIds });
    }


  }
};

const bulkExportSubmit = (event, url) => {
  event.preventDefault();
  bulkIOPostRequest(url, new FormData(event.target), bulkExportSubmitSuccess);
};

const bulkExportSubmitSuccess = (response) => {
  bulkIoCreateBootstrapToast(response.message);
};

const bulkIoCreateBootstrapToast = (message) => {
  const toastContainer = document.getElementById("bulkIOLiveToast");
  const toast = new bootstrap.Toast(toastContainer);
  toastContainer.querySelector(".toast-body").innerText = message;
  toast.show();
};
