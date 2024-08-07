// Initialize the map
var map = L.map('map').setView([20.5937, 78.9629], 5); // Center on India

L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map);

// Define bounds for India
var southWest = L.latLng(6.462, 68.175);
var northEast = L.latLng(37.6, 97.4);
var bounds = L.latLngBounds(southWest, northEast);

// Set the map bounds to restrict the view to India
map.setMaxBounds(bounds);
map.on('drag', function() {
    map.panInsideBounds(bounds);
});

var markers = [];
var boundingBoxLayer;
var coordinatesConfirmed = false;  // Flag to track if coordinates are confirmed

// Function to handle adding markers
function addMarker(e) {
    if (markers.length < 2) {
        var marker = L.marker(e.latlng).addTo(map);
        markers.push(marker);

        if (markers.length === 2) {
            var bounds = L.latLngBounds(markers[0].getLatLng(), markers[1].getLatLng());
            boundingBoxLayer = L.rectangle(bounds, {color: "#ff7800", weight: 1}).addTo(map);
        }
    }
}

map.on('click', addMarker);

document.getElementById('resetMarkers').addEventListener('click', function() {
    markers.forEach(marker => map.removeLayer(marker));
    if (boundingBoxLayer) {
        map.removeLayer(boundingBoxLayer);
    }
    markers = [];
    coordinatesConfirmed = false;  // Reset the confirmation flag
    document.getElementById('nextPage').disabled = true;  // Disable the Next Page button
});

document.getElementById('confirmMarkers').addEventListener('click', function() {
    if (markers.length === 2) {
        var bounds = L.latLngBounds(markers[0].getLatLng(), markers[1].getLatLng());

        var boundingBox = {
            north: bounds.getNorth(),
            south: bounds.getSouth(),
            east: bounds.getEast(),
            west: bounds.getWest()
        };

        localStorage.setItem('boundingBox', JSON.stringify(boundingBox));
        console.log("Bounding Box Coordinates Saved:", boundingBox);

        fetch('http://127.0.0.1:5000/bounding-box', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(boundingBox)
        })
        .then(response => response.json())
        .then(data => console.log(data))
        .catch(error => console.error('Error:', error));

        coordinatesConfirmed = true;  // Set the confirmation flag
        document.getElementById('nextPage').disabled = false;  // Enable the Next Page button
    } else {
        alert("Please select exactly 2 markers.");
    }
});

document.getElementById('nextPage').addEventListener('click', function() {
    if (coordinatesConfirmed) {
        // Navigate to the demographic section without reloading the page
        document.getElementById('mapTabContent').classList.remove('active');
        document.getElementById('demographicsTabContent').classList.add('active');
        document.getElementById('mapTab').classList.remove('active');
        document.getElementById('demographicsTab').classList.add('active');
    }
});

document.getElementById('mapTab').addEventListener('click', function() {
    document.getElementById('mapTabContent').classList.add('active');
    document.getElementById('demographicsTabContent').classList.remove('active');
    this.classList.add('active');
    document.getElementById('demographicsTab').classList.remove('active');
});

document.getElementById('demographicsTab').addEventListener('click', function() {
    document.getElementById('mapTabContent').classList.remove('active');
    document.getElementById('demographicsTabContent').classList.add('active');
    this.classList.add('active');
    document.getElementById('mapTab').classList.remove('active');
});

map.on('mousemove', function(e) {
    var latLng = e.latlng;
    document.getElementById('coordinates').innerText = 
        'Lat: ' + latL
