function changePicture() {
  // trigger the click event on the file input element
  document.getElementById("picture").click();

  // listen for the change event on the file input element and save the file name to assets folder and show image to image tag
  document.getElementById("picture").onchange = function () {
    // get the file name
    var file = this.files[0];
    // create a new FileReader
    var reader = new FileReader();
    // load the local file
    reader.readAsDataURL(file);
    // set the image data as background of body
    reader.onload = function (e) {
      document.getElementById("image").src = e.target.result;
    };
  };
}

function saveProfile(e) {
  e.preventDefault();
  // get the form data
  var formData = new FormData(document.getElementById("profile-form"));
  // send the form data to the server
  console.log(formData);
  var xhr = new XMLHttpRequest();
  xhr.open("post", "/saveProfile", true);
  xhr.send(formData);
  // listen for the response
  xhr.onreadystatechange = function () {
    if (xhr.readyState == 4 && xhr.status == 200) {
      // show the response
      alert(xhr.responseText);
    }
  };
}

async function saveFormData(e) {
  e.preventDefault();

  //   get form data
  var formData = new FormData(document.getElementById("profile-form"));

  //   change file to base64
  var file = formData.get("picture");
  if (file) {
    const base64 = await readFileAsBase64(file);
    formData.set("picture", base64);
  }

  // get data from localStorage
  var data = JSON.parse(localStorage.getItem("customer")) || [];

  //   set localStorage array of objects
  data.push(Object.fromEntries(formData.entries()));

  // save data to localStorage
  localStorage.setItem("customer", JSON.stringify(data));

  modalOverlay.classList.remove("hidden");
  modalOverlay.classList.add("flex");

  // Trigger enter animation
  setTimeout(() => {
    modalContent.classList.add("modal-enter-active");
  }, 10);
}

function readFileAsBase64(file) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();

    reader.onloadend = () => {
      resolve(reader.result); // Base64 string is in reader.result
    };

    reader.onerror = () => {
      reject("Error reading file.");
    };

    reader.readAsDataURL(file); // Read file as Data URL (base64)
  });
}

document
  .getElementById("profile-form")
  .addEventListener("submit", saveFormData);

document.addEventListener("DOMContentLoaded", function () {
  // JavaScript to handle modal display with animation
  const modalOverlay = document.getElementById("modalOverlay");
  const modalContent = document.getElementById("modalContent");
  const closeModalButton = document.getElementById("closeModal");

  // Hide the modal with animation
  closeModalButton.addEventListener("click", () => {
    modalContent.classList.remove("modal-enter-active");
    modalContent.classList.add("modal-exit-active");

    setTimeout(() => {
      modalOverlay.classList.remove("flex");
      modalOverlay.classList.add("hidden");
      modalContent.classList.remove("modal-exit-active");
    }, 300); // Match the transition duration
  });

  // Optional: close modal when clicking outside the modal content
  modalOverlay.addEventListener("click", (event) => {
    if (event.target === modalOverlay) {
      modalContent.classList.remove("modal-enter-active");
      modalContent.classList.add("modal-exit-active");

      setTimeout(() => {
        modalOverlay.classList.remove("flex");
        modalOverlay.classList.add("hidden");
        modalContent.classList.remove("modal-exit-active");
      }, 300); // Match the transition duration
    }
  });
});
