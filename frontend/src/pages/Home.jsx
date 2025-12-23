import React from "react";
import NavBar from "../components/NavBar";
import Hero from "../components/Hero";
import AboutSection from "../components/AboutSection";

const Home = () => {
  return (
    <main className="min-h-screen bg-slate-950 text-slate-100">
      <NavBar />
      <Hero />
      <AboutSection />
    </main>
  );
};

export default Home;
