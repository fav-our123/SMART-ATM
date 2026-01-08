let audioEnabled = false;

// Enable audio on first user action
function enableAudio() {
    if (!audioEnabled) {
        audioEnabled = true;
        speak("Audio guidance enabled. Please follow the instructions.");
        document.removeEventListener("keydown", enableAudio);
        document.removeEventListener("click", enableAudio);
    }
}

// Text-to-Speech helper
function speak(text) {
    if (!audioEnabled) return;
    window.speechSynthesis.cancel(); // Stop any ongoing speech
    const msg = new SpeechSynthesisUtterance(text);
    msg.rate = 1;
    msg.pitch = 1;
    window.speechSynthesis.speak(msg);
}

// Speak an element’s inner text
function speakLive(id) {
    const el = document.getElementById(id);
    if (el) speak(el.innerText);
}

// Initialize camera (simulated)
function initCamera() {
    const video = document.getElementById("biometric-video");
    if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
        navigator.mediaDevices.getUserMedia({ video: true })
            .then((stream) => { video.srcObject = stream; })
            .catch(() => { speak("Camera access denied. Biometric verification failed."); });
    } else {
        speak("Camera not supported on this device.");
    }
}

// Simulate biometric verification and submit form
function verifyBiometric() {
    speak("Sit still. Verifying your identity, please wait.");
    setTimeout(() => {
        speak("Biometric verification successful. You may continue.");
        // Submit the hidden form to /card with biometric_passed=true
        document.getElementById("biometric-form").submit();
    }, 4000); // simulate 4 seconds verification
}

// Event listeners
document.addEventListener("keydown", enableAudio);
document.addEventListener("click", enableAudio);

// On page load
window.onload = function() {
    speak("Welcome to Smartsight Bank. Please look at the camera for biometric verification.");
    initCamera();
};
