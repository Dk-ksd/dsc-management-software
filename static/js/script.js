const hamBurger = document.querySelector(".toggle-btn");

hamBurger.addEventListener("click", function () {
  const sidebar = document.querySelector("#sidebar");
  sidebar.classList.toggle("expand");

  const mainContent = document.querySelector(".main");
  if (sidebar.classList.contains("expand")) {
    mainContent.style.marginLeft = "260px";
  } else {
    mainContent.style.marginLeft = "70px";
  }
});


