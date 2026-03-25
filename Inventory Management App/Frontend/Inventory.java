
const apiURL = "http://YOUR-EC2-PUBLIC-IP:5000";

const form = document.getElementById('form');
const itemsDiv = document.getElementById('items');
const alertDiv = document.getElementById('alertItems');

// Switch Views
function showDashboard() {
  document.getElementById('dashboard').classList.remove('hidden');
  document.getElementById('alerts').classList.add('hidden');
}

function showAlerts() {
  document.getElementById('dashboard').classList.add('hidden');
  document.getElementById('alerts').classList.remove('hidden');
  loadAlerts();
}

// Add Item
form.addEventListener('submit', async (e) => {
  e.preventDefault();

  const name = document.getElementById('name').value;
  const quantity = document.getElementById('quantity').value;
  const min = document.getElementById('min').value;
  const max = document.getElementById('max').value;

  await fetch(apiURL + '/add', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ name, quantity, min, max })
  });

  loadItems();
});

// Load All Items
async function loadItems() {
  const res = await fetch(apiURL + '/items');
  const data = await res.json();

  itemsDiv.innerHTML = '';

  data.forEach(item => {
    let color = "white";
    if (item.alert.includes("LOW")) color = "orange";
    if (item.alert.includes("OVER")) color = "red";
    if (item.alert.includes("OK")) color = "lightgreen";

    itemsDiv.innerHTML += `
      <div class="card" style="border-left: 6px solid ${color}">
        <h3>${item.name}</h3>
        <p>Quantity: ${item.quantity}</p>
        <p>Status: ${item.alert}</p>
      </div>
    `;
  });
}

// Load Only Alerts
async function loadAlerts() {
  const res = await fetch(apiURL + '/items');
  const data = await res.json();

  alertDiv.innerHTML = '';

  data.forEach(item => {
    if (item.alert.includes("LOW") || item.alert.includes("OVER")) {
      let color = item.alert.includes("LOW") ? "orange" : "red";

      alertDiv.innerHTML += `
        <div class="card" style="border-left: 6px solid ${color}">
          <h3>${item.name}</h3>
          <p>Quantity: ${item.quantity}</p>
          <p>Status: ${item.alert}</p>
        </div>
      `;
    }
  });
}

loadItems();
