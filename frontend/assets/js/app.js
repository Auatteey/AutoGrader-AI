/* ============================
   AutoGrader AI — Frontend JS
   ============================ */

/* Highlight current sidebar page */
document.addEventListener("DOMContentLoaded", () => {
  const current = window.location.pathname.split("/").pop();
  const items = document.querySelectorAll(".sidebar li");

  items.forEach((li) => {
    if (li.innerHTML.toLowerCase().includes(current.replace(".php", ""))) {
      li.style.background = "#21262d";
      li.style.borderLeft = "3px solid #6e40ff";
    }
  });
});

/* Animate cards on scroll */
const cards = document.querySelectorAll(".card");

const observer = new IntersectionObserver(
  (entries) => {
    entries.forEach((e) => {
      if (e.isIntersecting) {
        e.target.classList.add("card-visible");
      }
    });
  },
  { threshold: 0.15 }
);

cards.forEach((card) => observer.observe(card));

/* Optional: Toast notifications */
function showToast(message, type = "success") {
  const toast = document.createElement("div");
  toast.className = `toast ${type}`;
  toast.textContent = message;

  document.body.appendChild(toast);
  setTimeout(() => toast.classList.add("visible"), 50);

  setTimeout(() => {
    toast.classList.remove("visible");
    setTimeout(() => toast.remove(), 400);
  }, 3000);
}
