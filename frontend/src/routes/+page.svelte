<!DOCTYPE html>
<html lang="en">
<head>
	<meta charset="UTF-8" />
	<meta name="viewport" content="width=device-width, initial-scale=1.0" />
	<title>Draggable Marker with Radius Circle</title>
	<!-- Include Leaflet CSS and JavaScript -->
	<link rel="stylesheet" href="https://unpkg.com/leaflet/dist/leaflet.css" />
	<script src="https://unpkg.com/leaflet/dist/leaflet.js"></script>
	<style>
		#map {
			height: 400px;
		}
		#coordinates {
			margin-top: 10px;
			font-family: Arial, sans-serif;
		}
	</style>
</head>
<body>
<div id="map"></div>
<div id="coordinates">Latitude: <span id="lat"></span>, Longitude: <span id="lng"></span></div>
<div>
	<label for="radius">Enter Radius (in miles):</label>
	<input type="number" id="radius" min="0" value="10" />
	<button onclick="drawCircle()">Draw Circle</button>
</div>
<div>
	<button onclick="sendDataToWolfram()">Submit to Wolfram</button>
</div>

<script>
	window.pointCoordinates = [];

	// Initialize Leaflet map centered on United States
	var map = L.map('map').setView([39.8283, -98.5795], 4);

	// Add OpenStreetMap tile layer
	L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
		attribution:
				'&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
	}).addTo(map);

	// Initialize variables to store latitude and longitude
	var latitude, longitude;
	var circle;

	// Add a draggable marker at the center of the United States
	var marker = L.marker([39.8283, -98.5795], {
		draggable: true
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
			fillColor: 'blue',
			fillOpacity: 0.2
		}).addTo(map);

		// Calculate and add points within the circle
		var totalPoints = 5;
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

				// Add point to the map
				var point = L.marker([pointLat, pointLng]).addTo(map);
				window.pointCoordinates.push({ lat: pointLat, lng: pointLng });
			}
		}
	}
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
				})
				.catch((error) => {
					console.error('Error:', error); // Handle errors
				});
	}
</script>
</body>
</html>