import React from "react";

const AboutSection = () => {
  return (
    <section id="about" className="border-t border-slate-800 bg-slate-950/95">
      <div className="max-w-6xl mx-auto px-6 py-16 md:py-20 grid md:grid-cols-[minmax(0,1.25fr)_minmax(0,1fr)] gap-12 items-start">
        {/* About text */}
        <div>
          <h2 className="text-2xl md:text-3xl font-semibold tracking-tight mb-4">
            About us
          </h2>
          <p className="text-sm md:text-base text-slate-300 leading-relaxed max-w-3xl">
            We&apos;re building an infrastructure for meaningful professional
            connections. Instead of cold DMs and noisy feeds, Connect.Network
            focuses on intent: what you&apos;re working on, what you want next,
            and who can actually help you get there.
          </p>
          <p className="mt-4 text-sm md:text-base text-slate-300 leading-relaxed max-w-3xl">
            Whether you&apos;re exploring a new industry, looking for a
            co-founder, or just want sharper people in your circle, our matching
            engine pairs you with professionals who share your interests,
            ambition, and timezone.
          </p>

          <ul className="mt-6 space-y-3 text-sm md:text-base text-slate-300">
            <li className="flex gap-2">
              <span className="mt-1 h-1.5 w-1.5 rounded-full bg-emerald-400" />
              <span>Curated, 1:1 intros based on your goals.</span>
            </li>
            <li className="flex gap-2">
              <span className="mt-1 h-1.5 w-1.5 rounded-full bg-sky-400" />
              <span>No feeds, no doomscrolling — just conversations.</span>
            </li>
            <li className="flex gap-2">
              <span className="mt-1 h-1.5 w-1.5 rounded-full bg-fuchsia-400" />
              <span>Built for operators, builders, and founders.</span>
            </li>
          </ul>
        </div>

        {/* Demo + stats card */}
        <div className="space-y-6">
          {/* Demo "UI" card */}
          <div className="rounded-3xl border border-slate-800 bg-slate-900/60 backdrop-blur-xl p-5 shadow-2xl shadow-black/40">
            <div className="flex items-center justify-between mb-4">
              <div>
                <p className="text-xs uppercase tracking-[0.2em] text-slate-400">
                  Demo
                </p>
                <p className="mt-1 text-sm font-medium text-slate-100">
                  A match in under 30 seconds
                </p>
              </div>
              <span className="text-[10px] px-2 py-1 rounded-full bg-emerald-500/15 text-emerald-300 border border-emerald-500/40">
                Interactive mock
              </span>
            </div>

            <div className="relative mt-2 rounded-2xl bg-slate-950/70 border border-slate-800 p-4 overflow-hidden">
              {/* avatar row */}
              <div className="flex items-center justify-between gap-3">
                <div className="flex items-center gap-3">
                  <div className="h-10 w-10 rounded-full bg-gradient-to-br from-purple-500 to-blue-500 flex items-center justify-center text-xs font-semibold">
                    PM
                  </div>
                  <div>
                    <p className="text-sm font-medium text-slate-100">
                      Product Manager
                    </p>
                    <p className="text-xs text-slate-400">
                      Fintech • NYC • Series B
                    </p>
                  </div>
                </div>
                <div className="text-[10px] uppercase tracking-wide text-slate-500">
                  Matches with
                </div>
                <div className="flex items-center gap-3">
                  <div className="h-10 w-10 rounded-full bg-gradient-to-br from-emerald-500 to-teal-400 flex items-center justify-center text-xs font-semibold">
                    ENG
                  </div>
                  <div>
                    <p className="text-sm font-medium text-slate-100">
                      ML Engineer
                    </p>
                    <p className="text-xs text-slate-400">
                      AI infra • Remote • Seed
                    </p>
                  </div>
                </div>
              </div>

              {/* connecting line */}
              <div className="mt-4 mb-3 h-px w-full bg-gradient-to-r from-purple-500/0 via-purple-400/60 to-blue-400/0" />

              <div className="flex items-center justify-between text-xs text-slate-400">
                <span>Matched for: AI product strategy</span>
                <span className="text-emerald-300">Next intro in 02:14</span>
              </div>
            </div>
          </div>

          {/* Stats row */}
          <div className="grid grid-cols-3 gap-4">
            <div className="rounded-2xl border border-slate-800 bg-slate-900/70 px-3 py-4 text-center">
              <div className="text-xs text-slate-400">Professionals</div>
              <div className="mt-1 text-xl font-semibold text-slate-50">
                12k+
              </div>
            </div>
            <div className="rounded-2xl border border-slate-800 bg-slate-900/70 px-3 py-4 text-center">
              <div className="text-xs text-slate-400">Valuable calls</div>
              <div className="mt-1 text-xl font-semibold text-slate-50">
                87%
              </div>
            </div>
            <div className="rounded-2xl border border-slate-800 bg-slate-900/70 px-3 py-4 text-center">
              <div className="text-xs text-slate-400">Time to first match</div>
              <div className="mt-1 text-xl font-semibold text-slate-50">
                48h
              </div>
            </div>
          </div>

          <p className="text-[11px] text-slate-500">
            “I found my co-founder here.” — <span className="italic">Ava</span>
          </p>
        </div>
      </div>
    </section>
  );
};

export default AboutSection;
