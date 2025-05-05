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
![Banner](pic.png)


## 🛠️ Tech Stack

| Feature             | Technology                   |
|---------------------|-------------------------------|
| Game Engine          | Python + Pygame               |
| AI Content Generation| Generative AI (local/API-based) |
| Email Reports        | Python `smtplib`, `email`     |
| Platform             | Desktop (Cross-platform)      |

---

## 🚀 Getting Started

### Prerequisites

- Python 3.x
- Pygame
- Internet access for email functionality

### Installation

```bash
git clone https://github.com/yourusername/cognitive-horizons.git
cd cognitive-horizons
pip install -r requirements.txt
python main.py
