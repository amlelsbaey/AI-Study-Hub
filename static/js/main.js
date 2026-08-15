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
};

// =========================
// DARK MODE
// =========================

const darkModeToggle = document.getElementById("darkModeToggle");

function applyTheme(theme) {
    if (theme === "dark") {
        document.body.classList.add("dark-mode");

        if (darkModeToggle) {
            darkModeToggle.checked = true;
        }
    } else {
        document.body.classList.remove("dark-mode");

        if (darkModeToggle) {
            darkModeToggle.checked = false;
        }
    }
}


// Apply saved theme immediately
const savedTheme = localStorage.getItem("theme") || "light";

applyTheme(savedTheme);


// Toggle dark mode from Settings
if (darkModeToggle) {

    darkModeToggle.addEventListener("change", function () {

        const newTheme = this.checked ? "dark" : "light";

        localStorage.setItem("theme", newTheme);

        applyTheme(newTheme);

    });

}