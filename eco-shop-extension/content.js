console.log("✅ Eco Analyzer content script loaded!");

// Create sidebar container
const container = document.createElement("div");
container.id = "eco-analyzer";
Object.assign(container.style, {
  position: "fixed",
  top: "80px",
  right: "0",
  width: "350px",
  height: "80vh",
  background: "#e8f5e9",
  boxShadow: "0 0 10px rgba(0,0,0,0.3)",
  zIndex: "9999",
  padding: "15px",
  overflowY: "auto",
  fontFamily: "Arial, sans-serif",
  borderRadius: "8px 0 0 8px"
});

// Close button
const closeBtn = document.createElement("div");
closeBtn.textContent = "❌";
Object.assign(closeBtn.style, {
  cursor: "pointer",
  textAlign: "right",
  fontSize: "18px"
});
closeBtn.onclick = () => container.remove();
container.appendChild(closeBtn);

// Header
const header = document.createElement("h3");
header.textContent = "🌱 Eco Analyzer";
header.style.color = "#2e7d32";
header.style.marginTop = "0";
container.appendChild(header);

// Status paragraph
const status = document.createElement("p");
status.textContent = "Analyzing product…";
status.style.color = "#555";
container.appendChild(status);

// inject into page
document.body.appendChild(container);

// Extract product info
let productText = "";
if (location.hostname.includes("amazon")) {
  const titleEl = document.getElementById("productTitle");
  const descEl = document.getElementById("feature-bullets") || document.getElementById("productDescription");
  productText = (titleEl?.innerText || "") + "\n\n" + (descEl?.innerText || "");
} else if (location.hostname.includes("flipkart")) {
  const titleEl = document.querySelector("span.B_NuCI");
  const descEl = document.querySelector("div._1mXcCf");
  productText = (titleEl?.innerText || "") + "\n\n" + (descEl?.innerText || "");
}

// Send to backend
fetch("http://localhost:5000/analyze", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ productText })
})
.then(res => res.json())
.then(data => {
  if (data.error) {
    status.textContent = "⚠️ " + data.error;
    return;
  }
  status.remove();
  container.innerHTML += `<pre>${JSON.stringify(data, null, 2)}</pre>`;
})
.catch(err => {
  status.textContent = "❌ Failed to connect to backend.";
  console.error(err);
});