document.addEventListener("DOMContentLoaded", () => {
    loadWeather();
    loadClothing();
    // Load saved theme
    const savedTheme = localStorage.getItem("theme");
    if (savedTheme) {
        document.getElementById("theme").value = savedTheme;
        document.body.classList.toggle("dark", savedTheme === "dark");
    }
});

function loadWeather() {
    const location = localStorage.getItem("location") || "Delhi";
    fetch(`https://api.openweathermap.org/data/2.5/weather?q=${location}&appid=dadacf579e1607f1ab46d718b7b268b5&units=metric`)
        .then(response => response.json())
        .then(data => {
            document.getElementById("weather-icon").src = `https://openweathermap.org/img/wn/${data.weather[0].icon}.png`;
            document.getElementById("weather-details").innerText = `${data.weather[0].description}, ${data.main.temp}°C`;
            suggestOutfit(data);
        })
        .catch(error => console.error("Failed to Fetch Weather Data:", error));
}

function loadClothing() {
    const category = document.getElementById("category-filter")?.value || "";
    const occasion = document.getElementById("occasion-filter")?.value || "";
    fetch(`http://127.0.0.1:5000/get-clothing?category=${category}&occasion=${occasion}`)
        .then(response => response.json())
        .then(data => {
            const container = document.getElementById("clothing-list");
            container.innerHTML = "";
            data.forEach(item => {
                const div = document.createElement("div");
                div.classList.add("outfit");
                div.innerHTML = `
                    <img src="${item.image_path ? `/static/${item.image_path}` : `images/${item.category}.png`}" alt="${item.name}">
                    <p><strong>${item.name}</strong> (${item.color})</p>
                    <p>${item.category} - ${item.occasion}</p>
                    <p>Last Worn: ${item.last_worn || "Never"}</p>
                    <button onclick="markWorn(${item.id})">Mark Worn</button>
                    <button onclick="deleteItem(${item.id})">Delete</button>
                `;
                container.appendChild(div);
            });
        })
        .catch(error => console.error("Failed to Fetch Clothing Data:", error));
}

function suggestOutfit(weatherData) {
    const temp = weatherData.main.temp;
    fetch(`http://127.0.0.1:5000/suggest-outfit?temp=${temp}&occasion=Casual`)
        .then(response => response.json())
        .then(outfit => {
            const container = document.getElementById("outfit-container");
            container.innerHTML = `
                <div class="outfit">
                    <img src="${outfit.top.image_path ? `/static/${outfit.top.image_path}` : `images/${outfit.top.category}.png`}" alt="${outfit.top.name}">
                    <p>${outfit.top.name} (${outfit.top.color})</p>
                </div>
                <div class="outfit">
                    <img src="${outfit.bottom.image_path ? `/static/${outfit.bottom.image_path}` : `images/${outfit.bottom.category}.png`}" alt="${outfit.bottom.name}">
                    <p>${outfit.bottom.name} (${outfit.bottom.color})</p>
                </div>`;
        });
}

function markWorn(id) {
    const today = new Date().toISOString().split("T")[0]; // YYYY-MM-DD
    fetch(`http://127.0.0.1:5000/mark-worn/${id}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ date: today })
    }).then(() => loadClothing());
}

function deleteItem(id) {
    fetch(`http://127.0.0.1:5000/delete-clothing/${id}`, { method: "DELETE" })
        .then(() => loadClothing());
}

// Form submission for adding clothing
document.getElementById("add-clothing-form")?.addEventListener("submit", (e) => {
    e.preventDefault();
    const formData = new FormData();
    formData.append("name", document.getElementById("name").value);
    formData.append("category", document.getElementById("category").value);
    formData.append("color", document.getElementById("color").value);
    formData.append("occasion", document.getElementById("occasion").value);
    formData.append("image", document.getElementById("image").files[0]);
    fetch("http://127.0.0.1:5000/add-clothing", {
        method: "POST",
        body: formData
    }).then(() => loadClothing());
});

// Filter form
document.getElementById("filter-form")?.addEventListener("submit", (e) => {
    e.preventDefault();
    loadClothing();
});

// Theme toggle
document.getElementById("theme")?.addEventListener("change", (e) => {
    document.body.classList.toggle("dark", e.target.value === "dark");
    localStorage.setItem("theme", e.target.value);
});

// Location change
document.getElementById("location")?.addEventListener("change", (e) => {
    localStorage.setItem("location", e.target.value);
    loadWeather();
});