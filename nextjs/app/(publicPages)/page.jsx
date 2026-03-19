"use client";
import { useState, useRef, useEffect } from "react";

// --- CUSTOM WAVEFORM AUDIO PLAYER COMPONENT ---
const WaveformPlayer = ({ audioUrl, downloadName, chapters = [] }) => {
  const audioRef = useRef(null);
  const progressRef = useRef(null);
  const [isPlaying, setIsPlaying] = useState(false);
  const [progress, setProgress] = useState(0);
  const [currentTime, setCurrentTime] = useState("0:00");
  const [durationStr, setDurationStr] = useState("0:00");
  const [rawDuration, setRawDuration] = useState(0);

  const waveBars = [
    20, 30, 45, 60, 50, 40, 35, 55, 70, 85, 100, 90, 75, 60, 50, 45, 65, 80, 95, 
    85, 70, 60, 50, 40, 30, 45, 60, 75, 90, 100, 85, 70, 55, 45, 35, 50, 65, 80, 
    70, 55, 40, 30, 45, 60, 50, 35, 25, 20
  ];

  const formatTime = (time) => {
    if (isNaN(time)) return "0:00";
    const minutes = Math.floor(time / 60);
    const seconds = Math.floor(time % 60);
    return `${minutes}:${seconds < 10 ? '0' : ''}${seconds}`;
  };

  const togglePlay = () => {
    if (isPlaying) audioRef.current.pause();
    else audioRef.current.play();
    setIsPlaying(!isPlaying);
  };

  const handleTimeUpdate = () => {
    const current = audioRef.current.currentTime;
    const total = audioRef.current.duration;
    setCurrentTime(formatTime(current));
    setProgress((current / total) * 100);
  };

  const handleLoadedMetadata = () => {
    setDurationStr(formatTime(audioRef.current.duration));
    setRawDuration(audioRef.current.duration);
  };

  const handleSeek = (e) => {
    const rect = progressRef.current.getBoundingClientRect();
    const percent = (e.clientX - rect.left) / rect.width;
    audioRef.current.currentTime = percent * audioRef.current.duration;
  };

  const seekToTime = (timeInSeconds) => {
    if (audioRef.current) {
      audioRef.current.currentTime = timeInSeconds;
      if (!isPlaying) {
        audioRef.current.play();
        setIsPlaying(true);
      }
    }
  };

  return (
    <div className="w-full bg-black/60 backdrop-blur-3xl border border-white/10 rounded-2xl p-6 shadow-2xl flex flex-col gap-4">
      <audio ref={audioRef} src={audioUrl} onTimeUpdate={handleTimeUpdate} onLoadedMetadata={handleLoadedMetadata} onEnded={() => setIsPlaying(false)} className="hidden" />
      
      <div ref={progressRef} className="flex items-end gap-[2px] h-16 cursor-pointer group relative" onClick={handleSeek}>
        {waveBars.map((height, i) => {
          const barPercent = (i / waveBars.length) * 100;
          const isActive = barPercent <= progress;
          return <div key={i} style={{ height: `${height}%` }} className={`flex-1 rounded-sm transition-colors duration-75 ${isActive ? 'bg-[#1DB954]' : 'bg-white/10 group-hover:bg-white/20'}`} />
        })}
      </div>

      <div className="w-full h-1 bg-white/10 rounded-full overflow-hidden mt-[-8px] relative">
        <div className="absolute top-0 left-0 h-full bg-[#1DB954]" style={{ width: `${progress}%` }} />
      </div>

      <div className="flex items-center justify-between mt-2">
        <div className="flex items-center gap-4">
          <button onClick={togglePlay} className="w-12 h-12 flex items-center justify-center bg-[#1DB954] hover:bg-[#1ed760] text-black rounded-full transition-transform hover:scale-105 shadow-lg">
            {isPlaying ? <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><path d="M6 19h4V5H6v14zm8-14v14h4V5h-4z"/></svg> : <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor" className="ml-1"><path d="M8 5v14l11-7z"/></svg>}
          </button>
          <button onClick={() => seekToTime(0)} className="w-10 h-10 flex items-center justify-center bg-gray-800 hover:bg-white/10 text-gray-400 hover:text-white rounded-xl transition-colors border border-gray-700">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"/><path d="M3 3v5h5"/></svg>
          </button>
          <div className="text-gray-400 text-sm font-medium">
            {currentTime} / {durationStr}
          </div>
        </div>
        <a href={audioUrl} download={downloadName || "OmniCast_Audio.mp3"} target="_blank" rel="noreferrer" className="flex items-center gap-2 px-5 py-2.5 bg-transparent border border-gray-700 hover:bg-gray-800 text-[#1DB954] rounded-xl font-bold text-sm transition-colors">
          Download
        </a>
      </div>

      {chapters && chapters.length > 0 && (
        <div className="mt-4 pt-4 border-t border-white/10">
          <h4 className="text-sm font-bold text-gray-400 mb-3 uppercase tracking-wider">Chapters</h4>
          <div className="flex flex-col gap-2">
            {chapters.map((chap, idx) => (
              <button key={idx} onClick={() => seekToTime(chap.start_time)} className="flex items-center justify-between p-2 hover:bg-white/5 rounded-lg transition-colors text-left group">
                <span className="text-white text-sm font-medium group-hover:text-[#1DB954] transition-colors">{chap.title}</span>
                <span className="text-xs text-gray-500 font-mono bg-black/40 px-2 py-1 rounded">{formatTime(chap.start_time)}</span>
              </button>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

// Our Database of Murf Voices
const VOICE_OPTIONS = {
  "English": [
    { id: "en-US-marcus", name: "Marcus (Professional Male)" },
    { id: "en-US-terrell", name: "Terrell (Energetic Male)" },
    { id: "en-US-miles", name: "Miles (Deep/Calm Male)" },
    { id: "en-UK-hazel", name: "Hazel (British Female)" },
    { id: "en-US-natalie", name: "Natalie (Friendly Female)" }
  ]
};

export default function OmniPodcastConverter() {
  const [activeTab, setActiveTab] = useState("url"); 
  const [sourceUrl, setSourceUrl] = useState("");
  const [selectedFile, setSelectedFile] = useState(null);
  const [promptText, setPromptText] = useState("");
  const [podcastStyle, setPodcastStyle] = useState("Standard Educational Podcast");
  const [selectedLanguage, setSelectedLanguage] = useState("English");
  const [selectedVoice, setSelectedVoice] = useState(VOICE_OPTIONS["English"][0].id);

  const [isGenerating, setIsGenerating] = useState(false);
  const [audioUrl, setAudioUrl] = useState(null);
  const [chapters, setChapters] = useState([]);
  const [transcriptPreview, setTranscriptPreview] = useState("");
  const [errorMessage, setErrorMessage] = useState("");
  
  const fileInputRef = useRef(null);

  useEffect(() => {
    if (VOICE_OPTIONS[selectedLanguage]) {
      setSelectedVoice(VOICE_OPTIONS[selectedLanguage][0].id);
    }
  }, [selectedLanguage]);

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files.length > 0) {
      setSelectedFile(e.target.files[0]);
    }
  };

  const handleGenerate = async () => {
    if (activeTab === "url" && !sourceUrl) return;
    if (activeTab === "pdf" && !selectedFile) return;
    if (activeTab === "prompt" && !promptText) return;
    
    setIsGenerating(true);
    setErrorMessage("");
    setTranscriptPreview("");
    setAudioUrl(null);
    setChapters([]);
    
    try {
      let res;
      
      if (activeTab === "pdf") {
        const formData = new FormData();
        formData.append("file", selectedFile);
        formData.append("style", podcastStyle);
        formData.append("language", selectedLanguage);
        formData.append("voice_id", selectedVoice);
        
        res = await fetch("http://localhost:8000/api/convert/pdf", {
          method: "POST", body: formData, 
        });
      } else if (activeTab === "url") {
        res = await fetch("http://localhost:8000/api/convert", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ url: sourceUrl, style: podcastStyle, language: selectedLanguage, voice_id: selectedVoice }),
        });
      } else if (activeTab === "prompt") {
        res = await fetch("http://localhost:8000/api/convert/prompt", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ prompt: promptText, style: podcastStyle, language: selectedLanguage, voice_id: selectedVoice }),
        });
      } else if (activeTab === "web") {
        res = await fetch("http://localhost:8000/api/convert/web", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ url: sourceUrl, style: podcastStyle, language: selectedLanguage, voice_id: selectedVoice }),
        });
      } else if (activeTab === "audio") {
        const formData = new FormData();
        formData.append("file", selectedFile);
        formData.append("style", podcastStyle);
        formData.append("language", selectedLanguage);
        formData.append("voice_id", selectedVoice);
        
        res = await fetch("http://localhost:8000/api/convert/audio", {
          method: "POST", body: formData, 
        });
      }

      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || "Failed to connect to the backend.");

      setTranscriptPreview(data.transcript_preview);
      setAudioUrl(data.audio_url);
      setChapters(data.chapters || []);

    } catch (err) {
      setErrorMessage(err.message);
    } finally {
      setIsGenerating(false);
    }
  };

  return (
    <main className="min-h-screen flex flex-col items-center justify-center bg-[#121212] p-6 relative overflow-hidden pt-20">
      {/* Background Gradients */}
      <div className="absolute inset-0 pointer-events-none flex justify-center z-0">
        {/* Main central wide glow behind the title */}
        <div className="absolute top-[5%] w-[120vw] h-[40vh] bg-[#1DB954]/20 blur-[160px] rounded-[100%]" />
        {/* Secondary soft glow behind the cards */}
        <div className="absolute top-[40%] w-[80vw] h-[50vh] bg-[#1DB954]/10 blur-[180px] rounded-[100%]" />
      </div>

      <div className="max-w-4xl w-full space-y-8 text-center mt-10 relative z-10">
        
        <div className="flex justify-center items-center">
          <div className="inline-flex items-center gap-2 px-5 py-2 rounded-full bg-[#1DB954]/10 border border-[#1DB954]/20 text-sm font-medium text-[#1DB954] backdrop-blur-md">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <path d="m12 3-1.912 5.813a2 2 0 0 1-1.275 1.275L3 12l5.813 1.912a2 2 0 0 1 1.275 1.275L12 21l1.912-5.813a2 2 0 0 1 1.275-1.275L21 12l-5.813-1.912a2 2 0 0 1-1.275-1.275L12 3Z"/>
              <path d="M5 3v4M7 5H3"/>
            </svg>
            Voice-First AI Platform &middot; Powered by Murf Falcon
          </div>
        </div>

        <h1 className="text-4xl md:text-6xl font-extrabold tracking-tight text-white mt-4">
          Turn Any Content into an <br />
          <span className="text-[#1DB954]">
            Audio Notebook
          </span>
        </h1>
        <p className="text-lg md:text-xl text-gray-400 font-medium max-w-2xl mx-auto leading-relaxed">
          &quot;Listen to the web seamlessly. Convert your documents, articles, and videos into engaging, studio-quality podcasts instantly.&quot;
        </p>

        <div className="bg-white/5 backdrop-blur-2xl border border-white/10 p-8 rounded-3xl shadow-2xl space-y-6 text-left">
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8 mt-2">
            <div className="flex flex-col gap-1">
              <label className="text-xs font-bold text-gray-400 uppercase tracking-wider">Style</label>
              <select value={podcastStyle} onChange={(e) => setPodcastStyle(e.target.value)} className="bg-black/40 border border-white/10 rounded-xl px-4 py-3 text-sm text-white focus:ring-2 focus:ring-[#1DB954] cursor-pointer hover:bg-black/60 outline-none transition-colors">
                <option className="bg-[#121212] text-white" value="Standard Educational Podcast">🎙️ Single-Speaker Educational</option>
                <option className="bg-[#121212] text-white" value="2-Person Podcast Conversation">🎧 2-Person Podcast (Host & Guest)</option>
                <option className="bg-[#121212] text-white" value="Hype Tech Reviewer on YouTube">🔥 Hype Reviewer</option>
                <option className="bg-[#121212] text-white" value="Calm, relaxing late-night storyteller">🌙 Storyteller</option>
                <option className="bg-[#121212] text-white" value="Fast-paced 60-second executive summary">⚡ Executive Summary</option>
              </select>
            </div>
            <div className="flex flex-col gap-1">
              <label className="text-xs font-bold text-gray-400 uppercase tracking-wider">Language</label>
              <select value={selectedLanguage} onChange={(e) => setSelectedLanguage(e.target.value)} className="bg-black/40 border border-white/10 rounded-xl px-4 py-3 text-sm text-white focus:ring-2 focus:ring-[#1DB954] cursor-pointer hover:bg-black/60 outline-none transition-colors">
                <option className="bg-[#121212] text-white" value="English">🇬🇧 English</option>
                <option className="bg-[#121212] text-gray-500" value="Spanish" disabled>🇪🇸 Spanish (Coming Soon)</option>
                <option className="bg-[#121212] text-gray-500" value="French" disabled>🇫🇷 French (Coming Soon)</option>
                <option className="bg-[#121212] text-gray-500" value="Hindi" disabled>🇮🇳 Hindi (Coming Soon)</option>
              </select>
            </div>
            <div className="flex flex-col gap-1">
              <label className="text-xs font-bold text-gray-400 uppercase tracking-wider">Host Voice</label>
              <select value={selectedVoice} onChange={(e) => setSelectedVoice(e.target.value)} className="bg-black/40 border border-white/10 rounded-xl px-4 py-3 text-sm text-white focus:ring-2 focus:ring-[#1DB954] cursor-pointer hover:bg-black/60 outline-none transition-colors">
                {VOICE_OPTIONS[selectedLanguage]?.map(voice => (
                  <option className="bg-[#121212] text-white" key={voice.id} value={voice.id}>{voice.name}</option>
                ))}
              </select>
            </div>
          </div>

          <div className="flex justify-center gap-2 p-1.5 bg-black/40 border border-white/10 rounded-full mb-6 overflow-x-auto scrollbar-hide">
            <button onClick={() => setActiveTab("url")} className={`flex-shrink-0 px-4 py-2 text-sm font-bold rounded-lg transition-all ${activeTab === "url" ? "bg-[#1DB954] shadow-lg text-black" : "text-gray-400 hover:text-white hover:scale-105"}`}>🔗 YouTube Link</button>
            <button onClick={() => setActiveTab("pdf")} className={`flex-shrink-0 px-4 py-2 text-sm font-bold rounded-lg transition-all ${activeTab === "pdf" ? "bg-[#1DB954] shadow-lg text-black" : "text-gray-400 hover:text-white hover:scale-105"}`}>📄 PDF File</button>
            <button onClick={() => setActiveTab("prompt")} className={`flex-shrink-0 px-4 py-2 text-sm font-bold rounded-lg transition-all ${activeTab === "prompt" ? "bg-[#1DB954] shadow-lg text-black" : "text-gray-400 hover:text-white hover:scale-105"}`}>✍️ AI Story</button>
            <button onClick={() => setActiveTab("web")} className={`flex-shrink-0 px-4 py-2 text-sm font-bold rounded-lg transition-all ${activeTab === "web" ? "bg-[#1DB954] shadow-lg text-black" : "text-gray-400 hover:text-white hover:scale-105"}`}>🌐 Web Article</button>
            <button onClick={() => setActiveTab("audio")} className={`flex-shrink-0 px-4 py-2 text-sm font-bold rounded-lg transition-all ${activeTab === "audio" ? "bg-[#1DB954] shadow-lg text-black" : "text-gray-400 hover:text-white hover:scale-105"}`}>🎤 Upload Media</button>
          </div>

          {activeTab === "url" && (
            <input type="text" placeholder="Paste YouTube URL here..." value={sourceUrl} onChange={(e) => setSourceUrl(e.target.value)} className="w-full bg-black/40 border border-white/10 rounded-2xl px-5 py-4 text-white focus:ring-2 focus:ring-[#1DB954] placeholder:text-gray-500 hover:bg-[#333] outline-none" />
          )}

          {activeTab === "pdf" && (
            <div className="w-full bg-black/20 border-2 border-dashed border-white/20 rounded-2xl hover:bg-black/40 transition-colors cursor-pointer p-6 text-center">
              <input type="file" accept=".pdf" ref={fileInputRef} onChange={handleFileChange} className="hidden" />
              {selectedFile ? (
                <div className="flex justify-between items-center bg-[#333] p-4 rounded-xl border border-white/10 shadow-sm">
                  <span className="font-medium text-white truncate">📄 {selectedFile.name}</span>
                  <button onClick={() => setSelectedFile(null)} className="text-red-500 font-bold hover:text-red-700">✕</button>
                </div>
              ) : (
                <button onClick={() => fileInputRef.current.click()} className="text-[#1DB954] text-lg font-bold hover:underline">Click to Browse PDF</button>
              )}
            </div>
          )}

          {activeTab === "prompt" && (
            <textarea placeholder="Write an educational script..." value={promptText} onChange={(e) => setPromptText(e.target.value)} rows="4" className="w-full bg-black/40 border border-white/10 rounded-2xl px-5 py-4 text-white focus:ring-2 focus:ring-[#1DB954] placeholder:text-gray-500 hover:bg-[#333] outline-none resize-none" />
          )}
          
          
          {activeTab === "web" && (
            <input type="text" placeholder="Paste Medium/Blog URL here..." value={sourceUrl} onChange={(e) => setSourceUrl(e.target.value)} className="w-full bg-black/40 border border-white/10 rounded-2xl px-5 py-4 text-white focus:ring-2 focus:ring-[#1DB954] placeholder:text-gray-500 hover:bg-[#333] outline-none" />
          )}
          {activeTab === "audio" && (
            <div className="w-full bg-black/20 border-2 border-dashed border-white/20 rounded-2xl hover:bg-black/40 transition-colors cursor-pointer p-6 text-center">
              <input type="file" accept="audio/*,video/*" ref={fileInputRef} onChange={handleFileChange} className="hidden" />
              {selectedFile ? (
                <div className="flex justify-between items-center bg-[#333] p-4 rounded-xl border border-white/10 shadow-sm">
                  <span className="font-medium text-white truncate">🎵 {selectedFile.name}</span>
                  <button onClick={() => setSelectedFile(null)} className="text-red-500 font-bold hover:text-red-700">✕</button>
                </div>
              ) : (
                <button onClick={() => fileInputRef.current.click()} className="text-[#1DB954] text-lg font-bold hover:underline">Click to Browse Audio/Video (.mp4, .mp3, .wav)</button>
              )}
            </div>
          )}
          {errorMessage && <div className="text-red-500 text-sm font-medium px-2">Error: {errorMessage}</div>}

          <div className="flex justify-end pt-2">
            <button
              onClick={handleGenerate}
              disabled={isGenerating || ((activeTab === "url" || activeTab === "web") && !sourceUrl) || ((activeTab === "pdf" || activeTab === "audio") && !selectedFile) || (activeTab === "prompt" && !promptText)}
              className={`px-10 py-4 rounded-full text-lg font-bold text-white transition-all ${
                isGenerating || ((activeTab === "url" || activeTab === "web") && !sourceUrl) || ((activeTab === "pdf" || activeTab === "audio") && !selectedFile) || (activeTab === "prompt" && !promptText) 
                ? "bg-black/40 border border-white/10 text-gray-500 cursor-not-allowed" : "bg-[#1DB954] hover:bg-[#1ed760] text-black hover:scale-105 shadow-xl shadow-[#1DB954]/20"
              }`}
            >
              {isGenerating ? "Producing Audio..." : "Generate Audio Notebook"}
            </button>
          </div>
        </div>

        {transcriptPreview && (
          <div className="animate-fade-in-up space-y-6">
            <div className="bg-white/80 dark:bg-gray-900/80 backdrop-blur-xl border border-gray-200 dark:border-white/10 p-6 rounded-2xl shadow-xl text-left">
              <h3 className="text-lg font-bold text-white mb-2 flex items-center gap-2"><span>📄</span> AI Script Preview</h3>
              <p className="text-sm text-gray-300 italic whitespace-pre-wrap">{transcriptPreview}</p>
            </div>

            {audioUrl && (
              <div className="animate-fade-in-up">
                {/* REPLACED DEFAULT AUDIO WITH OUR CUSTOM WAVEFORM PLAYER
                */}
                <WaveformPlayer audioUrl={audioUrl} downloadName="OmniCast_Audio.mp3" chapters={chapters} />
              </div>
            )}
          </div>
        )}
      </div>
    </main>
  );
}