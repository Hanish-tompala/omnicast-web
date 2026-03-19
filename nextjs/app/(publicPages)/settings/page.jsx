export default function SettingsPage() {
  return (
    <main className="min-h-screen bg-[#121212] pt-32 px-6 relative overflow-hidden flex flex-col items-center">
      {/* Background Gradients */}
      <div className="absolute inset-0 pointer-events-none flex justify-center z-0">
        {/* Main central wide glow */}
        <div className="absolute top-[10%] w-[120vw] h-[40vh] bg-[#1DB954]/15 blur-[160px] rounded-[100%]" />
        {/* Secondary soft glow */}
        <div className="absolute top-[50%] w-[80vw] h-[50vh] bg-[#1DB954]/5 blur-[180px] rounded-[100%]" />
      </div>

      <div className="max-w-3xl w-full relative z-10 space-y-8">
        <h1 className="text-4xl md:text-5xl font-extrabold tracking-tight text-white mb-2">
          Settings
        </h1>
        
        <div className="bg-white/5 backdrop-blur-2xl border border-white/10 p-8 rounded-3xl shadow-2xl space-y-6 text-left">
          <div className="bg-black/40 border border-white/10 p-6 rounded-2xl">
            <h2 className="text-xl font-bold text-white mb-2">Preferences</h2>
            <p className="text-gray-400 text-sm">
              API keys, default voice preferences, and account configurations will go here.
            </p>
          </div>
        </div>
      </div>
    </main>
  );
}