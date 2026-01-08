// Global audio helper
function speak(text) {
    window.speechSynthesis.cancel();  // Stop previous speech
    const msg = new SpeechSynthesisUtterance(text);
    msg.rate = 1;
    msg.pitch = 1;
    window.speechSynthesis.speak(msg);
}

// Speak multiple sentences in sequence
function speakSequence(arr) {
    if (!arr || arr.length === 0) return;
    let index = 0;
    function next() {
        if (index >= arr.length) return;
        const msg = new SpeechSynthesisUtterance(arr[index]);
        msg.onend = () => { index++; next(); };
        window.speechSynthesis.speak(msg);
    }
    next();
}

// Speak a live element (errors, messages)
function speakLive(id) {
    const el = document.getElementById(id);
    if (el && el.innerText.trim() !== "") {
        speak(el.innerText);
    }
}
