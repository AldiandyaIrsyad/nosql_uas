function getColor(value, min, max) {
  if (value === null || value === undefined || min === undefined || max === undefined) {
    return '#808080';  // gray for no data
  }
  
  // Calculate percentage (0 to 1)
  const percentage = (value - min) / (max - min);
  
  // Red starts at 255 and decreases to 0
  // Green starts at 0 and increases to 255
  const red = Math.round(255 * (1 - percentage));
  const green = Math.round(255 * percentage);
  
  return `rgb(${red},${green},0)`;
}

function updateMapData(indicators) {
  console.log('Updating map with indicators:', indicators);
  
  // Clear existing layers
  if (window.indonesiaLayer) {
    map.removeLayer(window.indonesiaLayer);
  }
  if (legend && legend._map) {
    legend.remove();
  }

  // Calculate min and max for color scaling
  const values = indicators.map(i => i.value).filter(v => v != null);
  const min = Math.min(...values);
  const max = Math.max(...values);

  // Create GeoJSON with new data
  const geoJSON = convertToGeoJSON(Geometries);
  const mergedData = {
    ...geoJSON,
    features: geoJSON.features.map(feature => ({
      ...feature,
      properties: {
        ...feature.properties,
        value: indicators.find(i => i.province === feature.properties.name)?.value
      }
    }))
  };

  // Style function for the map
  function style(feature) {
    return {
      fillColor: getColor(feature.properties.value, min, max),
      weight: 1,
      opacity: 1,
      color: '#2a2a40',
      fillOpacity: 0.7
    };
  }

  // Create new layer with new data
  window.indonesiaLayer = L.geoJSON(mergedData, {
    style: style,
    onEachFeature: onEachFeature
  }).addTo(map);

  // Update legend
  const legend = L.control({ position: 'bottomright' });
  legend.onAdd = function(map) {
    const div = L.DomUtil.create('div', 'info legend');
    const grades = [
      min,
      min + (max - min) * 0.25,
      min + (max - min) * 0.5,
      min + (max - min) * 0.75,
      max
    ];

    div.innerHTML = '<h4>Value Range</h4>';
    for (let i = 0; i < grades.length; i++) {
      div.innerHTML += `
        <i style="background:${getColor(grades[i], min, max)}"></i>
        ${grades[i].toFixed(2)}${i === grades.length - 1 ? '+' : ''}<br>
      `;
    }
    return div;
  };
  legend.addTo(map);
}

async function onYearChange() {
  const title = titleSelect.value;
  const year = yearSelect.value;
  if (!title || !year) return;

  const response = await fetch(`/dashboard?title=${encodeURIComponent(title)}&year=${encodeURIComponent(year)}`, {
    headers: { 'X-Requested-With': 'XMLHttpRequest' }
  });
  const data = await response.json();
  console.log('Year change response:', data);
  
  // Store current indicators and update map
  window.currentIndicators = data.indicators;
  updateMapData(data.indicators);
}