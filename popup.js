document.getElementById("SummarizeBtn").addEventListener("click", () => {
    const selectedLanguage = document.getElementById("language-select").value;

    // Retrieving videoID from local storage.
    chrome.storage.local.get(["videoID"], (result) => {
        if (result.videoID) {
            console.log("videoID: ", result.videoID, "language: ", selectedLanguage);

            // Sending videoID and user-selected language to background.js.
            chrome.runtime.sendMessage({
                action: "request_sent",
                videoID: result.videoID, // ✅ Corrected
                language: selectedLanguage
            }, (response) => {
                if (chrome.runtime.lastError) {
                    console.error("Error: ", chrome.runtime.lastError);
                } else {
                    console.log("Response: ", response);
                    
                    // Redirect to summary page AFTER receiving a response.
                    window.location.href = "summary.html";
                }
            });
        } else {
            console.warn("No video ID found in storage.");
        }
    });
});




