import os

path = r"h:\projects2\murf ai\nextjs\app\(publicPages)\page.jsx"
with open(path, "r", encoding="utf-8") as f:
    code = f.read()

# Tabs container
code = code.replace(' gap-2 p-1.5 bg-[#282828] rounded-full mb-6 border border-white/5', ' gap-2 mb-6')

# Text Inputs
code = code.replace('bg-[#282828] border-none', 'bg-black/40 border border-white/10')

# Drag/Drop Areas
code = code.replace('bg-[#282828]/50 border-2', 'bg-black/20 border-2')
code = code.replace('hover:bg-[#282828]', 'hover:bg-black/40')

# Submit button disabled state
code = code.replace('"bg-[#282828] text-gray-500 cursor-not-allowed"', '"bg-black/40 border border-white/10 text-gray-500 cursor-not-allowed"')

with open(path, "w", encoding="utf-8") as f:
    f.write(code)

print("Solid grey backgrounds successfully removed!")
