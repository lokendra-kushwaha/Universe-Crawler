import streamlit.components.v1 as components

def inject_voice_search():
    js_code = """
    <script>
    const parentDoc = window.parent.document;
    
    function addMicButton() {
        if (parentDoc.getElementById('custom-mic-btn')) {
            clearInterval(checkExist);
            return;
        }
        
        const searchInput = parentDoc.querySelector('input[aria-label="Search Your Indexed Universe"]');
        
        if (searchInput) {
            const micBtn = parentDoc.createElement('button');
            micBtn.id = 'custom-mic-btn';
            micBtn.innerHTML = '🎙️';
            
            micBtn.style.position = 'absolute';
            micBtn.style.right = '12px';
            micBtn.style.top = '50%';
            micBtn.style.transform = 'translateY(-50%)';
            micBtn.style.setProperty('background', 'transparent', 'important');
            micBtn.style.setProperty('border', 'none', 'important')
            micBtn.style.fontSize = '20px';
            micBtn.style.cursor = 'pointer';
            micBtn.style.zIndex = '9999';
            micBtn.title = 'Click to speak';
            
            searchInput.parentElement.style.position = 'relative';
            searchInput.parentElement.appendChild(micBtn);

            const SpeechRecognition = window.parent.SpeechRecognition || window.parent.webkitSpeechRecognition;
            
            if (SpeechRecognition) {
                const recognition = new SpeechRecognition();
                recognition.continuous = false;
                recognition.lang = 'en-US';

                micBtn.onclick = function() {
                    micBtn.innerHTML = '🔴'; // Recording state
                    recognition.start();
                };

                recognition.onresult = function(event) {
                    const transcript = event.results[0][0].transcript;
                    micBtn.innerHTML = '🎙️'; 
                    
                    let nativeInputValueSetter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, "value").set;
                    nativeInputValueSetter.call(searchInput, transcript);
                    
                    searchInput.dispatchEvent(new Event('input', { bubbles: true }));
                    
                    setTimeout(() => {
                        searchInput.dispatchEvent(new KeyboardEvent('keydown', {
                            key: 'Enter', 
                            keyCode: 13, 
                            code: 'Enter', 
                            bubbles: true
                        }));
                    }, 500); 
                };

                recognition.onerror = function(event) {
                    micBtn.innerHTML = '🎙️';
                };
            }
            clearInterval(checkExist); 
        }
    }
    
    const checkExist = setInterval(addMicButton, 500);
    </script>
    """
    
    components.html(js_code, height=0, width=0)