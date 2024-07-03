function get_todos_request() {
    return fetch("http://127.0.0.1:8000/api/v1/todos", {
        method: "GET",
        headers: {
            'Content-Type': 'application/json', // Set the appropriate content type if sending JSON data
        }
    }).then(resp => resp.json())
    .then(data => data);
}

async function get_todos() {
    const todos = await get_todos_request();
    todos["data"].forEach(todo => {
        const markup = `<li>${todo.title}</li>`

        document.querySelector("ul").insertAdjacentHTML("beforeend", markup)
    });
}