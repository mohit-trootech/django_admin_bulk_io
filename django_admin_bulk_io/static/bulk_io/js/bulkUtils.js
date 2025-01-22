/**
 * Utility functions for bulk actions
 */
const actionToggle = "#action-toggle";
const selectedAction = "[name=_selected_action]";
const bulkIOFile = "#bulk-io-fileinput";
const BulkIOAdminModal = "#bulkIoAdminModal";

/**
 * function to handle the ajax request to export the selected rows
 * @param event event object
 * @param url backend export url
 */
const bulkIOExport = async (event, url) => {
  event.preventDefault();
  const selectAll = document.querySelector(actionToggle);
  const allActions = document.querySelectorAll(selectedAction);

  /**Check if allActions Available */
  if (allActions) {
    const selectedActions = [...allActions].filter((item) => {
      return item.checked && item;
    });
    if (selectedActions) {
      const selectedIds = [...selectedActions]
        .map((item) => {
          return item.value;
        })
        .join(",");
      const formData = new FormData();
      formData.append("selectedIds", selectedIds);

      bulkIOPostRequest(url, formData, bulkIOExportSuccess);
    }
  }
};

/**
 * callback success function to trigger download process
 * @param response the XMLHttpRequest response object
 */
const bulkIOExportSuccess = (response) => {
  const downloadLink = document.createElement("a");
  downloadLink.href = response.file.url;
  downloadLink.target = "_blank";
  downloadLink.click();
};

/**
 * function to handle the ajax request to send the file for import
 * @param event event object
 * @param url backend import url
 */
const bulkIOImport = async (event, url) => {
  event.preventDefault();
  const bulkIoFileInput = document.querySelector(bulkIOFile);
  if (bulkIoFileInput.files.length) {
    const files = bulkIoFileInput.files;
    const formData = new FormData();
    formData.append("file", files[0]);
    bulkIOPostRequest(url, formData, bulkIOImportSuccess);
  } else {
    triggerToast("Warning", "Please Choose a File First");
  }
};
/**
 * callback success function to trigger reload process
 * @param response the XMLHttpRequest response object
 */
const bulkIOImportSuccess = (response) => {
  $(BulkIOAdminModal).fadeOut(500);
  $(bulkIOFile).val("");
};
