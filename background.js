chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === "request_sent") {
        let { videoID, language } = request;
        let apiUrl = `http://localhost:5000/translate?videoID=${videoID}&lang=${language}`;

        fetch(apiUrl)
            .then(response => response.json())
            .then(data => {
                chrome.storage.local.set({ translated: data.translated }, () => {
                    console.log("Translated text stored successfully!");
                    sendResponse({ success: true, translated: data.translated });
                });
            })
            .catch(error => {
                console.error("Fetch error:", error);
                sendResponse({ success: false, error: error.message });
            });

        return true; // Keeps the response channel open for async processing
    }
});

