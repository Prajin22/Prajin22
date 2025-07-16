document.addEventListener("DOMContentLoaded", () => {
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
    const interactiveElements = document.querySelectorAll('button, input, select, textarea, a');
    interactiveElements.forEach(element => {
        element.addEventListener('mouseenter', () => {
            cursor.classList.add('hover');
        });
        
        element.addEventListener('mouseleave', () => {
            cursor.classList.remove('hover');
        });
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

    // Password match green border (signup page)
    const password = document.querySelector('input[name="password"]');
    const confirmPassword = document.querySelector('input[name="confirmPassword"]');
    function checkPasswordMatch() {
        if (password && confirmPassword) {
            if (password.value && confirmPassword.value && password.value === confirmPassword.value) {
                password.style.border = "2px solid green";
                confirmPassword.style.border = "2px solid green";
            } else {
                password.style.border = "1px solid #ccc";
                confirmPassword.style.border = "1px solid #ccc";
            }
        }
    }
    if (password && confirmPassword) {
        password.addEventListener('input', checkPasswordMatch);
        confirmPassword.addEventListener('input', checkPasswordMatch);
    }

    const form = document.getElementById("signupForm");

    form.addEventListener("submit", (event) => {
        const userType = document.getElementById("userType").value;
        const email = document.getElementById("email").value;

        const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailPattern.test(email)) {
            alert("Please enter a valid email address.");
            event.preventDefault();
            return;
        }

        if (userType === "recruiter") {
            const trustedDomains = ["companydomain.com", "officialdomain.com"];
            const emailDomain = email.split("@")[1];

            if (!trustedDomains.includes(emailDomain)) {
                alert("Please use an official company email address.");
                event.preventDefault();
                return;
            }
        }

        const password = document.getElementById("password").value;
        const confirmPassword = document.getElementById("confirmPassword").value;

        if (password !== confirmPassword) {
            alert("Passwords do not match.");
            event.preventDefault();
        }
    });

    gsap.from(".animated-title", {
        duration: 1.2,
        y: -50,
        opacity: 0,
        ease: "bounce.out"
    });

    gsap.from("fieldset", {
        duration: 1,
        x: -50,
        opacity: 0,
        stagger: 0.2,
        ease: "power2.out"
    });

    const buttons = document.querySelectorAll(".role-button, button");
    gsap.from(buttons, {
        duration: 1,
        scale: 0.8,
        opacity: 0,
        stagger: 0.3,
        ease: "elastic.out(1, 0.3)"
    });

    buttons.forEach((button) => {
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
                backgroundColor: "#0073b1",
                color: "#fff"
            });
        });
    });

    const jobSeekerBtn = document.getElementById("jobSeekerBtn");
    const recruiterBtn = document.getElementById("recruiterBtn");

    if (jobSeekerBtn) {
        jobSeekerBtn.addEventListener("click", () => {
            location.href = jobSeekerBtn.dataset.url;
        });
    }

    if (recruiterBtn) {
        recruiterBtn.addEventListener("click", () => {
            location.href = recruiterBtn.dataset.url;
        });
    }

    const verifyPanButton = document.getElementById("verifyPanButton");
    const businessPancardInput = document.getElementById("businessPancard");
    const verificationStatus = document.getElementById("verificationStatus");
    const companyDetails = document.getElementById("companyDetails");
    const submitButton = document.querySelector(".animated-submit");

    if (verifyPanButton) {
        verifyPanButton.addEventListener("click", () => {
            const panNumber = businessPancardInput.value.trim();

            if (!panNumber) {
                verificationStatus.textContent = "Please enter a PAN number to verify.";
                verificationStatus.style.color = "red";
                shakeElement(businessPancardInput);
                return;
            }

            const panDatabase = {
                "U74900UP2011PTC045365": "Google",
                "U74899DL1988PTC032549": "Microsoft",
                "L22210MH1995PLC084781": "TCS",
                "U72200KA2009PLC050684": "Infosys",
                "U74120TG2004PTC043417": "Deloitte"
            };

            if (panDatabase[panNumber]) {
                verifyPanButton.textContent = "Verified";
                verifyPanButton.style.backgroundColor = "Green";
                verificationStatus.textContent = `Welcome ${panDatabase[panNumber]}! Your PAN Number is Verified.`;
                verificationStatus.style.color = "green";
                unlockFields();
            } else {
                verifyPanButton.textContent = "Not Verified";
                verifyPanButton.style.backgroundColor = "Red";
                verificationStatus.textContent = "Sorry! Your PAN Number is not Verified.";
                verificationStatus.style.color = "red";
                shakeElement(businessPancardInput);
            }
        });
    }

    function unlockFields() {
        if (companyDetails) {
            companyDetails.classList.remove("locked");
        }
        if (submitButton) {
            submitButton.classList.remove("locked");
            submitButton.disabled = false;
        }

        if (companyDetails) {
            gsap.to(companyDetails, { opacity: 1, duration: 0.5 });
        }
        if (submitButton) {
            gsap.to(submitButton, { opacity: 1, duration: 0.5 });
        }
    }

    function shakeElement(element) {
        gsap.fromTo(
            element,
            { x: -10 },
            { x: 10, repeat: 5, yoyo: true, duration: 0.2 }
        );
    }
});
