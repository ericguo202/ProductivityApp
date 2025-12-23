import React, { useState, useEffect, useRef } from "react";
import { useNavigate } from "react-router-dom";

const Hero = () => {
  const words = ["Create", "Change", "Revolutionize", "Build", "Inspire"];
  const [index, setIndex] = useState(0);
  const vantaRef = useRef(null);
  const navigate = useNavigate();

  // Rotating words
  useEffect(() => {
    const interval = setInterval(
      () => setIndex((prev) => (prev + 1) % words.length),
      5000
    );
    return () => clearInterval(interval);
  }, []);

  // Vanta BIRDS background
  useEffect(() => {
    if (!vantaRef.current) return;

    // In case scripts haven’t loaded for some reason
    if (!window.VANTA || !window.VANTA.BIRDS) return;

    const effect = window.VANTA.BIRDS({
      el: vantaRef.current,
      mouseControls: true,
      touchControls: true,
      gyroControls: false,
      minHeight: 200.0,
      minWidth: 200.0,
      scale: 0.8, //old 1 
      scaleMobile: 1.0,

      // your custom settings (from the snippet)
      color1: 0x8d2ec3,
      color2: 0x00ca, // same as 0xca but 4-digit hex
      colorMode: "lerpGradient",
      birdSize: 1, // 2.5 old 
      separation: 65.0,  // old 41
      quantity: 5.0,   //3 old
    });

    // cleanup on unmount
    return () => {
      effect && effect.destroy();
    };
  }, []);

  const scrollToAbout = () => {
    const el = document.getElementById("about");
    el?.scrollIntoView({ behavior: "smooth" });
  };

  return (
    <section className="relative overflow-hidden min-h-[75vh]">
      {/* VANTA background (canvas gets injected here) */}
      <div ref={vantaRef} className="absolute inset-0 z-0" />

      {/* Hero content */}
      <div className="relative z-10 max-w-6xl mx-auto px-6 pt-24 pb-28 flex flex-col items-start">
        <p className="mb-3 text-xs uppercase tracking-[0.25em] text-slate-200 font-semibold">
          A better way to connect.
        </p>

        <h1 className="antialiased text-4xl sm:text-5xl md:text-6xl font-semibold leading-tight tracking-tight text-white">
          Find others to
          <br />
          <span
            key={index}
            className="hero-word inline-block bg-gradient-to-r from-purple-300 via-fuchsia-400 to-blue-300 bg-clip-text text-transparent"
          >
            {words[index]}
          </span>
        </h1>

        <p className="mt-6 text-base md:text-lg text-slate-200 max-w-xl">
          CoLab matches ambitious professionals based on their goals,
          skills, and industries — so every conversation moves you forward, not
          sideways.
        </p>

        <div className="mt-8 flex flex-wrap items-center gap-4">
          <button
            onClick={() => navigate("/signup")}
            className="px-7 py-3 rounded-full text-sm md:text-base font-medium bg-gradient-to-r from-purple-500 via-fuchsia-500 to-blue-500 hover:brightness-110 shadow-xl shadow-purple-500/35 transition"
          >
            Join the network
          </button>

          <button
            onClick={scrollToAbout}
            className="px-7 py-3 rounded-full text-sm md:text-base font-medium border border-slate-400/60 text-slate-100 hover:border-slate-100 hover:bg-slate-900/70 transition"
          >
            See how it works
          </button>
        </div>

        <p className="mt-5 text-xs text-slate-200">
          Start your journey now.
        </p>
      </div>
    </section>
  );
};

export default Hero;
