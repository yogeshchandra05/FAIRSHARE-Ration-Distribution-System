// static/ration_app/js/user_dashboard.js
document.addEventListener("DOMContentLoaded", () => {
  const cards = document.querySelectorAll(".card");
  const dynamicSection = document.getElementById("dynamic-section");

  // --- Fade-in dashboard cards on load ---
  const cardObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add("visible");
        cardObserver.unobserve(entry.target);
      }
    });
  }, { threshold: 0.2 });

  cards.forEach(card => {
    card.classList.add("fade-up");
    cardObserver.observe(card);
  });

  // --- Handle card clicks (including QR section) ---
  cards.forEach(card => {
    card.addEventListener("click", async () => {
      const section = card.getAttribute("data-section");
      console.log("Clicked section:", section);
      dynamicSection.innerHTML = `<p class="loading">Loading ${section}...</p>`;

      // ✅ Handle QR separately
      if (section === "qr") {
        try {
          const qrResponse = await fetch("/generate_qr/");
          console.log("QR Fetch Status:", qrResponse.status);

          if (!qrResponse.ok) throw new Error("QR fetch failed");

          const blob = await qrResponse.blob();
          const qrURL = URL.createObjectURL(blob);

          dynamicSection.innerHTML = `
            <div class="fade-up visible">
              <h3>Ration QR Code</h3>
              <img src="${qrURL}" alt="Ration QR" class="qr-code">
              <p>Scan this QR code to view your ration details.</p>
            </div>
          `;
        } catch (err) {
          dynamicSection.innerHTML = `<p class="error fade-up visible">❌ Failed to load QR Code.</p>`;
          console.error(err);
        }
        return; // stop further content loading
      }

      // 🕒 Default logic for other sections
      setTimeout(() => {
        dynamicSection.innerHTML = `
          <div class="fade-up visible">
            <h3>${section.charAt(0).toUpperCase() + section.slice(1)} Section</h3>
            <p>Dynamic content for <b>${section}</b> will appear here soon.</p>
          </div>`;
      }, 400);
    });
  });
});
