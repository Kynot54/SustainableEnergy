<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Neon Draggable Marker with Radius Circle</title>
    <!-- Include Leaflet CSS and JavaScript -->
    <link rel="stylesheet" href="https://unpkg.com/leaflet/dist/leaflet.css" />
    <script src="https://unpkg.com/leaflet/dist/leaflet.js"></script>
    <style>
        body {
            margin: 0;
            padding: 0;
            font-family: Arial, sans-serif;
            background-color: #000;
            color: #fff;
            overflow: hidden;
            position: relative; /* Ensure correct positioning of response box */
        }

        #map {
            height: 70vh;
            width: 100vw;
        }

        #coordinates {
            margin-top: 10px;
        }

        /* Neon Marker CSS */
        .neon-marker {
            border: 2px solid #fff;
            border-radius: 50%;
            width: 20px;
            height: 20px;
            background-color: pink; /* Change the background color to pink */
            box-shadow: 0 0 10px pink, 0 0 20px pink, 0 0 40px pink, 0 0 80px pink; /* Adjust box shadow color */
            animation: neon-pulse 1.5s infinite alternate;
        }

        @keyframes neon-pulse {
            from {
                opacity: 0.2;
            }
            to {
                opacity: 1;
            }
        }

        /* Button Styles */
        button {
            background-color: #f0f;
            border: none;
            color: #000;
            padding: 10px 20px;
            cursor: pointer;
            border-radius: 5px;
            font-size: 16px;
            margin-top: 10px;
        }

        button:hover {
            background-color: #0f0;
        }

        /* Input Styles */
        input[type="number"] {
            padding: 5px 10px;
            border-radius: 5px;
            border: 1px solid #fff;
            background-color: transparent;
            color: #fff;
        }

        label {
            display: flex;
            margin-top: 10px;
        }

        /* Top coordinates box styles */
#top-coordinates-box {
    position: absolute;
    bottom: 0px;
    right: 50px; /* Adjust right position for more space */
    max-width: 500px; /* Limit the maximum width */
    background-color: rgba(0, 0, 0, 0.8); /* Update background color */
    padding: 10px;
    border-radius: 5px;
    max-height: calc(100vh - 100px); /* Adjust max-height to fit within the viewport */
    overflow-y: auto;
    z-index: 1000; /* Ensure it's on top of other elements */
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.3); /* Add box shadow for depth */
}

#top-coordinates-box h3 {
    margin-top: 0;
    color: #fff; /* Update heading color */
}

#top-coordinates-list {
    list-style-type: none;
    padding: 0;
    margin: 0;
}

#top-coordinates-list li {
    margin-bottom: 5px;
    color: #fff; /* Update list item color */
}
    </style>
</head>
<body>
<div id = "container">


<div id="map"></div>
<div id="coordinates">Latitude: <span id="lat"></span>, Longitude: <span id="lng"></span></div>
<div>
    <label for="radius">Enter Radius (in miles):</label>
    <input type="number" id="radius" min="0" value="10" />
    <button onclick="drawCircle()">Draw Circle</button>
</div>
<div>
    <button onclick="sendDataToWolfram()">Submit</button>
</div>
    </div>

<!-- Top coordinates box -->
<div id="top-coordinates-box">
    <h3>Top 5 Coordinates</h3>
    <ul id="top-coordinates-list"></ul>
</div>

<script>
    window.pointCoordinates = [];

    // Initialize Leaflet map centered on United States
    var map = L.map('map').setView([39.8283, -98.5795], 4);

    // Add Dark-themed tile layer
    L.tileLayer('https://tile.thunderforest.com/transport-dark/{z}/{x}/{y}.png?apikey=515b56fecb2d45b8aeaad6ef3860a5b1', {
        attribution: '&copy; <a href="https://www.thunderforest.com/">Thunderforest</a> contributors'
    }).addTo(map);

    // Initialize variables to store latitude and longitude
    var latitude, longitude;
    var circle;

    // Add a draggable marker at the center of the United States with neon effect
    var marker = L.marker([39.8283, -98.5795], {
        draggable: true,
        icon: L.divIcon({
            className: 'neon-marker'
        })
    }).addTo(map);

    // Implement drag and drop functionality for the marker
    marker.on('dragend', function (event) {
        var marker = event.target;
        var position = marker.getLatLng();
        latitude = position.lat;
        longitude = position.lng;
        map.panTo(position); // Pan the map to the new marker position
        document.getElementById('lat').innerText = latitude.toFixed(6);
        document.getElementById('lng').innerText = longitude.toFixed(6);
    });

    // Function to draw circle based on entered radius
    function drawCircle() {
        var miles = parseFloat(document.getElementById('radius').value);
        var radiusInMeters = miles * 1609.34; // Convert miles to meters

        // Remove existing circle and points if present
        if (circle) {
            map.removeLayer(circle);
        }
        // Clear existing points if any
        if (window.points && window.points.length) {
            window.points.forEach(function (point) {
                map.removeLayer(point);
            });
        }
        window.points = [];

        // Add new circle
        circle = L.circle(marker.getLatLng(), {
            radius: radiusInMeters,
            opacity: 0.5,
            fillColor: 'pink', // Change the circle fill color to pink
            fillOpacity: 0.2
        }).addTo(map);

        // Calculate and add points within the circle
        var totalPoints = 7;
        var rings = Math.ceil(Math.sqrt(totalPoints)); // Estimate number of rings needed
        var angleStep = 360 / rings; // Angle step for distribution
        var radialIncrement = radiusInMeters / rings; // Radial increment for each ring

        for (var ring = 0; ring < rings; ring++) {
            var pointsInRing = ring === 0 ? 1 : Math.round(2 * Math.PI * ring); // Distribute more points in outer rings
            for (var i = 0; i < pointsInRing; i++) {
                var angle = i * (360 / pointsInRing); // Angle for the current point
                var angleRad = angle * (Math.PI / 180); // Convert angle to radians

                // Adjust radius for each ring to distribute points inside the circle
                var adjustedRadius = radialIncrement * ring;

                // Calculate point position
                var pointLat = marker.getLatLng().lat + (adjustedRadius / 111111) * Math.cos(angleRad);
                var pointLng =
                    marker.getLatLng().lng +
                    ((adjustedRadius / 111111) * Math.sin(angleRad)) /
                    Math.cos((marker.getLatLng().lat * Math.PI) / 180);

                // Add point to the map with neon effect
                window.pointCoordinates.push({ lat: pointLat, lng: pointLng });
            }
        }
    }

    var yellowMarkers = L.layerGroup().addTo(map); // Create a layer group for yellow markers

    function sendDataToWolfram() {
        var coordinates = window.pointCoordinates; // Get the stored coordinates

        console.log('Point Coordinates:', coordinates);

        // Specify the URL of your Flask backend endpoint
        var flaskEndpoint = 'http://localhost:5000/submit-coordinates'; // Change this to your actual Flask endpoint URL

        // Make the POST request to your Flask backend
        fetch(flaskEndpoint, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ coordinates: coordinates })
        })
            .then((response) => response.json()) // Assuming your Flask endpoint responds with JSON
            .then((data) => {
                console.log('Success:', data); // Handle success response
                drawTopLocations(data.top_5_results); // Call function to draw top locations
                // Update the response box with the generated text
               // document.getElementById('response-box').innerText = data.generated_text;
            })
            .catch((error) => {
                console.error('Error:', error); // Handle errors
            });
    }



// Function to draw the top locations on the map
function drawTopLocations(topLocations) {
    var topCoordinatesList = document.getElementById('top-coordinates-list');
    topCoordinatesList.innerHTML = ''; // Clear previous list items

    // Loop through all top locations, consider all 10 for processing
    for (var i = 0; i < Math.min(topLocations.length, 5); i++) {
        var location = topLocations[i];
        var index = location.index;
        var lat = window.pointCoordinates[index].lat;
        var lng = window.pointCoordinates[index].lng;

        // Add yellow marker for each top location to the yellowMarkers layer group
        var marker = L.marker([lat, lng], { icon: yellowIcon }).addTo(yellowMarkers);

        // Display only the top 5 coordinates in the list
        if (i < 5) {
            // Add coordinates to the top coordinates box
            var listItem = document.createElement('li');
            listItem.textContent = `${i + 1}. Latitude: ${lat.toFixed(6)}, Longitude: ${lng.toFixed(6)}`;
            topCoordinatesList.appendChild(listItem);

            // For even indices, add a line break to display two coordinates per line
            if ((i + 1) % 2 === 0) {
                topCoordinatesList.appendChild(document.createElement('br'));
            }
        }
    }
}


    // Define a custom icon for the yellow marker
    var yellowIcon = L.icon({
        iconUrl: 'https://preview.redd.it/my-guinner-solar-pnel-v0-kureb0ch0skc1.png?auto=webp&s=0559fcbd587232674691053948c7d4979d40ae91',
        iconSize: [80, 90],
        iconAnchor: [12, 41],
        popupAnchor: [1, -34],
    });
</script>
</body>
</html>
