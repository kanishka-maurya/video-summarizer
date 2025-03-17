function getYouTubeVideoID() {
    const URL = window.location.href;
    const regex = /(?:youtube\.com\/(?:.*[?&]v=|embed\/|v\/)|youtu\.be\/)([a-zA-Z0-9_-]{11})/;
    const match = URL.match(regex);

    return match ? match[1] : null; 
}

const videoID = getYouTubeVideoID();


chrome.storage.local.set({ videoID: videoID }, () => {
    console.log("videoID stored successfully:", videoID);
});


