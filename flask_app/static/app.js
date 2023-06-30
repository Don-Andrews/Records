const searchInput = document.querySelector(".search-input")
const dropdownMenu = document.querySelector(".dropdown-menu")

searchInput.addEventListener("keyup", handleSearchInput)

async function handleSearchInput(event) {
    const searchString = event.target.value;
    if(searchString !== "") {
        dropdownMenu.classList.add("show")
        const users = await makeApiCall(searchString)
        renderUsers(users)
    } else {
        dropdownMenu.classList.remove("show")
    }
}

function renderUsers(usersList){
    const markup = []
    if(usersList.length === 0){
        markup.push(`<a href="javascript:void(0)" class="dropdown-item rounded-pill spotify-words">No users found!</a>`)
    } else {
        for(let i=0; i < usersList.length; i++){
            const user = usersList[i];
            markup.push(`<a href="/${user.id}/reccPage" class="dropdown-item rounded-pill spotify-words">${user.user_name}</a>`)
        }
    }
    dropdownMenu.innerHTML = markup.join("")
}

async function makeApiCall(searchString){
    const formData = new FormData()
    formData.append("user_name", searchString)
    const response = await fetch("http://127.0.0.1:5000/search_user", {
        method: "POST",
        body: formData
    })
    const data = response.json()
    return data
}