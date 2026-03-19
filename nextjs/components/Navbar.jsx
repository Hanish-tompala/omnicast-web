"use client";
import Link from "next/link";
import { useState } from "react";
import { navLinks } from "../data/navLinks";

export default function Navbar() {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <nav className="fixed top-6 left-1/2 -translate-x-1/2 w-[95%] max-w-5xl z-50 bg-[#121212]/60 backdrop-blur-xl border border-white/10 rounded-2xl shadow-2xl transition-all">
      <div className="px-6 h-14 flex items-center justify-between relative">
        
        {/* Brand / Logo */}
        <Link href="/" className="flex items-center gap-2 z-10 group">
          <span className="text-[15px] font-bold text-white tracking-tight">
            OmniCast
          </span>
        </Link>

        {/* Desktop Navigation (Centered) */}
        <div className="hidden md:flex items-center gap-8 absolute left-1/2 -translate-x-1/2">
          {navLinks.map((link, index) => (
            <Link
              key={index} 
              href={link.href}
              className="text-[13px] font-medium text-gray-400 hover:text-white transition-colors"
            >
              {link.label}
            </Link>
          ))}
        </div>

        {/* Actions (Right Side) */}
        <div className="hidden md:flex items-center gap-5 z-10">
          <Link href="/" className="px-4 py-1.5 bg-white hover:bg-gray-200 text-black text-[13px] font-bold rounded-lg transition-colors">
            Get Started
          </Link>
        </div>

        {/* Mobile Menu Toggle */}
        <div className="md:hidden flex items-center z-10">
          <button 
            className="p-2 text-white"
            onClick={() => setIsOpen(!isOpen)}
            aria-label="Toggle Menu"
          >
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d={isOpen ? "M6 18L18 6M6 6l12 12" : "M4 6h16M4 12h16M4 18h16"} />
            </svg>
          </button>
        </div>
      </div>

      {/* Mobile Navigation Dropdown */}
      {isOpen && (
        <div className="md:hidden border-t border-white/10 px-6 py-4 space-y-4 rounded-b-2xl bg-black/40 backdrop-blur-2xl">
          {navLinks.map((link, index) => (
            <Link
              key={`mobile-${index}`}
              href={link.href}
              onClick={() => setIsOpen(false)}
              className="block text-sm font-medium text-gray-300 hover:text-white"
            >
              {link.label}
            </Link>
          ))}
          <div className="pt-4 border-t border-white/5 flex flex-col gap-3">
             <Link href="/" className="block text-center w-full px-4 py-2 bg-white text-black text-sm font-bold rounded-lg" onClick={() => setIsOpen(false)}>Get Started</Link>
          </div>
        </div>
      )}
    </nav>
  );
}