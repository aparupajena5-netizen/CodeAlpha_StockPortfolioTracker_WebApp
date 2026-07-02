// Stock Portfolio Tracker - frontend logic
// Talks to the Flask backend via fetch() calls to /api/* routes.

const symbolSelect = document.getElementById("symbol");
const quantityInput = document.getElementById("quantity");
const addForm = document.getElementById("addForm");
const formError = document.getElementById("formError");
const priceList = document.getElementById("priceList");
const holdingsBody = document.getElementById("holdingsBody");
const totalValueEl = document.getElementById("totalValue");
const exportBtn = document.getElementById("exportBtn");
const ticker = document.getElementById("ticker");

let stockPrices = {};

function formatMoney(n) {
  return "$" + Number(n).toLocaleString();
}

// Load the hardcoded stock price list and populate the dropdown, price list, and ticker
async function loadStocks() {
  const res = await fetch("/api/stocks");
  stockPrices = await res.json();

  symbolSelect.innerHTML = "";
  priceList.innerHTML = "";
  let tickerHtml = "";

  Object.entries(stockPrices).forEach(([symbol, price]) => {
    const option = document.createElement("option");
    option.value = symbol;
    option.textContent = `${symbol} — ${formatMoney(price)}`;
    symbolSelect.appendChild(option);

    const li = document.createElement("li");
    li.innerHTML = `<span>${symbol}</span><span>${formatMoney(price)}</span>`;
    priceList.appendChild(li);

    tickerHtml += `<span class="up">${symbol} ${formatMoney(price)}</span>`;
  });

  // Duplicate the ticker content so the scroll loops seamlessly
  ticker.innerHTML = tickerHtml + tickerHtml;
}

// Load the current portfolio from the database and render it
async function loadPortfolio() {
  const res = await fetch("/api/portfolio");
  const data = await res.json();
  renderPortfolio(data);
}

function renderPortfolio(data) {
  totalValueEl.textContent = formatMoney(data.total_value);

  if (data.holdings.length === 0) {
    holdingsBody.innerHTML = '<tr class="empty-row"><td colspan="5">No holdings yet — add your first stock.</td></tr>';
    return;
  }

  holdingsBody.innerHTML = "";
  data.holdings.forEach((h) => {
    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td>${h.symbol}</td>
      <td>${h.quantity}</td>
      <td>${formatMoney(h.price)}</td>
      <td>${formatMoney(h.value)}</td>
      <td><button class="remove-btn" data-id="${h.id}">Remove</button></td>
    `;
    holdingsBody.appendChild(tr);
  });

  // Wire up remove buttons
  document.querySelectorAll(".remove-btn").forEach((btn) => {
    btn.addEventListener("click", () => removeHolding(btn.dataset.id));
  });
}

async function removeHolding(id) {
  const res = await fetch(`/api/remove/${id}`, { method: "DELETE" });
  const data = await res.json();
  renderPortfolio(data);
}

addForm.addEventListener("submit", async (e) => {
  e.preventDefault();
  formError.textContent = "";

  const symbol = symbolSelect.value;
  const quantity = quantityInput.value;

  const res = await fetch("/api/add", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ symbol, quantity }),
  });

  const data = await res.json();

  if (!res.ok) {
    formError.textContent = data.error || "Something went wrong.";
    return;
  }

  quantityInput.value = "";
  renderPortfolio(data);
});

exportBtn.addEventListener("click", () => {
  window.location.href = "/api/export";
});

// Initial load
loadStocks().then(loadPortfolio);
