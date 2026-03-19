import sys

path = r'h:\projects2\murf ai\nextjs\app\(publicPages)\notebooks\page.jsx'

with open(path, 'r', encoding='utf-8') as f:
    data = f.read()

# Layout
data = data.replace('min-h-screen bg-gray-50 dark:bg-[#0a0a0a]', 'min-h-screen bg-[#121212] text-white')
data = data.replace('bg-purple-500/10 blur-[120px]', 'bg-[#121212]/50 blur-[150px]')
data = data.replace('bg-blue-500/10 blur-[120px]', 'bg-[#1DB954]/20 blur-[150px]')

# Header
data = data.replace('border-gray-200 dark:border-gray-800', 'border-white/10')
data = data.replace('text-gray-900 dark:text-white', 'text-white')
data = data.replace('text-gray-500 dark:text-gray-400', 'text-gray-400')
data = data.replace('bg-gradient-to-r from-blue-600 to-purple-600 text-white font-bold rounded-xl shadow-lg hover:scale-105 transition-transform', 'bg-[#1DB954] hover:bg-[#1ed760] text-black rounded-full shadow-xl shadow-[#1DB954]/20 hover:scale-105 transition-all')

# Loading & Error text
data = data.replace('text-gray-500 font-bold animate-pulse', 'text-gray-400 font-bold animate-pulse')

# Empty State
data = data.replace('bg-white dark:bg-gray-900/50 rounded-2xl border border-gray-200 dark:border-gray-800', 'bg-white/5 backdrop-blur-2xl rounded-3xl border border-white/10')

# Podcast Cards
data = data.replace('bg-white dark:bg-gray-900/80 backdrop-blur-xl border border-gray-200 dark:border-gray-800 rounded-2xl p-6 shadow-xl flex flex-col justify-between hover:border-purple-500/50', 'bg-black/40 backdrop-blur-3xl border border-white/10 rounded-3xl p-6 shadow-2xl flex flex-col justify-between hover:border-[#1DB954]/50')
data = data.replace('bg-red-100 hover:bg-red-600 dark:bg-red-900/30 dark:hover:bg-red-600 text-red-600 hover:text-white dark:text-red-400', 'bg-red-500/20 hover:bg-red-600 text-red-500 hover:text-white')
data = data.replace('bg-gradient-to-tr from-purple-500 to-blue-500', 'bg-[#1DB954]')
data = data.replace('bg-gray-100 dark:bg-gray-800 px-3 py-1 rounded-full', 'bg-black/50 border border-white/5 px-3 py-1 rounded-full')
data = data.replace('bg-gray-50 dark:bg-gray-800/50 rounded-lg', 'bg-[#282828] border border-white/5 rounded-xl')
data = data.replace('text-gray-600 dark:text-gray-400', 'text-gray-300')
data = data.replace('text-gray-500 mt-2', 'text-gray-400 mt-2')

# Audio & Download
data = data.replace('bg-gray-100 dark:bg-gray-800 hover:bg-gray-200 dark:hover:bg-gray-700 text-gray-900 dark:text-white rounded-lg', 'bg-[#282828] hover:bg-[#333] border border-white/10 text-white rounded-full')

with open(path, 'w', encoding='utf-8') as f:
    f.write(data)

print("Notebooks page UI updated successfully")
