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

// Dark mode with persistence
const themeToggle = document.getElementById("themeToggle");

if (localStorage.getItem("theme") === "dark") {
    document.body.classList.add("dark-mode");
}

if (themeToggle) {
    themeToggle.addEventListener("click", () => {
        document.body.classList.toggle("dark-mode");
        
        if (document.body.classList.contains("dark-mode")) {
            localStorage.setItem("theme", "dark");
        } else {
            localStorage.setItem("theme", "light");
        }
    });
}