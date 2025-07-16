document.addEventListener("DOMContentLoaded", () => {
    // Password field green border on input
    const password = document.querySelector('input[type="password"]');
    if (password) {
        password.addEventListener('input', () => {
            if (password.value.length > 0) {
                password.style.border = "2px solid green";
            } else {
                password.style.border = "1px solid #ccc";
            }
        });
    }

    // Custom cursor functionality
    const cursor = document.querySelector('.custom-cursor');
    const floatingElements = document.querySelectorAll('.floating-element');
    
    // Track mouse movement for custom cursor
    document.addEventListener('mousemove', (e) => {
        cursor.style.left = e.clientX + 'px';
        cursor.style.top = e.clientY + 'px';
        
        // Check distance to floating elements and make them move away
        floatingElements.forEach(element => {
            const rect = element.getBoundingClientRect();
            const elementCenterX = rect.left + rect.width / 2;
            const elementCenterY = rect.top + rect.height / 2;
            
            const distance = Math.sqrt(
                Math.pow(e.clientX - elementCenterX, 2) + 
                Math.pow(e.clientY - elementCenterY, 2)
            );
            
            // If cursor is within 100px of element, make it move away (reduced from 150px)
            if (distance < 100) {
                const angle = Math.atan2(e.clientY - elementCenterY, e.clientX - elementCenterX);
                const moveX = Math.cos(angle) * 80; // Increased movement distance
                const moveY = Math.sin(angle) * 80;
                
                gsap.to(element, {
                    duration: 0.3, // Faster response
                    x: -moveX,
                    y: -moveY,
                    scale: 0.6, // More dramatic scale down
                    opacity: 0.2, // More transparent
                    ease: "power2.out"
                });
            } else {
                // Return to original position
                gsap.to(element, {
                    duration: 0.6, // Slightly faster return
                    x: 0,
                    y: 0,
                    scale: 1,
                    opacity: 1,
                    ease: "elastic.out(1, 0.3)"
                });
            }
        });
    });
    
    // Add hover effect to cursor
    document.addEventListener('mouseenter', () => {
        cursor.style.opacity = '1';
    });
    
    document.addEventListener('mouseleave', () => {
        cursor.style.opacity = '0';
    });
    
    // Add hover class to cursor when hovering over interactive elements
    const interactiveElements = document.querySelectorAll('button, input, a');
    interactiveElements.forEach(element => {
        element.addEventListener('mouseenter', () => {
            cursor.classList.add('hover');
        });
        
        element.addEventListener('mouseleave', () => {
            cursor.classList.remove('hover');
        });
    });

    // Original GSAP animations
    gsap.from(".animated-title", {
        duration: 1.2,
        y: -50,
        opacity: 0,
        ease: "bounce.out"
    });

    gsap.from("input", {
        duration: 1,
        x: -50,
        opacity: 0,
        stagger: 0.2,
        ease: "power2.out"
    });

    gsap.from(".animated-submit", {
        duration: 1,
        scale: 0.8,
        opacity: 0,
        delay: 1,
        ease: "elastic.out(1, 0.3)"
    });

    // Floating elements entrance animation
    gsap.from(".floating-element", {
        duration: 2,
        scale: 0,
        opacity: 0,
        stagger: 0.2,
        ease: "back.out(1.7)",
        delay: 0.5
    });

    const button = document.querySelector(".animated-submit");
    button.addEventListener("mouseenter", () => {
        gsap.to(button, {
            duration: 0.3,
            scale: 1.1,
            backgroundColor: "#005f8d",
            color: "#fff"
        });
    });

    button.addEventListener("mouseleave", () => {
        gsap.to(button, {
            duration: 0.3,
            scale: 1,
            backgroundColor: "#1a73e8",
            color: "#fff"
        });
    });
    
    // Add particle trail effect
    let particles = [];
    document.addEventListener('mousemove', (e) => {
        if (Math.random() > 0.9) { // 10% chance to create particle
            createParticle(e.clientX, e.clientY);
        }
    });
    
    function createParticle(x, y) {
        const particle = document.createElement('div');
        particle.style.position = 'fixed';
        particle.style.left = x + 'px';
        particle.style.top = y + 'px';
        particle.style.width = '4px';
        particle.style.height = '4px';
        particle.style.background = 'rgba(255, 255, 255, 0.8)';
        particle.style.borderRadius = '50%';
        particle.style.pointerEvents = 'none';
        particle.style.zIndex = '9998';
        
        document.body.appendChild(particle);
        
        gsap.to(particle, {
            duration: 1,
            x: (Math.random() - 0.5) * 100,
            y: (Math.random() - 0.5) * 100,
            opacity: 0,
            scale: 0,
            ease: "power2.out",
            onComplete: () => {
                document.body.removeChild(particle);
            }
        });
    }
});
