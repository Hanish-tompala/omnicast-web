export default function Footer() {
    return (
        <footer className="w-full bg-black/40 border-t border-white/10 py-12 px-6 mt-16 relative z-10 backdrop-blur-xl">
            <div className="max-w-6xl mx-auto flex flex-col md:flex-row justify-between items-center gap-6">
                
                {/* Brand / Copyright */}
                <div className="flex flex-col items-center md:items-start gap-3">
                    <span className="text-xl font-bold text-white tracking-tight flex items-center gap-2">
                        OmniCast
                    </span>
                    <p className="text-sm font-medium text-gray-400">
                        © {new Date().getFullYear()} OmniCast. All rights reserved.
                    </p>
                </div>

                {/* Developer Info */}
                <div className="flex flex-col items-center md:items-end gap-3">
                    <p className="text-sm font-medium text-gray-300">
                        Developed by <span className="text-[#1DB954] font-bold">Hanish Tompala</span>
                    </p>
                    <div className="flex items-center gap-6 mt-1">
                        <a 
                            href="mailto:hanishtompla@gmail.com" 
                            className="flex items-center gap-2 text-sm font-medium text-gray-400 hover:text-white transition-colors group"
                        >
                            <svg className="w-5 h-5 text-gray-500 group-hover:text-[#1DB954] transition-colors" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"></path></svg>
                            hanishtompla@gmail.com
                        </a>
                        <a 
                            href="https://portfolio-hanish3s-projects.vercel.app/" 
                            target="_blank" 
                            rel="noopener noreferrer"
                            className="flex items-center gap-2 text-sm font-medium text-gray-400 hover:text-white transition-colors group"
                        >
                            <svg className="w-5 h-5 text-gray-500 group-hover:text-[#1DB954] transition-colors" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2 2v2m4 6h.01M5 20h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"></path></svg>
                            Portfolio
                        </a>
                    </div>
                </div>

            </div>
        </footer>
    );
}