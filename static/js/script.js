document.addEventListener("DOMContentLoaded", () => {
  const bootScreen = document.getElementById("boot-screen");
  const terminalContainer = document.getElementById("terminal-container");
  const form = document.getElementById("terminal-form");
  const input = document.getElementById("terminal-input");
  const output = document.getElementById("terminal-output");

  setTimeout(() => {
    bootScreen.style.display = "none";
    terminalContainer.style.display = "block";
    input.focus();
  }, 8500); // Wait for boot simulation

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const cmd = input.value.trim();
    if (!cmd) return;
    output.innerHTML += "\\nroot@deadnet:~$ " + cmd + "\\n";
    input.value = "";

    try {
      const res = await fetch("/command", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ command: cmd }),
      });
      const data = await res.json();
      output.innerHTML += data.response + "\\n";
    } catch {
      output.innerHTML += "⚠️ Disconnected from DeadNet Core...\\n";
    }

    output.scrollTop = output.scrollHeight;
  });
});
