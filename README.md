# 🧠 Cognitive Horizons

**Cognitive Horizons** is a multi-game educational platform built using **Python (Pygame)**, designed to support individuals with cognitive challenges. It enhances **memory**, **critical thinking**, and **focus** through adaptive games powered by **Generative AI**, with automated performance reporting.

---

## 🎯 Project Goals

- Deliver accessible and engaging cognitive training through interactive games.
- Use AI to personalize content and track progress.
- Provide medical professionals with clear, timely updates via email.

---

## 🕹️ Included Games

1. **Quiz Game**  
   AI-generated critical thinking questions tailored for ages 50–60.

2. **Water Sort Puzzle**  
   A color-sorting challenge that strengthens logic and concentration.

3. **Card Matching Game**  
   Classic game to improve memory recall and short-term memory.

4. **Pattern Finder**  
   Logical visual puzzles that train cognitive sequencing.

5. **Word Builder**  
   Enhance vocabulary, spelling, and mental speed.

6. **Color Trails**  
   Visual memory game using sequenced color recall.

---

## 🧠 AI Integration

- **Content Creation**: AI dynamically generates questions, images, and word puzzles.
- **Difficulty Scaling**: Games adapt to user performance in real-time.
- **Report Generation**: Detailed performance summaries created post-session.

---

## 📤 Report Sharing

- After each session, an **AI-generated performance report** is:
  - Summarized clearly for medical or caregiving review.
  - **Automatically emailed to the concerned doctor** for tracking patient progress.
  - Includes metrics like accuracy, speed, improvement trends, and focus duration.

---
![Banner](images/pic.png)


## 🛠️ Tech Stack

| Feature             | Technology                   |
|---------------------|-------------------------------|
| Game Engine          | Python + Pygame               |
| AI Content Generation| Generative AI (local/API-based) |
| Email Reports        | Python `smtplib`, `email`     |
| Platform             | Desktop (Cross-platform)      |

---

## 🚀 Getting Started

Installation
Clone the repository:

First, clone the repository to your local machine:

bash
Copy
Edit
git clone https://github.com/stutisrijan/CognitiveHorizon.git
cd CognitiveHorizon
Install the dependencies:

Install all required libraries:

bash
Copy
Edit
pip install -r requirements.txt
Set up your environment variables:

For security, sensitive information like email credentials should not be hard-coded into the source code. To manage this:

Create a .env file in the root directory of the project.

Add the following keys to the .env file (you'll need to replace your_email and your_password with your actual email credentials or API keys):

text
Copy
Edit
EMAIL_USER=your_email@gmail.com
EMAIL_PASS=your_password_or_app_specific_password
Run the Project:

Finally, run the project with:

bash
Copy
Edit
python main.py
