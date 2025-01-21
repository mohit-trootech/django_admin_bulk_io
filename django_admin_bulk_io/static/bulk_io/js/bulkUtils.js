/* Bulk IO Utils */
/**Constants */
const actionToggle = "#action-toggle"
const selectedAction = "[name=_selected_action]"
const bulkIOFile = "#bulk-io-fileinput"
/* Handle Bulk Export Form Submit */
const bulkIOExport = async (event, url) => {
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
      const formData = new FormData();
      formData.append("selectedIds", selectedIds);

      bulkIOPostRequest(url, formData, bulkIOExportSuccess);
    }
  }
};

const bulkIOExportSuccess = (response) => {
  const downloadLink = document.createElement('a');
  downloadLink.href = response.file.url;
  downloadLink.target = "_blank"
  downloadLink.click();
};

const bulkIOImport = async (event, url) => {
  event.preventDefault();
  const bulkIoFileInput = document.querySelector(bulkIOFile);
  if (bulkIoFileInput.files.length) {
    const files = bulkIoFileInput.files
    const formData = new FormData();
    formData.append("file", files[0]);
    bulkIOPostRequest(url, formData, bulkIOImportSuccess);
  }
  else {
    triggerToast("Warning", "Please Choose a File First")
  }

}
const bulkIOImportSuccess = (response) => {
  console.log(response)
}