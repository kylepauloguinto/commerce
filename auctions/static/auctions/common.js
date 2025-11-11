document.addEventListener("DOMContentLoaded", function () {
  if ("serviceWorker" in navigator) {
    navigator.serviceWorker
      .register("/static/auctions/service-worker.js")
      .then((reg) => console.log("Service Worker registered", reg))
      .catch((err) => console.log("Service Worker error", err));
  }
  if (window.location.pathname.endsWith("/register")) {
    $("#autoModal").modal("show");
  }
  // japanese codes
  $(".jap").hide();
  $("#lang").on("click", function () {
    var $button = $(this);
    let isPressed = $(this).attr("aria-pressed") === "true";
    if (isPressed) {
      $button.text("日本語版");
      $("#all").show();
      $(".jap").hide();
      $(".eng").show();
    } else {
      $button.text("English Version");
      $("#all-jap").show();
      $(".jap").show();
      $(".eng").hide();
    }
  });

  if (window.location.pathname.endsWith("/login")) {
    const form = document.getElementById("login-form");
    const loader = document.getElementById("loader");
    const button = document.getElementsByClassName("submit")[0];

    button.onclick = function () {
      // show loader
      loader.style.display = "flex";
    };
  }

  // Close dropdown when clicking outside
  window.onclick = function (event) {
    if (!event.target.matches(".dropdown-btn")) {
      document.querySelectorAll(".dropdown-content").forEach((menu) => {
        menu.classList.remove("show");
      });
    }
  };

  // Get all nav links
  const navLinks = document.querySelectorAll("nav a");

  navLinks.forEach((link) => {
    link.addEventListener("click", () => {
      // Remove active class from all links
      navLinks.forEach((l) => l.classList.remove("active"));

      // Add active class to clicked link
      link.classList.add("active");
    });
  });

  let activeLink;
  let activeLinkBottom;
  // Adding active class depends on
  if (window.location.pathname.endsWith("/")) {
    activeLink = document.querySelector("#nav-active");
    activeLinkBottom = document.querySelector("#nav-active-bottom");
    activeLink.classList.add("active");
    activeLinkBottom.classList.add("active");
  } else if (window.location.pathname.endsWith("/allList")) {
    activeLink = document.querySelector("#nav-all");
    activeLinkBottom = document.querySelector("#nav-all-bottom");
    activeLink.classList.add("active");
    activeLinkBottom.classList.add("active");
  } else if (window.location.pathname.endsWith("/create")) {
    activeLink = document.querySelector("#nav-create");
    activeLinkBottom = document.querySelector("#nav-create-bottom");
    activeLink.classList.add("active");
    activeLinkBottom.classList.add("active");
  }
});

function toggleDropdown() {
  document.getElementById("dropdownMenu").classList.toggle("show");
}
