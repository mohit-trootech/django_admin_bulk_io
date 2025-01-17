/* Bulk IO Ajax Request Ultility */

const bulkIOPostRequest = (url, data, callback) => {
  bulkIoAjaxRequest(url, "POST", data, callback);
};

const bulkIoAjaxRequest = (url, type, data, callback) => {
  // Send Ajax Request to Send FormData
  $.ajax({
    url: url,
    type: type,
    data: data,
    contentType: "application/json",
    processData: false,
    contentType: false,
    success: (responseData) => {
      callback && callback(responseData);
    },
    error: (error) => {
      bulkIoCreateBootstrapToast(
        (error.responseJSON && error.responseJSON.message) || error.responseText
      );
    },
  });
};
