document.addEventListener("DOMContentLoaded", function () {
    const searchInput = document.getElementById("liveSearchNotes");
    const categoryFilter = document.getElementById("categoryFilterNotes");
    const noteCards = document.querySelectorAll(".note-card");

    function filterNotes() {
        const query = searchInput.value.toLowerCase().trim();
        const selectedCategory = categoryFilter.value.toLowerCase().trim();

        noteCards.forEach(function (card) {
            const text = card.textContent.toLowerCase();
            const category = card.getAttribute("data-category");

            const matchesSearch = text.includes(query);
            const matchesCategory =
                !selectedCategory ||
                category === selectedCategory;

            card.style.display =
                matchesSearch && matchesCategory
                    ? "flex"
                    : "none";
        });
    }

    if (searchInput) {
        searchInput.addEventListener("input", filterNotes);
    }

    if (categoryFilter) {
        categoryFilter.addEventListener("change", filterNotes);
    }
});

function openModal(id) {
    const modal = document.getElementById(id);

    if (!modal) {
        return;
    }

    modal.style.display = "flex";
    document.body.style.overflow = "hidden";
}

function closeModal(id) {
    const modal = document.getElementById(id);

    if (!modal) {
        return;
    }

    modal.style.display = "none";
    document.body.style.overflow = "";
}

function closeModalOutside(event, id) {
    if (event.target.id === id) {
        closeModal(id);
    }
}

function toggleInline(id) {
    const box = document.getElementById(id);

    if (!box) {
        return;
    }

    if (box.style.display === "block") {
        box.style.display = "none";
    } else {
        box.style.display = "block";
    }
}

function getCSRFToken() {
    const input = document.querySelector(
        "[name=csrfmiddlewaretoken]"
    );

    return input ? input.value : "";
}

async function createCategory(inputId, selectId, boxId) {
    const input = document.getElementById(inputId);
    const select = document.getElementById(selectId);
    const box = document.getElementById(boxId);

    if (!input || !select || !box) {
        return;
    }

    const name = input.value.trim();

    if (!name) {
        input.focus();
        return;
    }

    try {
        const response = await fetch(
            "{% url 'study:add_category' %}",
            {
                method: "POST",
                headers: {
                    "Content-Type":
                        "application/x-www-form-urlencoded",
                    "X-CSRFToken": getCSRFToken(),
                    "X-Requested-With": "XMLHttpRequest"
                },
                body: new URLSearchParams({
                    name: name
                })
            }
        );

        const data = await response.json();

        if (!response.ok || !data.success) {
            throw new Error(
                data.error || "Unable to create note type."
            );
        }

        let option = Array.from(
            select.options
        ).find(
            item => item.value == data.id
        );

        if (!option) {
            option = document.createElement("option");
            option.value = data.id;
            option.textContent = data.name;
            select.appendChild(option);
        }

        option.selected = true;

        const filter = document.getElementById(
            "categoryFilterNotes"
        );

        if (filter) {
            const exists = Array.from(
                filter.options
            ).some(
                item =>
                    item.value ===
                    data.name.toLowerCase()
            );

            if (!exists) {
                const filterOption =
                    document.createElement("option");

                filterOption.value =
                    data.name.toLowerCase();

                filterOption.textContent =
                    data.name;

                filter.appendChild(filterOption);
            }
        }

        input.value = "";
        box.style.display = "none";

    } catch (error) {
        alert(
            error.message ||
            "Something went wrong."
        );
    }
}

async function createCourse(inputId, selectId, boxId) {
    const input = document.getElementById(inputId);
    const select = document.getElementById(selectId);
    const box = document.getElementById(boxId);

    if (!input || !select || !box) {
        return;
    }

    const name = input.value.trim();

    if (!name) {
        input.focus();
        return;
    }

    try {
        const response = await fetch(
            "{% url 'study:add_course' %}",
            {
                method: "POST",
                headers: {
                    "Content-Type":
                        "application/x-www-form-urlencoded",
                    "X-CSRFToken": getCSRFToken(),
                    "X-Requested-With": "XMLHttpRequest"
                },
                body: new URLSearchParams({
                    name: name
                })
            }
        );

        const data = await response.json();

        if (!response.ok || !data.success) {
            throw new Error(
                data.error || "Unable to create course."
            );
        }

        let option = Array.from(
            select.options
        ).find(
            item => item.value == data.id
        );

        if (!option) {
            option = document.createElement("option");
            option.value = data.id;
            option.textContent = data.name;
            select.appendChild(option);
        }

        option.selected = true;

        input.value = "";
        box.style.display = "none";

    } catch (error) {
        alert(
            error.message ||
            "Something went wrong."
        );
    }
}

document.addEventListener(
    "keydown",
    function (event) {
        if (event.key === "Escape") {
            document
                .querySelectorAll(".modal-overlay")
                .forEach(function (modal) {
                    modal.style.display = "none";
                });

            document.body.style.overflow = "";
        }
    }
);