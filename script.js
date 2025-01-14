document.getElementById("send").addEventListener("click", async () => {
    const prompt = document.getElementById("prompt").value;
    const messages = document.getElementById("messages");

    if (!prompt.trim()) return;

    // הוספת הודעה של המשתמש למסך
    messages.innerHTML += `<div class="user-message"><strong>You:</strong> ${prompt}</div>`;
    document.getElementById("prompt").value = "";

    try {
        const response = await fetch("http://127.0.0.1:8000/generate", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ prompt })
        });
        const data = await response.json();

        // הוספת תגובת הבוט למסך
        messages.innerHTML += `<div class="bot-message"><strong>Bot:</strong> ${data.generated_text}</div>`;
    } catch (error) {
        messages.innerHTML += `<div class="error-message"><strong>Error:</strong> ${error.message}</div>`;
    }

    // גלילה אוטומטית לתחתית הצ'אט
    messages.scrollTop = messages.scrollHeight;
});
