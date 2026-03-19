import sys

path = r'h:\projects2\murf ai\nextjs\app\(publicPages)\page.jsx'

with open(path, 'r', encoding='utf-8') as f:
    data = f.read()

# WaveformPlayer styling
data = data.replace('bg-blue-500', 'bg-[#1DB954]')
data = data.replace('hover:bg-blue-400', 'hover:bg-[#1ed760]')
data = data.replace('text-blue-500', 'text-[#1DB954]')
data = data.replace('border-gray-800', 'border-white/10')
data = data.replace('bg-[#161618]', 'bg-black/60 backdrop-blur-3xl border border-white/5')
data = data.replace('bg-gray-700', 'bg-white/10')
data = data.replace('hover:bg-gray-600', 'hover:bg-white/20')

# Main background orbs
data = data.replace('bg-blue-500/20', 'bg-[#1DB954]/20')
data = data.replace('bg-purple-500/20', 'bg-[#121212]/50')
data = data.replace('blur-[120px]', 'blur-[150px]')

# Layout styling
data = data.replace('bg-gray-50 dark:bg-[#0a0a0a]', 'bg-[#121212]')
data = data.replace('text-gray-900 dark:text-white', 'text-white')
data = data.replace('text-transparent bg-clip-text bg-gradient-to-r from-blue-600 to-purple-600', 'text-[#1DB954]')

# Cards & Container
data = data.replace('bg-white dark:bg-gray-900/50 backdrop-blur-xl border border-gray-200 dark:border-gray-800 p-6 rounded-2xl shadow-xl space-y-4 text-left', 'bg-black/40 backdrop-blur-3xl border border-white/10 p-8 rounded-3xl shadow-2xl space-y-6 text-left')
data = data.replace('bg-gray-50 dark:bg-gray-800/50 p-4 rounded-xl border border-gray-100 dark:border-gray-800', 'bg-white/5 p-4 rounded-2xl border border-white/5')
data = data.replace('bg-white/80 dark:bg-gray-900/80 backdrop-blur-xl border border-gray-200 dark:border-gray-800', 'bg-black/40 backdrop-blur-3xl border border-white/10')

# Selects & Inputs
data = data.replace('text-xs font-bold text-gray-500 uppercase tracking-wider', 'text-xs font-bold text-gray-400 uppercase tracking-wider')
data = data.replace('bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-700 rounded-lg px-3 py-2 text-sm text-gray-900 dark:text-white focus:ring-2 focus:ring-purple-500', 'bg-[#282828] border border-white/10 rounded-xl px-4 py-3 text-sm text-white focus:ring-2 focus:ring-[#1DB954] cursor-pointer hover:bg-[#333]')
data = data.replace('bg-gray-100 dark:bg-gray-800 border-none rounded-xl px-4 py-4 text-gray-900 dark:text-white focus:ring-2 focus:ring-purple-500', 'bg-[#282828] border border-white/10 rounded-2xl px-5 py-4 text-white focus:ring-2 focus:ring-[#1DB954] placeholder:text-gray-500 hover:bg-[#333]')

# Tabs Container
data = data.replace('flex gap-2 p-1 bg-gray-100 dark:bg-gray-800 rounded-xl mb-4', 'flex gap-2 p-1.5 bg-[#282828] rounded-full mb-6 border border-white/5')

# Tab buttons active / inactive 
data = data.replace('bg-white dark:bg-gray-700 shadow text-purple-600 dark:text-purple-400', 'bg-[#1DB954] shadow-lg text-black')
data = data.replace('text-gray-500 hover:text-gray-700 dark:hover:text-gray-300', 'text-gray-400 hover:text-white hover:scale-105')

# PDF Upload
data = data.replace('bg-gray-100 dark:bg-gray-800 border-2 border-dashed border-gray-300 dark:border-gray-600 rounded-xl', 'bg-[#282828]/50 border-2 border-dashed border-white/20 rounded-2xl hover:bg-[#282828] transition-colors cursor-pointer')
data = data.replace('bg-white dark:bg-gray-700 p-3 rounded-lg', 'bg-[#333] p-4 rounded-xl border border-white/10')
data = data.replace('text-purple-600 dark:text-purple-400 font-bold hover:underline', 'text-[#1DB954] text-lg font-bold hover:underline')

# Generate Button
data = data.replace('bg-gray-400 cursor-not-allowed', 'bg-[#282828] text-gray-500 cursor-not-allowed')
data = data.replace('bg-gradient-to-r from-blue-600 to-purple-600 hover:scale-105 shadow-lg shadow-purple-500/30', 'bg-[#1DB954] hover:bg-[#1ed760] text-black hover:scale-105 shadow-xl shadow-[#1DB954]/20')
data = data.replace('px-8 py-3 rounded-xl', 'px-10 py-4 rounded-full text-lg')

# Script Preview text
data = data.replace('text-gray-600 dark:text-gray-400', 'text-gray-300')

with open(path, 'w', encoding='utf-8') as f:
    f.write(data)

print("Replaced successfully")
