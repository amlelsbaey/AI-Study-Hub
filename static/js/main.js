const sidebar = document.getElementById("sidebar");
const sidebarToggle = document.getElementById("sidebarToggle");
const menuBtn = document.getElementById("menuBtn");
const overlay = document.getElementById("sidebarOverlay");
const darkModeToggle = document.getElementById("darkModeToggle");

function toggleMobileSidebar(open) {
    if (!sidebar || !overlay) {
        return;
    }

    sidebar.classList.toggle("open", open);
    overlay.classList.toggle("active", open);
}

function applyTheme(theme) {
    const isDark = theme === "dark";

    document.body.classList.toggle("dark-mode", isDark);

    if (darkModeToggle) {
        darkModeToggle.checked = isDark;
    }
}

function setupSidebar() {
    if (sidebarToggle) {
        sidebarToggle.addEventListener("click", function () {
            if (window.innerWidth > 900) {
                document.body.classList.toggle(
                    "sidebar-collapsed"
                );
            } else {
                toggleMobileSidebar(false);
            }
        });
    }

    if (menuBtn) {
        menuBtn.addEventListener("click", function () {
            toggleMobileSidebar(true);
        });
    }

    if (overlay) {
        overlay.addEventListener("click", function () {
            toggleMobileSidebar(false);
        });
    }
}

function setupDarkMode() {
    const savedTheme =
        localStorage.getItem("theme") || "light";

    applyTheme(savedTheme);

    if (darkModeToggle) {
        darkModeToggle.addEventListener(
            "change",
            function () {
                const newTheme =
                    this.checked ? "dark" : "light";

                localStorage.setItem(
                    "theme",
                    newTheme
                );

                applyTheme(newTheme);
            }
        );
    }
}

setupSidebar();
setupDarkMode();
