import { gsap } from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";

gsap.registerPlugin(ScrollTrigger);

export const useScrollTrigger = (target) => {
  gsap.to(target, {
    scrollTrigger: {
      trigger: target,
      start: "top center",
      end: "bottom center",
      scrub: true,
    },
    x: 500,
  });
};
