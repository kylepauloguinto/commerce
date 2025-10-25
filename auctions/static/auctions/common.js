document.addEventListener("DOMContentLoaded", function () {

    // Close dropdown when clicking outside
    window.onclick = function(event) {
        if (!event.target.matches('.dropdown-btn')) {
        document.querySelectorAll(".dropdown-content").forEach(menu => {
            menu.classList.remove('show');
        });
        }
    }

    // Get all nav links
    const navLinks = document.querySelectorAll('nav a');

    navLinks.forEach(link => {
        link.addEventListener('click', () => {
            // Remove active class from all links
            navLinks.forEach(l => l.classList.remove('active'));
            
            // Add active class to clicked link
            link.classList.add('active');
        });
    });

    let activeLink;
    let activeLinkBottom;
    // Adding active class depends on
    if (window.location.pathname.endsWith("/")) {
        activeLink = document.querySelector('#nav-active');
        activeLinkBottom = document.querySelector('#nav-active-bottom');
        activeLink.classList.add('active');
        activeLinkBottom.classList.add('active');
    } else if (window.location.pathname.endsWith("/allList")) {
        activeLink = document.querySelector('#nav-all');
        activeLinkBottom = document.querySelector('#nav-all-bottom');
        activeLink.classList.add('active');
        activeLinkBottom.classList.add('active');
    } else if (window.location.pathname.endsWith("/create")) {
        activeLink = document.querySelector('#nav-create');
        activeLinkBottom = document.querySelector('#nav-create-bottom');
        activeLink.classList.add('active');
        activeLinkBottom.classList.add('active');
    }
}); 

function toggleDropdown() {
    document.getElementById("dropdownMenu").classList.toggle("show");
}

