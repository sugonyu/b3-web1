const statusElement = document.querySelector("#api-status");
const checkButton = document.querySelector("#check-api");
const apiLink = document.querySelector("#api-url");
const healthApiUrl = "http://127.0.0.1:5000/api/health";
let checkCount = 0;

apiLink.href = healthApiUrl;
apiLink.textContent = healthApiUrl;

async function checkApi() {
  checkCount += 1;
  statusElement.textContent = "Checking...";
  checkButton.disabled = true;
  checkButton.textContent = "Checking...";

  try {
    const response = await fetch(healthApiUrl);

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }

    const data = await response.json();
    const checkedAt = new Date().toLocaleTimeString();
    statusElement.textContent = `Check #${checkCount}: ${data.status} — ${data.service} ${data.version} at ${checkedAt}`;
  } catch (error) {
    statusElement.textContent = `Check #${checkCount}: API error — ${error.message}`;
  } finally {
    checkButton.disabled = false;
    checkButton.textContent = "Check Again";
  }
}

checkButton.addEventListener("click", checkApi);
checkApi();
