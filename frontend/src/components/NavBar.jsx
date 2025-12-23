import React from "react";
import { useNavigate } from "react-router-dom";

const NavBar = () => {
  const navigate = useNavigate();

  const scrollToAbout = () => {
    const el = document.getElementById("about");
    el?.scrollIntoView({ behavior: "smooth" });
  };

  return (
    <header className="w-full border-b border-slate-800 bg-slate-950/80 backdrop-blur">
      <div className="max-w-6xl mx-auto px-6 py-4 flex items-center justify-between">
        {/* Logo / brand */}
        <div
          className="flex items-center gap-2 cursor-pointer"
          onClick={() => navigate("/")}
        >
          <div className="h-8 w-8 rounded-xl bg-gradient-to-br from-purple-500 to-blue-500 flex items-center justify-center text-xs font-bold">
            CL
          </div>
          <span className="font-semibold tracking-tight text-lg">
            CoLab
          </span>
        </div>

        {/* Nav links */}
        <nav className="hidden md:flex items-center gap-8 text-sm text-slate-300">
          <button
            onClick={scrollToAbout}
            className="hover:text-slate-50 transition"
          >
            About
          </button>

          <button
            onClick={() => navigate("/login")}
            className="px-4 py-2 rounded-full border border-slate-600 text-slate-100 text-sm hover:border-slate-300 hover:bg-slate-900 transition"
          >
            Log in
          </button>
          <button
            onClick={() => navigate("/signup")}
            className="px-5 py-2 rounded-full text-sm font-medium bg-gradient-to-r from-purple-500 via-fuchsia-500 to-blue-500 hover:brightness-110 shadow-lg shadow-purple-500/25 transition"
          >
            Get started
          </button>
        </nav>
      </div>
    </header>
  );
};

export default NavBar;
