//   customer page
document.addEventListener("DOMContentLoaded", function () {
  // Get the data from localStorage
  var data = JSON.parse(localStorage.getItem("customer")) || [];

  // Get the table element
  var table = document.getElementById("customer-table");

  // Loop through the data and add it to the table
  data.forEach(function (customer) {
    var row = table.insertRow(-1);
    row.classList.add(
      "bg-white",
      "border-b",
      "dark:bg-gray-800",
      "dark:border-gray-700"
    );
    var cell1 = row.insertCell(0);
    cell1.classList.add(
      "px-6",
      "py-4",
      "font-medium",
      "text-gray-900",
      "whitespace-nowrap",
      "dark:text-white"
    );
    var cell2 = row.insertCell(1);
    cell2.classList.add("px-6", "py-4");
    var cell3 = row.insertCell(2);
    cell3.classList.add("px-6", "py-4");
    var cell4 = row.insertCell(3);
    cell4.classList.add("px-6", "py-4");
    var cell5 = row.insertCell(4);
    cell5.classList.add("hidden");
    cell1.innerHTML = customer.username ?? "N/A";
    cell2.innerHTML = customer.full_name ?? "N/A";
    cell3.innerHTML = customer.phone ?? "N/A";
    cell4.innerHTML = `<button class="rounded-xl bg-orange-400 px-4 py-2 mx-auto" onclick="showCustomer(this)">Show</button>`;
    cell5.innerHTML = customer.email ?? "N/A";
  });

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

function showCustomer(e) {
  const modalOverlay = document.getElementById("modalOverlay");
  const modalContent = document.getElementById("modalContent");
  //   const closeModalButton = document.getElementById("closeModal");
  var row = e.closest("tr");
  var cells = row.getElementsByTagName("td");
  var username = cells[0].innerText;
  var fullName = cells[1].innerText;
  var phone = cells[2].innerText;
  var email = cells[4].innerText;

  // split the full name into first and last name
  var name = fullName.split(" ");
  var firstName = name[0];
  var lastName = name[1];

  document.getElementById("customer_id").innerText = `Customer 1`;
  document.getElementById("username").innerText = username ?? "";
  document.getElementById("first_name").innerText = firstName ?? "";
  document.getElementById("last_name").innerText = lastName ?? "";
  document.getElementById("phone").innerText = phone;
  document.getElementById("email").innerText = email;

  modalOverlay.classList.remove("hidden");
  modalOverlay.classList.add("flex");

  // Trigger enter animation
  setTimeout(() => {
    modalContent.classList.add("modal-enter-active");
  }, 10);
}
