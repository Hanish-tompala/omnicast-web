import os
import re

path = r'h:\projects2\murf ai\nextjs\app\(publicPages)\notebooks\page.jsx'
with open(path, 'r', encoding='utf-8') as f:
    code = f.read()

# 1. State hook additions
new_state = '''  const [error, setError] = useState(null);
  
  // Chat Feature States
  const [activeChatPodcastId, setActiveChatPodcastId] = useState(null);
  const [chatInput, setChatInput] = useState("");
  const [chatHistory, setChatHistory] = useState({});
  const [isChatting, setIsChatting] = useState(false);'''

code = code.replace('  const [error, setError] = useState(null);', new_state)

# 2. Chat Logic Handler
chat_handler = '''
  const handleChat = async (podcastId) => {
    if (!chatInput.trim()) return;
    
    setIsChatting(true);
    const userMessage = chatInput;
    setChatInput("");
    
    // Optimistic UI update
    setChatHistory(prev => ({
      ...prev,
      [podcastId]: [...(prev[podcastId] || []), { role: "user", content: userMessage }]
    }));
    
    try {
      const res = await fetch("http://localhost:8000/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ podcast_id: podcastId, question: userMessage })
      });
      const data = await res.json();
      
      if (!res.ok) throw new Error(data.detail || "Failed to chat");
      
      setChatHistory(prev => ({
        ...prev,
        [podcastId]: [...(prev[podcastId] || []), { role: "assistant", content: data.answer }]
      }));
    } catch (err) {
      alert("Chat Error: " + err.message);
    } finally {
      setIsChatting(false);
    }
  };

  return ('''
code = code.replace('  return (', chat_handler)


# 3. Chat UI inside the card (under audio and download)
chat_ui = '''
                <div className="mt-auto space-y-3">
                  <audio controls className="w-full h-10" src={podcast.audio_url}>
                    Your browser does not support the audio element.
                  </audio>
                  <div className="flex gap-2">
                    <a 
                      href={podcast.audio_url} 
                      download={`OmniCast_${podcast.id}.mp3`}
                      target="_blank"
                      rel="noreferrer"
                      className="flex-1 text-center px-4 py-2 bg-[#282828] hover:bg-[#333] border border-white/10 text-white rounded-full font-bold text-sm transition-colors"
                    >
                      💾 Download
                    </a>
                    <button 
                      onClick={() => setActiveChatPodcastId(activeChatPodcastId === podcast.id ? null : podcast.id)}
                      className={`px-4 py-2 rounded-full font-bold text-sm transition-colors ${activeChatPodcastId === podcast.id ? "bg-[#1DB954] text-black shadow-lg" : "bg-purple-600/20 text-purple-400 hover:bg-purple-600/40 border border-purple-500/20"}`}
                    >
                      💬 Chat AI
                    </button>
                  </div>
                </div>

                {/* THE CHAT UI */}
                {activeChatPodcastId === podcast.id && (
                  <div className="mt-4 pt-4 border-t border-white/10 animate-fade-in-up flex flex-col gap-3">
                    <div className="flex-1 max-h-48 overflow-y-auto space-y-3 pr-2 scrollbar-thin scrollbar-thumb-white/10 scrollbar-track-transparent">
                      {(chatHistory[podcast.id] || []).map((msg, idx) => (
                        <div key={idx} className={`p-3 rounded-2xl text-sm ${msg.role === "user" ? "bg-[#282828] text-white ml-6 rounded-tr-none" : "bg-[#1DB954]/10 border border-[#1DB954]/20 text-green-100 mr-6 rounded-tl-none"}`}>
                          <strong>{msg.role === "user" ? "You" : "AI Notebook"}:</strong> {msg.content}
                        </div>
                      ))}
                      {isChatting && <div className="text-sm text-gray-500 italic animate-pulse">Thinking...</div>}
                      {(chatHistory[podcast.id] || []).length === 0 && (
                        <div className="text-sm text-gray-500 text-center py-4">Ask any question about this notebook! The AI will answer based purely on the transcript.</div>
                      )}
                    </div>
                    
                    <div className="flex gap-2 mt-2">
                      <input 
                        type="text" 
                        placeholder="e.g. What was the main takeaway?" 
                        value={chatInput}
                        onChange={(e) => setChatInput(e.target.value)}
                        onKeyDown={(e) => e.key === "Enter" && handleChat(podcast.id)}
                        className="flex-1 bg-black/40 border border-white/10 rounded-full px-4 text-sm text-white focus:ring-2 focus:ring-[#1DB954] outline-none placeholder:text-gray-600"
                      />
                      <button 
                        onClick={() => handleChat(podcast.id)}
                        disabled={isChatting}
                        className="w-10 h-10 shrink-0 bg-[#1DB954] hover:bg-[#1ed760] text-black rounded-full flex items-center justify-center font-bold disabled:opacity-50"
                      >
                        ↑
                      </button>
                    </div>
                  </div>
                )}
'''

# Find the section containing the audio and download link and replace it with our new grid
old_audio_section = r'''<div className="mt-auto space-y-3">.*?💾 Download MP3.*?</a>\s*</div>'''
code = re.sub(old_audio_section, chat_ui, code, flags=re.DOTALL)


with open(path, 'w', encoding='utf-8') as f:
    f.write(code)
print("Updated notebooks/page.jsx successfully")
