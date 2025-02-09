function uploadImage() {
    const fileInput = document.getElementById("fileInput");
    if (!fileInput.files.length) {
        alert("Valitse ensin kuva!");
        return;
    }

    const formData = new FormData();
    formData.append("file", fileInput.files[0]);

    fetch("http://127.0.0.1:5000/upload", {
        method: "POST",
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("message").textContent = data.message;
        if (data.image_url) {
            document.getElementById("resultImage").src = "http://127.0.0.1:5000" + data.image_url;
            document.getElementById("resultImage").style.display = "block";
        }
    })
    .catch(error => console.error("Error:", error));
}
