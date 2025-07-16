document.addEventListener("DOMContentLoaded", () => {
    document.getElementById("viewProfile").addEventListener("click", () => {
      alert("Redirecting to View Profile!");
    });
  
    document.getElementById("settings").addEventListener("click", () => {
      alert("Opening Settings!");
    });
  
    document.getElementById("help").addEventListener("click", () => {
      alert("Redirecting to Help!");
    });
  
    document.getElementById("signOut").addEventListener("click", () => {
      alert("Signing Out!");
    });
  
    const navItems = document.querySelectorAll(".nav-item");
    const profileDropdown = document.querySelector(".profile");
  
    profileDropdown.addEventListener("mouseenter", () => {
      gsap.to(navItems, {
        x: -100,
        duration: 0.5,
        stagger: 0.1,
        ease: "power1.out"
      });
    });
  
    profileDropdown.addEventListener("mouseleave", () => {
      gsap.to(navItems, {
        x: 0,
        duration: 0.5,
        stagger: 0.1,
        ease: "power1.out"
      });
    });
  
    const logoLeft = document.getElementById("logoLeft");
    const logoRight = document.getElementById("logoRight");
    const sparkleLeft = document.getElementById("sparkleLeft");
    const sparkleRight = document.getElementById("sparkleRight");
    const logo = document.getElementById("logo");
  
    logo.addEventListener("mouseenter", () => {
      gsap.to(logoLeft, {
        x: -20,
        opacity: 0.8,
        duration: 0.3,
        ease: "power1.out"
      });
      gsap.to(logoRight, {
        x: 20,
        opacity: 0.8,
        duration: 0.3,
        ease: "power1.out"
      });
  
      createSparkles(sparkleLeft);
      createSparkles(sparkleRight);
    });
  
    logo.addEventListener("mouseleave", () => {
      gsap.to([logoLeft, logoRight], {
        x: 0,
        opacity: 1,
        duration: 0.3,
        ease: "power1.out"
      });
  
      clearSparkles(sparkleLeft);
      clearSparkles(sparkleRight);
    });
  
    function createSparkles(container) {
      for (let i = 0; i < 10; i++) {
        const sparkle = document.createElement("div");
        sparkle.classList.add("sparkle");
        sparkle.style.top = `${Math.random() * 100}%`;
        sparkle.style.left = `${Math.random() * 100}%`;
        sparkle.style.animationDelay = `${Math.random()}s`;
        container.appendChild(sparkle);
      }
    }
  
    function clearSparkles(container) {
      while (container.firstChild) {
        container.removeChild(container.firstChild);
      }
    }
  });
  