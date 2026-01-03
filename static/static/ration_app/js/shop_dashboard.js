document.addEventListener("DOMContentLoaded", () => {
  const cards = document.querySelectorAll(".card");
  const dynamicSection = document.getElementById("dynamic-section");

  // Animate fade-up when visible
  const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add("visible");
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.2 });

  cards.forEach(card => {
    card.classList.add("fade-up");
    observer.observe(card);
  });

  // Dynamic section content
  cards.forEach(card => {
    card.addEventListener("click", () => {
      const section = card.getAttribute("data-section");
      dynamicSection.innerHTML = `<p class="fade-up visible">Loading ${section}...</p>`;

      setTimeout(() => {
        dynamicSection.innerHTML = `
          <div class="fade-up visible">
            <h3>${section.charAt(0).toUpperCase() + section.slice(1)} Section</h3>
            <p>Details for <b>${section}</b> will appear here soon.</p>
          </div>`;
      }, 400);
    });
  });
});
