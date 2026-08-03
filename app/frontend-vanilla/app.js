const statusElement = document.querySelector("#api-status");
const checkButton = document.querySelector("#check-api");
const apiLink = document.querySelector("#api-url");
const previewStatusElement = document.querySelector("#preview-status");
const previewButton = document.querySelector("#check-preview");
const previewLink = document.querySelector("#preview-url");
const healthApiUrl = "http://127.0.0.1:5000/api/health";
const livePreviewUrl = "http://127.0.0.1:3000/b3-web1/index.html?vscode-livepreview=true";
let checkCount = 0;
let previewCheckCount = 0;

apiLink.href = healthApiUrl;
apiLink.textContent = healthApiUrl;
previewLink.href = livePreviewUrl;

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
    statusElement.textContent = `Check #${checkCount}: Flask server reachable — ${data.status}, ${data.service} ${data.version} at ${checkedAt}`;
  } catch (error) {
    statusElement.textContent = `Check #${checkCount}: Flask server or API unavailable — ${error.message}`;
  } finally {
    checkButton.disabled = false;
    checkButton.textContent = "Check Flask Server Again";
  }
}

async function checkLivePreview() {
  previewCheckCount += 1;
  previewStatusElement.textContent = "Checking Live Preview server...";
  previewButton.disabled = true;
  previewButton.textContent = "Checking...";

  try {
    // port 8080과 3000은 서로 다른 origin이다. `no-cors` 응답은 status나 HTML을
    // 읽을 수 없지만, network 연결 자체가 실패하면 fetch가 reject되므로 개발
    // server의 기본 도달 가능 여부를 확인하는 데 사용할 수 있다.
    await fetch(livePreviewUrl, {
      mode: "no-cors",
      cache: "no-store",
    });

    const checkedAt = new Date().toLocaleTimeString();
    previewStatusElement.textContent = `Check #${previewCheckCount}: Live Preview server reachable at ${checkedAt} — open the page to verify its content`;
  } catch (error) {
    previewStatusElement.textContent = `Check #${previewCheckCount}: Live Preview server unavailable — ${error.message}`;
  } finally {
    previewButton.disabled = false;
    previewButton.textContent = "Check Live Preview Server Again";
  }
}

checkButton.addEventListener("click", checkApi);
previewButton.addEventListener("click", checkLivePreview);
checkApi();
checkLivePreview();
