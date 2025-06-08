const BASE_URL = "http://127.0.0.1:8000"; // Change to your backend URL after deployment

async function search() {
  const q = document.getElementById('query').value.trim();
  if (!q) {
    alert("Please enter a search query.");
    return;
  }
  const res = await fetch(`${BASE_URL}/search?q=${encodeURIComponent(q)}`);
  if (!res.ok) {
    alert("Search failed. Please try again.");
    return;
  }
  const data = await res.json();
  const resultsDiv = document.getElementById('results');
  if (data.results.length === 0) {
    resultsDiv.innerHTML = "<p>No results found.</p>";
    return;
  }
  resultsDiv.innerHTML = data.results.map(r => `
    <article tabindex="0">
      <h2>${r.title}</h2>
      <p>${r.content}</p>
    </article>
  `).join('');
}

async function summarize() {
  const res = await fetch(`${BASE_URL}/summarize`);
  if (!res.ok) {
    alert("Failed to fetch summaries. Please try again.");
    return;
  }
  const data = await res.json();
  const resultsDiv = document.getElementById('results');
  if (!data.enriched || data.enriched.length === 0) {
    resultsDiv.innerHTML = "<p>No summaries available.</p>";
    return;
  }
  resultsDiv.innerHTML = data.enriched.map(r => `
    <article tabindex="0">
      <h2>${r.title}</h2>
      <p><strong>Summary & Tags:</strong><br>${r.summary_and_tags.replaceAll('\n', '<br>')}</p>
    </article>
  `).join('');
}
