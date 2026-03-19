"use client";
import { useState, useEffect } from "react";
import Link from "next/link";

export default function AudioNotebooks() {
  const [podcasts, setPodcasts] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);
  
  // Chat Feature States
  const [activeChatPodcastId, setActiveChatPodcastId] = useState(null);
  const [chatInput, setChatInput] = useState("");
  const [chatHistory, setChatHistory] = useState({});
  const [isChatting, setIsChatting] = useState(false);

  useEffect(() => {
    fetchPodcasts();
  }, []);

  const fetchPodcasts = async () => {
    try {
      const res = await fetch("http://localhost:8000/api/podcasts");
      const data = await res.json();
      
      if (!res.ok) throw new Error(data.detail || "Failed to load notebooks");
      setPodcasts(data.podcasts);
    } catch (err) {
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  };

  // NEW: Delete Function
  const handleDelete = async (id) => {
    // Show a quick browser confirmation so you don't delete by accident
    const confirmDelete = window.confirm("Are you sure you want to delete this podcast permanently?");
    if (!confirmDelete) return;

    try {
      const res = await fetch(`http://localhost:8000/api/podcasts/${id}`, {
        method: "DELETE",
      });
      
      if (!res.ok) throw new Error("Failed to delete podcast.");
      
      // Instantly remove it from the screen without refreshing the page!
      setPodcasts(podcasts.filter(podcast => podcast.id !== id));
      
    } catch (err) {
      alert("Error: " + err.message);
    }
  };


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

  return (
    <main className="min-h-screen bg-[#121212] text-white p-6 pt-24 relative overflow-hidden">
      {/* Background Gradients */}
      {/* Background Gradients */}
      <div className="absolute inset-0 pointer-events-none flex justify-center z-0">
        {/* Main central wide glow behind the title */}
        <div className="absolute top-[10%] w-[120vw] h-[40vh] bg-[#1DB954]/15 blur-[160px] rounded-[100%]" />
        {/* Secondary soft glow behind the cards */}
        <div className="absolute top-[50%] w-[80vw] h-[50vh] bg-[#1DB954]/5 blur-[180px] rounded-[100%]" />
      </div>

      <div className="max-w-6xl mx-auto space-y-10 relative z-10">
        
        {/* Header */}
        <div className="flex flex-col md:flex-row justify-between items-center gap-4 border-b border-white/10 pb-8">
          <div>
            <h1 className="text-4xl font-extrabold tracking-tight text-white">
              My Audio Notebooks
            </h1>
            <p className="text-gray-400 mt-2">
              Your personal library of AI-generated podcasts and stories.
            </p>
          </div>
          <Link href="/" className="px-6 py-3 bg-[#1DB954] hover:bg-[#1ed760] text-black rounded-full shadow-xl shadow-[#1DB954]/20 hover:scale-105 transition-all">
            + Create New
          </Link>
        </div>

        {/* Content */}
        {isLoading ? (
          <div className="text-center py-20 text-gray-400 font-bold animate-pulse">Loading your library...</div>
        ) : error ? (
          <div className="text-center py-20 text-red-500 font-bold">Error: {error}</div>
        ) : podcasts.length === 0 ? (
          <div className="text-center py-20 bg-white dark:bg-gray-900/50 rounded-2xl border border-white/10">
            <span className="text-6xl block mb-4">📭</span>
            <h3 className="text-xl font-bold text-white">Your library is empty</h3>
            <p className="text-gray-400 mt-2">Go create your first audio notebook!</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {podcasts.map((podcast) => (
              <div key={podcast.id} className="bg-black/40 backdrop-blur-3xl border border-white/10 rounded-3xl p-6 shadow-2xl flex flex-col justify-between hover:border-[#1DB954]/50 transition-colors relative group">
                
                {/* THE NEW DELETE BUTTON */}
                <button 
                  onClick={() => handleDelete(podcast.id)}
                  className="absolute top-4 right-4 w-8 h-8 bg-red-500/20 hover:bg-red-600 text-red-500 hover:text-white rounded-full flex items-center justify-center transition-colors opacity-0 group-hover:opacity-100 focus:opacity-100"
                  title="Delete Podcast"
                >
                  ✕
                </button>

                <div>
                  <div className="flex justify-between items-start mb-4 pr-10">
                    <div className="w-12 h-12 bg-[#1DB954] rounded-full flex items-center justify-center shadow-lg shrink-0">
                      <span className="text-xl text-white font-bold">🎙️</span>
                    </div>
                    <span className="text-xs font-bold text-gray-400 bg-black/50 border border-white/5 px-3 py-1 rounded-full text-right">
                      {podcast.created_at}
                    </span>
                  </div>

                  <h3 className="text-xl font-bold text-white mb-2 line-clamp-1">
                    {podcast.title}
                  </h3>
                  
                  <div className="bg-[#282828] border border-white/5 rounded-xl p-3 mb-6">
                    <p className="text-sm text-gray-300 italic line-clamp-3 whitespace-pre-wrap">
                      "{podcast.transcript}"
                    </p>
                  </div>
                </div>

                
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
                      className={`px-4 py-2 rounded-full font-bold text-sm transition-colors border border-white/10 ${activeChatPodcastId === podcast.id ? "bg-[#1DB954] text-black shadow-lg border-[#1DB954]" : "bg-[#282828] text-white hover:bg-[#333]"}`}
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


              </div>
            ))}
          </div>
        )}
      </div>
    </main>
  );
}