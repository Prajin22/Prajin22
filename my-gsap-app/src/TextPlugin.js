import { gsap } from "gsap";
import { TextPlugin } from "gsap/TextPlugin";

gsap.registerPlugin(TextPlugin);

export const useTextPlugin = (target, newText) => {
  gsap.to(target, { text: newText, duration: 2 });
};
