import { gsap } from "gsap";
import { CustomEase } from "gsap/CustomEase";

gsap.registerPlugin(CustomEase);

export const useCustomEase = (target) => {
  CustomEase.create("myEase", "M0,0 C0.126,0.382 0.186,1 1,1");
  gsap.to(target, { x: 300, duration: 2, ease: "myEase" });
};
