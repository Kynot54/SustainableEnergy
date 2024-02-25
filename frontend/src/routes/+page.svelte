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

		<script>
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
				var radius = miles * 1609.34; // Convert miles to meters

				// Remove existing circle if present
				if (circle) {
					map.removeLayer(circle);
				}

				// Add new circle
				circle = L.circle(marker.getLatLng(), {
					radius: radius,
					opacity: 0.5,
					fillColor: 'blue',
					fillOpacity: 0.2
				}).addTo(map);
			}
		</script>
	</body>
</html>