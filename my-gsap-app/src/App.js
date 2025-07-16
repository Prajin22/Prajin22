import React, { useEffect, useRef } from "react";
import { gsap } from "gsap";
import { Flip, ScrollTrigger, Observer, ScrollToPlugin, Draggable, MotionPathPlugin, TextPlugin } from "gsap/all";

gsap.registerPlugin(Flip, ScrollTrigger, Observer, ScrollToPlugin, Draggable, MotionPathPlugin, TextPlugin);

const App = () => {
  const boxRef = useRef(null);
  const textRef = useRef(null);
  const circleRef = useRef(null);
  const containerRef = useRef(null);

  useEffect(() => {
    const flipState = Flip.getState(containerRef.current.children);
    gsap.to(containerRef.current.children, {
      x: 100,
      rotationY: 180,
      scale: 1.2,
      duration: 1,
      ease: "expo.out",
    });
    Flip.from(flipState, {
      duration: 1.5,
      ease: "expo.inOut",
    });

    gsap.to(boxRef.current, {
      scrollTrigger: {
        trigger: boxRef.current,
        start: "top 75%",
        end: "bottom 25%",
        scrub: true,
        markers: false,
      },
      rotation: 720,
      x: 300,
      y: 200,
      scale: 1.5,
      opacity: 0.5,
      ease: "power4.out",
    });

    gsap.to(textRef.current, {
      text: "Creative GSAP Animations!",
      duration: 3,
      ease: "power2.inOut",
      delay: 1,
    });

    gsap.to(circleRef.current, {
      motionPath: {
        path: [
          { x: 0, y: 0 },
          { x: 300, y: 300 },
          { x: 0, y: 600 },
          { x: -300, y: 300 },
        ],
        curviness: 2,
        autoRotate: true,
      },
      duration: 5,
      ease: "none",
      repeat: -1,
    });

    Draggable.create(circleRef.current, {
      bounds: containerRef.current,
      throwProps: true,
      onDrag: () => {
        gsap.to(circleRef.current, { scale: 1.2, duration: 0.2 });
      },
      onRelease: () => {
        gsap.to(circleRef.current, {
          scale: 1,
          duration: 0.5,
          ease: "elastic.out(1, 0.3)",
        });
      },
    });

    Observer.create({
      target: containerRef.current,
      onMove: () => {
        gsap.to(containerRef.current, {
          rotation: "+=5",
          scale: 1.1,
          duration: 0.5,
        });
      },
      onDown: () => {
        gsap.to(containerRef.current, { opacity: 0.5, duration: 0.3 });
      },
      onUp: () => {
        gsap.to(containerRef.current, { opacity: 1, duration: 0.3 });
      },
    });
  }, []);

  return (
    <div style={{ padding: "20px", backgroundColor: "#f0f0f0", minHeight: "100vh" }}>
      {}
      <div
        ref={containerRef}
        style={{ display: "flex", gap: "20px", marginBottom: "50px", perspective: "1000px" }}
      >
        <div
          style={{
            width: "100px",
            height: "100px",
            backgroundColor: "red",
            transformStyle: "preserve-3d",
            borderRadius: "10px",
          }}
        ></div>
        <div
          style={{
            width: "100px",
            height: "100px",
            backgroundColor: "green",
            transformStyle: "preserve-3d",
            borderRadius: "10px",
          }}
        ></div>
      </div>

      {}
      <div
        ref={boxRef}
        className="box"
        style={{
          width: "100px",
          height: "100px",
          backgroundColor: "blue",
          marginBottom: "50px",
          borderRadius: "10px",
        }}
      ></div>

      {}
      <h1 ref={textRef} style={{ marginBottom: "50px", color: "#333", fontSize: "24px" }}>
        Hello
      </h1>

      {}
      <div
        ref={circleRef}
        style={{
          width: "50px",
          height: "50px",
          borderRadius: "50%",
          backgroundColor: "orange",
          marginBottom: "50px",
        }}
      ></div>
    </div>
  );
};

export default App;
