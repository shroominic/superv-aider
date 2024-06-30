GUIDELINES = """
Brand Guidelines: Colors, Fonts, and Language

Color Palette:

Primary: #007BFF (Blue)
Secondary: #6C757D (Gray)
Accent: #28A745 (Green)
Background: #F8F9FA (Light Gray)
Text: #333333 (Dark Gray)


Typography:

Headings: Montserrat, sans-serif
H1: 32px, Bold
H2: 24px, Semi-bold
H3: 20px, Semi-bold
Body: Open Sans, sans-serif
Regular: 16px
Small: 14px
Line height: 1.5


Language and Tone:

Clear and concise
Friendly but professional
"""

GENERATED_CODE = """
<button class="non-compliant-button">Click Me Now!</button>

.non-compliant-button {
    background-color: #FF00FF;
    color: #FFFF00;
    font-family: "Comic Sans MS", cursive;
    font-size: 24px;
    padding: 25px 50px;
    border: 5px dashed #00FFFF;
    border-radius: 0;
    text-transform: uppercase;
    box-shadow: 10px 10px 5px #888888;
    animation: wiggle 0.5s infinite;
}

@keyframes wiggle {
    0% { transform: rotate(0deg); }
    25% { transform: rotate(5deg); }
    75% { transform: rotate(-5deg); }
    100% { transform: rotate(0deg); }
}

.non-compliant-button:hover {
    background-color: #00FFFF;
    color: #FF00FF;
}
"""
