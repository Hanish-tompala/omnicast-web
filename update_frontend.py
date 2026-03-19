import os
import re

path = r'h:\projects2\murf ai\nextjs\app\(publicPages)\page.jsx'
with open(path, 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Update WaveformPlayer definition and render
new_player = '''const WaveformPlayer = ({ audioUrl, downloadName, chapters = [] }) => {
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
};'''

# Replace the WaveformPlayer definition completely
code = re.sub(r'const WaveformPlayer = \(\{ audioUrl, downloadName \}\) => \{.*?\};\n\n\n// Our Database', new_player + '\n\n// Our Database', code, flags=re.DOTALL)

# 2. Add chapters to state
code = code.replace('const [audioUrl, setAudioUrl] = useState(null);', 'const [audioUrl, setAudioUrl] = useState(null);\n  const [chapters, setChapters] = useState([]);')
code = code.replace('setAudioUrl(null);', 'setAudioUrl(null);\n    setChapters([]);')

# 3. Handle Web Tab
tabs = '''<div className="flex gap-2 p-1.5 bg-[#282828] rounded-full mb-6 border border-white/5 overflow-x-auto scroolbar-hide">
            <button onClick={() => setActiveTab("url")} className={`flex-shrink-0 px-4 py-2 text-sm font-bold rounded-lg transition-all ${activeTab === "url" ? "bg-[#1DB954] shadow-lg text-black" : "text-gray-400 hover:text-white hover:scale-105"}`}>🔗 YouTube Link</button>
            <button onClick={() => setActiveTab("pdf")} className={`flex-shrink-0 px-4 py-2 text-sm font-bold rounded-lg transition-all ${activeTab === "pdf" ? "bg-[#1DB954] shadow-lg text-black" : "text-gray-400 hover:text-white hover:scale-105"}`}>📄 PDF File</button>
            <button onClick={() => setActiveTab("prompt")} className={`flex-shrink-0 px-4 py-2 text-sm font-bold rounded-lg transition-all ${activeTab === "prompt" ? "bg-[#1DB954] shadow-lg text-black" : "text-gray-400 hover:text-white hover:scale-105"}`}>✍️ AI Story</button>
            <button onClick={() => setActiveTab("web")} className={`flex-shrink-0 px-4 py-2 text-sm font-bold rounded-lg transition-all ${activeTab === "web" ? "bg-[#1DB954] shadow-lg text-black" : "text-gray-400 hover:text-white hover:scale-105"}`}>🌐 Web Article</button>
            <button onClick={() => setActiveTab("audio")} className={`flex-shrink-0 px-4 py-2 text-sm font-bold rounded-lg transition-all ${activeTab === "audio" ? "bg-[#1DB954] shadow-lg text-black" : "text-gray-400 hover:text-white hover:scale-105"}`}>🎤 Upload Media</button>
          </div>'''
code = re.sub(r'<div className="flex gap-2 p-1.5 bg-\[#282828\] rounded-full mb-6 border border-white/5">.*?</div>', tabs, code, flags=re.DOTALL)

# 4. Handle Inputs
web_input = '''
          {activeTab === "web" && (
            <input type="text" placeholder="Paste Medium/Blog URL here..." value={sourceUrl} onChange={(e) => setSourceUrl(e.target.value)} className="w-full bg-[#282828] border-none rounded-2xl px-5 py-4 text-white focus:ring-2 focus:ring-[#1DB954] placeholder:text-gray-500 hover:bg-[#333] outline-none" />
          )}'''
audio_input = '''
          {activeTab === "audio" && (
            <div className="w-full bg-[#282828]/50 border-2 border-dashed border-white/20 rounded-2xl hover:bg-[#282828] transition-colors cursor-pointer p-6 text-center">
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
          )}'''
code = code.replace('{errorMessage &&', web_input + audio_input + '\n          {errorMessage &&')

# 5. Disable condition
dis_oldStr = 'disabled={isGenerating || (activeTab === "url" && !sourceUrl) || (activeTab === "pdf" && !selectedFile) || (activeTab === "prompt" && !promptText)}'
dis_newStr = 'disabled={isGenerating || ((activeTab === "url" || activeTab === "web") && !sourceUrl) || ((activeTab === "pdf" || activeTab === "audio") && !selectedFile) || (activeTab === "prompt" && !promptText)}'
code = code.replace(dis_oldStr, dis_newStr)
class_oldStr = 'isGenerating || (activeTab === "url" && !sourceUrl) || (activeTab === "pdf" && !selectedFile) || (activeTab === "prompt" && !promptText)'
class_newStr = 'isGenerating || ((activeTab === "url" || activeTab === "web") && !sourceUrl) || ((activeTab === "pdf" || activeTab === "audio") && !selectedFile) || (activeTab === "prompt" && !promptText)'
code = code.replace(class_oldStr, class_newStr)

# 6. Fetch updates
handle_gen_old = '''} else if (activeTab === "prompt") {
        res = await fetch("http://localhost:8000/api/convert/prompt", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ prompt: promptText, style: podcastStyle, language: selectedLanguage, voice_id: selectedVoice }),
        });
      }'''
handle_gen_new = '''} else if (activeTab === "prompt") {
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
      }'''
code = code.replace(handle_gen_old, handle_gen_new)

# 7. Update data mapping
code = code.replace('setTranscriptPreview(data.transcript_preview);\n      setAudioUrl(data.audio_url);', 'setTranscriptPreview(data.transcript_preview);\n      setAudioUrl(data.audio_url);\n      setChapters(data.chapters || []);')

# 8. Render WaveformPlayer
code = code.replace('<WaveformPlayer audioUrl={audioUrl} downloadName="OmniCast_Audio.mp3" />', '<WaveformPlayer audioUrl={audioUrl} downloadName="OmniCast_Audio.mp3" chapters={chapters} />')

with open(path, 'w', encoding='utf-8') as f:
    f.write(code)
print("Updated page.jsx successfully")
