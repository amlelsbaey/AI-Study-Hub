document.addEventListener("DOMContentLoaded", function () {

    const searchInput =
        document.getElementById("liveSearchResources");

    const typeFilter =
        document.getElementById("typeFilterResources");

    const resourceItems =
        document.querySelectorAll(".resource-item");


    function filterResources() {

        const query =
            searchInput.value.toLowerCase().trim();

        const selectedType =
            typeFilter.value.toLowerCase().trim();


        resourceItems.forEach(function (item) {

            const text =
                item.textContent.toLowerCase();

            const itemType =
                item.getAttribute("data-type");


            const matchesSearch =
                text.includes(query);

            const matchesType =
                !selectedType ||
                itemType === selectedType;


            item.style.display =
                matchesSearch && matchesType
                    ? "flex"
                    : "none";

        });

    }


    if (searchInput) {
        searchInput.addEventListener(
            "input",
            filterResources
        );
    }


    if (typeFilter) {
        typeFilter.addEventListener(
            "change",
            filterResources
        );
    }

});


function openModal(id) {

    const modal =
        document.getElementById(id);

    if (!modal) {
        return;
    }

    modal.style.display = "flex";

    document.body.style.overflow = "hidden";
}


function closeModal(id) {

    const modal =
        document.getElementById(id);

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

    const box =
        document.getElementById(id);

    if (!box) {
        return;
    }


    box.style.display =
        box.style.display === "block"
            ? "none"
            : "block";

}


function getCSRFToken() {

    const tokenInput =
        document.querySelector(
            "[name=csrfmiddlewaretoken]"
        );

    return tokenInput
        ? tokenInput.value
        : "";
}


async function createResourceType() {

    const input =
        document.getElementById(
            "resourceTypeInput"
        );

    const select =
        document.getElementById(
            "resourceTypeSelect"
        );

    const box =
        document.getElementById(
            "addResourceTypeBox"
        );


    if (!input || !select || !box) {
        return;
    }


    const name =
        input.value.trim();


    if (!name) {
        input.focus();
        return;
    }


    try {

        const response =
            await fetch(
                window.addResourceTypeUrl,
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/x-www-form-urlencoded",

                        "X-CSRFToken":
                            getCSRFToken(),

                        "X-Requested-With":
                            "XMLHttpRequest"
                    },

                    body:
                        new URLSearchParams({
                            name: name
                        })
                }
            );


        const responseText =
            await response.text();


        let data;


        try {

            data =
                JSON.parse(responseText);

        } catch (jsonError) {

            console.error(
                "Server returned non-JSON response:",
                responseText
            );

            throw new Error(
                "The server returned an invalid response. Please make sure you are logged in."
            );
        }


        if (!response.ok || !data.success) {

            throw new Error(
                data.error ||
                "Unable to create resource type."
            );

        }


        let option =
            Array.from(
                select.options
            ).find(
                option =>
                    option.value == data.id
            );


        if (!option) {

            option =
                document.createElement(
                    "option"
                );

            option.value =
                data.id;

            option.textContent =
                data.name;

            select.appendChild(
                option
            );

        }


        option.selected = true;


        const filter =
            document.getElementById(
                "typeFilterResources"
            );


        if (filter) {

            const exists =
                Array.from(
                    filter.options
                ).some(
                    option =>
                        option.value ===
                        data.name.toLowerCase()
                );


            if (!exists) {

                const filterOption =
                    document.createElement(
                        "option"
                    );

                filterOption.value =
                    data.name.toLowerCase();

                filterOption.textContent =
                    data.name;

                filter.appendChild(
                    filterOption
                );

            }

        }


        input.value = "";

        box.style.display = "none";


    } catch (error) {

        console.error(error);

        alert(
            error.message ||
            "Something went wrong while creating the resource type."
        );

    }

}


document.addEventListener(
    "keydown",
    function (event) {

        if (event.key === "Escape") {

            document
                .querySelectorAll(
                    ".modal-overlay"
                )
                .forEach(
                    function (modal) {

                        modal.style.display =
                            "none";

                    }
                );

            document.body.style.overflow = "";

        }

    }
);