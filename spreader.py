import streamlit as st
import re
import json

def process_text_for_spreader(raw_text):
    """
    Cleans markdown, calculates ORP, and adds punctuation delays.
    """
    clean_text = re.sub(r'\*\*|\*|__|_|#', '', raw_text)
    clean_text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', clean_text) 
    
    paragraphs = clean_text.split('\n\n')
    processed_words = []
    
    p_index = 0
    for para in paragraphs:
        if not para.strip(): continue
        
        words = para.split()
        for i, word in enumerate(words):
            length = len(word)
            if length <= 1: orp = 0
            elif length <= 3: orp = 1
            elif length <= 5: orp = 2
            elif length <= 9: orp = 3
            elif length <= 13: orp = 4
            else: orp = 5
            
            multiplier = 1.0
            if word.endswith((',', '-', ';')):
                multiplier = 1.5
            elif word.endswith(('.', '!', '?', ':')):
                multiplier = 2.0
                
            processed_words.append({
                "word": word,
                "orp": orp,
                "mult": multiplier,
                "p_index": p_index
            })
        p_index += 1
        
    return processed_words

def render_spreader_module(enhanced_text):
    """
    Renders the collapsible Spreader module with built-in controls.
    """
    with st.expander("🚀 Spreader: Speed Read Enhanced Text", expanded=False):
        if not enhanced_text or not enhanced_text.strip():
            st.warning("No enhanced text available to read yet. Generate text first.")
            return

        st.markdown("""
        **Controls:** * 🖱️ **Click inside** to focus. * ⌨️ **Spacebar**: Play/Pause/Restart. 
        * 🖱️ **Scroll**: Adjust Speed. * ⬅️ ➡️ **Arrows**: Jump Paragraphs.
        """)

        # Process the text
        words_data = process_text_for_spreader(enhanced_text)
        words_json = json.dumps(words_data)

        # We initialize default values directly into the HTML
        default_wpm = 400
        default_font = 52

        # Updated HTML/JS Payload - No Python string injections for the UI state
        html_code = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{
                    background-color: #0E1117; /* Streamlit dark mode color */
                    color: #FAFAFA;
                    font-family: 'Inter', sans-serif, monospace;
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    justify-content: space-between;
                    height: 95vh;
                    margin: 0;
                    overflow: hidden; 
                    user-select: none;
                }}
                /* Reader Area */
                #reader-container {{
                    display: flex;
                    font-weight: 600;
                    width: 100%;
                    justify-content: center;
                    flex-grow: 1;
                    align-items: center;
                    font-size: {default_font}px; 
                }}
                .left-part {{ width: 50%; text-align: right; }}
                .orp-letter {{ color: #ff4b4b; }}
                .right-part {{ width: 50%; text-align: left; }}
                
                /* Overlays */
                #focus-overlay {{
                    position: absolute; top: 0; left: 0; width: 100%; height: 100%;
                    background: rgba(14,17,23,0.9);
                    display: flex; align-items: center; justify-content: center;
                    font-size: 24px; cursor: pointer; z-index: 20;
                }}
                
                /* Bottom Control Panel */
                #control-panel {{
                    width: 90%;
                    padding-bottom: 20px;
                    display: flex;
                    flex-direction: column;
                    gap: 15px;
                    font-family: sans-serif;
                    z-index: 10;
                }}
                
                .sliders-row {{
                    display: flex; justify-content: space-between; gap: 20px;
                }}
                
                .control-group {{
                    display: flex; flex-direction: column; width: 100%;
                    font-size: 14px; color: #bbb;
                }}
                
                .control-group span {{ color: #fff; font-weight: bold; }}
                
                /* Custom Range Sliders */
                input[type=range] {{
                    -webkit-appearance: none; width: 100%; background: transparent; margin-top: 8px;
                }}
                input[type=range]::-webkit-slider-thumb {{
                    -webkit-appearance: none; height: 16px; width: 16px;
                    border-radius: 50%; background: #ff4b4b; cursor: pointer; margin-top: -6px;
                }}
                input[type=range]::-webkit-slider-runnable-track {{
                    width: 100%; height: 4px; cursor: pointer; background: #444; border-radius: 2px;
                }}
            </style>
        </head>
        <body>
            <div id="focus-overlay">Click to Focus and Start Reading</div>
            
            <div id="reader-container">
                <span id="word-left" class="left-part"></span>
                <span id="word-orp" class="orp-letter"></span>
                <span id="word-right" class="right-part"></span>
            </div>

            <div id="control-panel">
                <div class="control-group">
                    <label>Reading Progress: <span id="progress-text">0 / 0</span></label>
                    <input type="range" id="progress-slider" min="0" value="0">
                </div>
                <div class="sliders-row">
                    <div class="control-group">
                        <label>Speed (WPM): <span id="wpm-text">{default_wpm}</span></label>
                        <input type="range" id="wpm-slider" min="100" max="1000" step="10" value="{default_wpm}">
                    </div>
                    <div class="control-group">
                        <label>Font Size (px): <span id="font-text">{default_font}</span></label>
                        <input type="range" id="font-slider" min="20" max="120" step="2" value="{default_font}">
                    </div>
                </div>
            </div>

            <script>
                const words = {words_json};
                let currentIndex = 0;
                let wpm = {default_wpm};
                let isPlaying = false;
                let timeoutId = null;

                // DOM Elements
                const leftEl = document.getElementById('word-left');
                const orpEl = document.getElementById('word-orp');
                const rightEl = document.getElementById('word-right');
                const readerContainer = document.getElementById('reader-container');
                const overlay = document.getElementById('focus-overlay');
                
                const wpmSlider = document.getElementById('wpm-slider');
                const wpmText = document.getElementById('wpm-text');
                const fontSlider = document.getElementById('font-slider');
                const fontText = document.getElementById('font-text');
                const progressSlider = document.getElementById('progress-slider');
                const progressText = document.getElementById('progress-text');

                // Initialize Progress Slider Max
                progressSlider.max = Math.max(0, words.length - 1);

                function renderWord(index) {{
                    if (index >= words.length) index = words.length - 1;
                    if (index < 0) index = 0;
                    
                    const data = words[index];
                    const word = data.word;
                    const orp = data.orp;
                    
                    leftEl.innerText = word.substring(0, orp);
                    orpEl.innerText = word.charAt(orp);
                    rightEl.innerText = word.substring(orp + 1);
                    
                    // Sync UI
                    progressText.innerText = `${{index + 1}} / ${{words.length}}`;
                    progressSlider.value = index;
                }}

                function loop() {{
                    if (!isPlaying) return;
                    if (currentIndex >= words.length) {{
                        isPlaying = false;
                        renderWord(words.length - 1); 
                        overlay.innerText = "Finished. Press Spacebar to Restart.";
                        overlay.style.display = 'flex';
                        return;
                    }}
                    
                    renderWord(currentIndex);
                    
                    const currentData = words[currentIndex];
                    const baseDelay = 60000 / wpm;
                    const finalDelay = baseDelay * currentData.mult;
                    
                    currentIndex++;
                    timeoutId = setTimeout(loop, finalDelay);
                }}

                function togglePlay() {{
                    if (currentIndex >= words.length) {{
                        currentIndex = 0; 
                    }}
                    
                    isPlaying = !isPlaying;
                    if (isPlaying) {{
                        overlay.style.display = 'none';
                        loop();
                    }} else {{
                        clearTimeout(timeoutId);
                        overlay.innerText = "Paused (Click or Spacebar)";
                        overlay.style.display = 'flex';
                    }}
                }}

                // --- EVENT LISTENERS ---

                overlay.addEventListener('click', togglePlay);

                // WPM Slider Sync - Allows setting speed BEFORE playing
                wpmSlider.addEventListener('input', (e) => {{
                    wpm = parseInt(e.target.value);
                    wpmText.innerText = wpm;
                }});

                // Font Size Sync - Allows setting font BEFORE playing
                fontSlider.addEventListener('input', (e) => {{
                    const newSize = e.target.value;
                    fontText.innerText = newSize;
                    readerContainer.style.fontSize = `${{newSize}}px`;
                }});

                // Progress/Bookmark Slider
                progressSlider.addEventListener('input', (e) => {{
                    currentIndex = parseInt(e.target.value);
                    renderWord(currentIndex);
                    if (isPlaying) togglePlay(); // Auto-pause when scrubbing
                }});

                // Mouse Scroll for WPM (Updates the internal slider automatically)
                window.addEventListener('wheel', (e) => {{
                    e.preventDefault(); 
                    if (e.deltaY < 0) wpm += 10;
                    else wpm -= 10;
                    
                    if (wpm < 100) wpm = 100;
                    if (wpm > 1000) wpm = 1000;
                    
                    wpmSlider.value = wpm; 
                    wpmText.innerText = wpm;
                }}, {{ passive: false }});

                // Keyboard Controls
                window.addEventListener('keydown', (e) => {{
                    if (e.code === 'Space') {{
                        e.preventDefault(); 
                        togglePlay();
                    }}
                    else if (e.code === 'ArrowRight') {{
                        e.preventDefault();
                        if (currentIndex >= words.length - 1) return;
                        
                        let currentP = words[currentIndex].p_index;
                        while(currentIndex < words.length && words[currentIndex].p_index === currentP) {{
                            currentIndex++;
                        }}
                        if (currentIndex >= words.length) currentIndex = words.length - 1;
                        
                        if(!isPlaying) renderWord(currentIndex);
                    }}
                    else if (e.code === 'ArrowLeft') {{
                        e.preventDefault();
                        if (currentIndex >= words.length) currentIndex = words.length - 1; 
                        
                        let currentP = words[currentIndex].p_index;
                        while(currentIndex > 0 && words[currentIndex].p_index === currentP) {{
                            currentIndex--;
                        }}
                        let prevP = words[currentIndex].p_index;
                        while(currentIndex > 0 && words[currentIndex-1].p_index === prevP) {{
                            currentIndex--;
                        }}
                        
                        if(!isPlaying) renderWord(currentIndex);
                    }}
                }});

                // Initial render
                if(words.length > 0) renderWord(0);
            </script>
        </body>
        </html>
        """

        st.iframe.html(html_code, height=380)