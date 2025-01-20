/* Bulk IO Ajax Request Ultility */

const bulkIOGetRequest = (url, callback) => {
  bulkIoAjaxRequest(url, "GET", null, callback)
}

const bulkIOPostRequest = (url, data, callback) => {
  bulkIoAjaxRequest(url, "POST", data, callback);
};

const bulkIoAjaxRequest = (url, type, data, callback) => {
  // Send Ajax Request to Send FormData
  $.ajax({
    url: url,
    type: type,
    data: data,
    success: (responseData) => {
      console.log(responseData)
      callback && callback(responseData);
    },
    error: (error) => {
      console.error(error)
      // bulkIoCreateBootstrapToast(
      //   (error.responseJSON && error.responseJSON.message) || error.responseText
      // );
    },
  });
};
