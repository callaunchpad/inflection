function uploadFile(form) {
  var req = new XMLHttpRequest();
  // oReq.open("POST", "upload_static_file", true);
  // oReq.onload = function (oEvent) {
  //   if (oReq.status == 200) {
  //     oOutput.innerHTML = "Uploaded!";
  //     console.log(oReq.response)
  //   } else {
  //     oOutput.innerHTML = "Error occurred when trying to upload your file.<br \/>";
  //   }
  // };
  // oOutput.innerHTML = "Sending file!";
  // console.log("Sending file!")
  // oReq.send("name=test");
  req.open('POST', "upload_static_file", true);
  req.setRequestHeader('content-type', 'application/x-www-form-urlencoded;charset=UTF-8');
  req.send("name=" + speech);
}