/* Bulk IO Utils */


const bulkExportSubmit = (event, url) => {
    event.preventDefault();
    bulkIOPostRequest(url, new FormData(event.target), bulkExportSubmitSuccess);
}

const bulkExportSubmitSuccess = (response) => {
    bulkIoCreateBootstrapToast(response.message);
}

const bulkIoCreateBootstrapToast = (message) => {
  const toastContainer = document.getElementById("bulkIOLiveToast");
  const toast = new bootstrap.Toast(toastContainer);
  toastContainer.querySelector(".toast-body").innerText = message;
  toast.show();
}