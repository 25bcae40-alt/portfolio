const typingText = document.getElementById("typingText");
const words = ["Data Analysis", "Web Development", "Machine Learning", "Financial Technology"];
let i = 0;
let char = 0;
let deleting = false;

function typeLoop() {
    if (!typingText) return;
    const word = words[i];
    typingText.textContent = word.slice(0, char);

    if (!deleting && char < word.length) {
        char++;
    } else if (deleting && char > 0) {
        char--;
    } else if (!deleting && char === word.length) {
        deleting = true;
    } else {
        deleting = false;
        i = (i + 1) % words.length;
    }

    const delay = deleting ? 45 : 85;
    setTimeout(typeLoop, char === word.length ? 1300 : delay);
}
typeLoop();

const form = document.getElementById("contactForm");
const statusText = document.getElementById("formStatus");

form?.addEventListener("submit", async (event) => {
    event.preventDefault();
    statusText.textContent = "Sending...";

    const payload = {
        name: form.name.value.trim(),
        email: form.email.value.trim(),
        message: form.message.value.trim(),
    };

    try {
        const res = await fetch("/api/messages", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload),
        });

        const data = await res.json();
        if (!res.ok) throw new Error(data.error || "Failed to send message");

        statusText.textContent = "Message sent successfully.";
        form.reset();
    } catch (error) {
        statusText.textContent = error.message;
    }
});
