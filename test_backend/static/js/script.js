document.getElementById("uploadForm").addEventListener("submit", function(event) {
    event.preventDefault();
    
    var formData = new FormData();
    var fileInput = document.getElementById("imgFile");
    var file = fileInput.files[0];
    formData.append("imgFile", file);
    
    // var progressBarContainer = document.getElementById("progressBarContainer");
    // progressBarContainer.classList.remove("hidden");
    // var progressBar = document.getElementById("progressBar");
    // progressBar.style.width = "0%";
    
    fetch("/persons_upload", {
        method: "POST",
        body: formData,
        headers: {
            "enctype": "multipart/form-data"
        },
        // onUploadProgress: function(progressEvent) {
        //     var progress = Math.round((progressEvent.loaded / progressEvent.total) * 100);
        //     progressBar.style.width = progress + "%";
        // }
    })
    .then(response => response.json())
    .then(data => {
        var messageContainer = document.getElementById("messageContainer");
        var messageText = document.getElementById("message");
        if (data.success) {
            messageText.innerText = "Upload successful";
            messageContainer.classList.remove("hidden");
        } else {
            messageText.innerText = "Upload failed";
            messageContainer.classList.remove("hidden");
        }
    })
    .catch(error => console.error(error));
});
