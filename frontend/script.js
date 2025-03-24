const API_URL = "http://127.0.0.1:5000";

// 🛒 Load wardrobe items from backend
function loadClothing() {
    fetch(`${API_URL}/get-clothing`)
        .then(response => response.json())
        .then(data => {
            let list = document.getElementById("clothing-list");
            list.innerHTML = ""; // Clear previous list
            
            data.forEach(item => {
                let li = document.createElement("li");
                li.textContent = `${item.name} - ${item.category} (${item.color})`;
                li.style.animation = "slideIn 0.5s ease-out";
                list.appendChild(li);
            });
        });
}

// ➕ Add a new clothing item with animation
function addClothing() {
    let name = document.getElementById("name").value;
    let category = document.getElementById("category").value;
    let color = document.getElementById("color").value;

    if (!name || !category || !color) {
        alert("Please fill all fields!");
        return;
    }

    fetch(`${API_URL}/add-clothing`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name, category, color })
    })
    .then(response => response.json())
    .then(() => {
        alert("Item added!");
        let list = document.getElementById("clothing-list");
        let newItem = document.createElement("li");
        newItem.textContent = `${name} - ${category} (${color})`;
        newItem.style.animation = "slideIn 0.5s ease-out";
        list.appendChild(newItem);
    });

    // Clear input fields
    document.getElementById("name").value = "";
    document.getElementById("category").value = "";
    document.getElementById("color").value = "";
}

// 🔎 Search functionality for wardrobe items
function searchClothing() {
    let searchInput = document.getElementById("search").value.toLowerCase();
    let items = document.querySelectorAll("#clothing-list li");

    items.forEach(item => {
        if (item.textContent.toLowerCase().includes(searchInput)) {
            item.style.display = "flex";
        } else {
            item.style.display = "none";
        }
    });
}

// 🌤 Fetch weather and suggest outfits
function getWeather() {
    const API_KEY = "YOUR_OPENWEATHERMAP_API_KEY"; // Replace with your API key
    const city = "Delhi"; // Change based on user location

    fetch(`https://api.openweathermap.org/data/2.5/weather?q=${city}&appid=${API_KEY}&units=metric`)
        .then(response => response.json())
        .then(data => {
            let temp = data.main.temp;
            let weather = data.weather[0].main;
            let weatherInfo = document.getElementById("weather-info");

            let outfit = "";
            if (temp > 25) {
                outfit = "Wear light and breathable clothes like T-shirts and shorts.";
            } else if (temp > 15) {
                outfit = "A comfortable outfit with a light jacket should be fine.";
            } else {
                outfit = "Wear warm clothes like sweaters and jackets.";
            }

            weatherInfo.innerHTML = `🌡 ${temp}°C - ${weather} <br> 👕 ${outfit}`;
        });
}

// 🚀 Load everything on start
window.onload = function() {
    loadClothing();
    getWeather();
};
