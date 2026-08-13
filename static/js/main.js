const sidebar = document.getElementById("sidebar");
const sidebarToggle = document.getElementById("sidebarToggle");
const menuBtn = document.getElementById("menuBtn");
const overlay = document.getElementById("sidebarOverlay");


// Desktop collapse
if (sidebarToggle) {
    sidebarToggle.addEventListener("click", () => {

        if (window.innerWidth > 900) {
            document.body.classList.toggle("sidebar-collapsed");
        } else {
            sidebar.classList.remove("open");
            overlay.classList.remove("active");
        }

    });
}


// Mobile open
if (menuBtn) {
    menuBtn.addEventListener("click", () => {

        sidebar.classList.add("open");
        overlay.classList.add("active");

    });
}


// Close mobile sidebar
if (overlay) {
    overlay.addEventListener("click", () => {

        sidebar.classList.remove("open");
        overlay.classList.remove("active");

    });
}

// =========================
// DARK MODE
// =========================

const darkModeToggle = document.getElementById("darkModeToggle");

// Check saved theme
const savedTheme = localStorage.getItem("theme");

if (savedTheme === "dark") {
    document.body.classList.add("dark-mode");

    if (darkModeToggle) {
        darkModeToggle.checked = true;
    }
}


// Toggle from Settings
if (darkModeToggle) {

    darkModeToggle.addEventListener("change", function () {

        if (this.checked) {

            document.body.classList.add("dark-mode");
            localStorage.setItem("theme", "dark");

        } else {

            document.body.classList.remove("dark-mode");
            localStorage.setItem("theme", "light");

        }

    });

}