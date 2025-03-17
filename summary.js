document.addEventListener("DOMContentLoaded", () => {
    chrome.storage.local.get(["translated"], (result) => {
        document.getElementById("summaryText").textContent = result.translated || "No summary found.";
    });

    document.getElementById("backBtn").addEventListener("click", () => {
        chrome.storage.local.remove("translated", () => {  // Clears only the summary, keeps videoID
            console.log("Summary cleared!");
            window.location.href = "popup.html";
        });
    });
});
