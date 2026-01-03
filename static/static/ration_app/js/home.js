// static/ration_app/js/home.js
document.addEventListener("DOMContentLoaded", () => {
  // --- Background Slideshow ---
  const hero = document.querySelector(".hero");
  if (hero) {
  hero.style.backgroundSize = "cover";
  hero.style.backgroundPosition = "center";
  hero.style.backgroundRepeat = "no-repeat";
  hero.style.backgroundAttachment = "fixed"; 
}

  const images = [
     
    "/static/ration_app/images/slide01.jpg",
    "/static/ration_app/images/slide03.jpg",
    "/static/ration_app/images/slide04.jpg"
  ];
  let current = 0;

  function changeBackground() {
    if (!hero) return;
    hero.style.backgroundImage = `url('${images[current]}')`;
    hero.classList.add("fade");
    setTimeout(() => hero.classList.remove("fade"), 900);
    current = (current + 1) % images.length;
  }

  changeBackground();
  setInterval(changeBackground, 5000); // Change every 5 seconds

  // --- Fade-up reveal for sections ---
  const fadeEls = document.querySelectorAll(".fade-up");

  if ("IntersectionObserver" in window && fadeEls.length) {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add("visible");
          // optional: unobserve so it doesn't trigger again
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.15 });

    fadeEls.forEach(el => observer.observe(el));
  } else {
    // Fallback: make them all visible after a short delay
    setTimeout(() => {
      fadeEls.forEach(el => el.classList.add("visible"));
    }, 400);
  }
});
