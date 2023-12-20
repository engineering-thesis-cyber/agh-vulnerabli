function logout(){
    window.location.href = '/logout/';
}

function description(){
    text = "Click create button for the lab that you are interested in. After finishing lab click delete button.\
    If you think given lab needs reset simply choose one from the dropdown menu and click <i>Reset</i> button.\
    Wait for about 1-2min.";
    text_place = document.getElementById("response");
    text_place.innerHTML = text;
}

function openPopup(markdownTextPath) {
    var popup = document.getElementById("popup");
    var markdownContent = document.getElementById("markdown-content");
    
    fetch(markdownTextPath)
    .then(response => response.text())
    .then(data => {
      var htmlContent = marked.parse(data);
      markdownContent.innerHTML = htmlContent;
      popup.style.display = "block";
    })
    .catch(error => {
      console.error("Error fetching file:", error);
    });
}

function closePopup() {
    var popup = document.getElementById("popup");
    popup.style.display = "none";
}