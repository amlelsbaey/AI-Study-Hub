document.addEventListener("DOMContentLoaded", function () {

    const searchInput = document.getElementById("liveSearchTasks");
    const taskItems = document.querySelectorAll(
        "#tasksList .task-item"
    );



    if (searchInput) {

        searchInput.addEventListener("input", function () {

            const query = this.value
                .toLowerCase()
                .trim();


            taskItems.forEach(function (item) {

                const text = item.textContent
                    .toLowerCase();


                if (text.includes(query)) {

                    item.style.display = "flex";

                } else {

                    item.style.display = "none";

                }

            });

        });

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

    const tokenInput = document.querySelector(
        "[name=csrfmiddlewaretoken]"
    );


    if (!tokenInput) {
        return "";
    }


    return tokenInput.value;

}


async function createCourse() {

    const input = document.getElementById(
        "courseNameInput"
    );

    const select = document.getElementById(
        "taskCourseSelect"
    );

    const box = document.getElementById(
        "addCourseBox"
    );


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
            "/study/courses/add/",
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

                body: new URLSearchParams({
                    name: name
                })
            }
        );


        const contentType =
            response.headers.get("content-type") || "";


        if (!contentType.includes("application/json")) {

            const text = await response.text();

            console.error(
                "Expected JSON but received:",
                text
            );

            throw new Error(
                "Server returned an unexpected response."
            );

        }


        const data = await response.json();


        if (!response.ok || !data.success) {

            throw new Error(
                data.error ||
                "Unable to create course."
            );

        }


        let option = Array
            .from(select.options)
            .find(
                item => item.value == data.id
            );



        if (!option) {

            option =
                document.createElement("option");

            option.value = data.id;

            option.textContent = data.name;

            select.appendChild(option);

        }

        option.selected = true;


        input.value = "";


        box.style.display = "none";


    } catch (error) {

        console.error(
            "Create course error:",
            error
        );


        alert(
            error.message ||
            "Something went wrong while creating the course."
        );

    }

}


document.addEventListener(
    "keydown",
    function (event) {

        if (event.key !== "Escape") {
            return;
        }


        document
            .querySelectorAll(".modal-overlay")
            .forEach(function (modal) {

                modal.style.display = "none";

            });


        document.body.style.overflow = "";

    }
);