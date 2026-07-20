---
title: AI Dialogue Reel Generator
dek: Paheli and Boojho from NCERT are now genz and explaining FastAPI for some reason.
date: 2025-06-03
status: shipped
stack: [Python, LLM Pipelines, AssemblyAI, Gemini API]
weight: 20
tags: [Python, LLM Pipelines]
hero: /img/pbpfp_dotted.jpg
hero_focus: "50% 50%"
hero_caption: The main characters.
links:
  - label: Repo
    url: https://github.com/roboshivam1/AI-Dialogue-Reel-Generator
  - label: Try some videos here
    url: https://www.instagram.com/paheliboojhopython/
---

# Paheli & Boojho Were Never Supposed to Become YouTubers

There are two kinds of project ideas.

The first kind arrives after careful market research, competitor analysis, and a beautifully color-coded Notion document.

The second kind arrives at 2 AM while staring at the ceiling thinking,

> "Wait... what if Paheli and Boojho from NCERT books became Gen-Z software engineers?"

This project belongs firmly in the second category.

Like most Indian kids, I grew up seeing these two tiny characters randomly interrupt science chapters. Every time the textbook got slightly interesting, Paheli would ask a question everyone secretly had, Boojho would confidently say something questionable, and somehow you'd end up learning something.

Years later, my brain looked at those memories and somehow concluded:

*"Let's make them explain APIs."*

---

# It Started With a Very Boring Pipeline

Before this project, I already had a working pipeline for generating educational videos.

It could generate a script using Gemini, generate narration, create supporting images, stitch everything together, add captions, and export a finished reel.

Technically, it worked.

Creatively...

It had the personality of an instruction manual.

It looked exactly like every other AI-generated educational reel on Instagram. Floating text. Generic voice. Stock visuals. Useful? Sure. Memorable? Not even slightly.

I wanted something that felt like two actual people talking instead of an AI reading a Wikipedia article.

---

# The NCERT Glow-Up

Paheli and Boojho felt like the perfect candidates.

The challenge was that they still looked like they had walked straight out of a 2008 textbook.

I didn't want to redesign them completely. The goal wasn't to replace them—it was to modernize them just enough that someone scrolling Instagram would immediately think,

> "WAIT... is that Boojho?"

while also wondering,

> "Why is he wearing a hoodie?"

So they got oversized hoodies, sneakers, expressive faces, cleaner illustrations and a healthy dose of Gen-Z energy.

They somehow looked exactly the same...

...and completely different.

---

# The First Problem

Making them talk sounded easy.

My first thought was simple:

Generate Paheli's voice.

Generate Boojho's voice.

Merge them.

Done.

Except...

The voices weren't perfectly consistent between generations.

Sometimes Paheli sounded slightly different halfway through the script.

Sometimes Boojho randomly decided to become a different person.

Sometimes the pauses felt unnatural.

Sometimes everything sounded slightly... stitched together.

Then Gemini released multi-speaker speech generation.

Problem solved.

One API call.

One audio file.

Two consistent speakers.

Natural conversations.

It genuinely felt like cheating.

---

# Then Came The "Wait..."

Having one audio file introduced another problem.

How does the computer know who's talking?

I had two characters.

One audio track.

Zero clues.

For a while I disappeared into the rabbit hole of speaker diarization.

Pyannote.

WhisperX.

Random GitHub repositories written by people much smarter than me.

At one point my browser history looked like I was trying to earn a PhD in identifying voices.

Eventually I landed on AssemblyAI.

Instead of giving me a mysterious black-box output, it simply said:

```text
Speaker A
Start: 3.2s
End: 7.8s

Speaker B
Start: 7.8s
End: 11.6s
```

Exactly what I needed.

Now I knew precisely when Paheli should appear and when Boojho should steal the screen.

---

# Static Faces Are Weird

Once I got the overlays working, I rendered a test video.

It looked...

terrifying.

Imagine having a conversation with someone whose facial expression never changes.

Ever.

No blinking.

No smiling.

No confusion.

Just the exact same PNG staring into your soul for an entire minute.

That wasn't going to work.

So I generated multiple expressions for both characters.

- Thinking
- Explaining
- Laughing
- Confused
- Smirking
- Questioning
- Surprised

Then every dialogue line goes through Gemini one more time—not to explain science, but to answer one very important question:

> "Which expression matches this sentence?"

That tiny change made an absurd difference.

Now Boojho actually looks confused when he's confused.

Paheli smirks when she's roasting him.

The videos suddenly felt alive.

---

# The Pipeline Quietly Became Ridiculous

At some point I stopped and realised what I'd accidentally built.

The pipeline had become something like this:

- Generate topic
- Gemini writes the dialogue
- Gemini generates dual-speaker narration
- AssemblyAI identifies who is speaking
- Gemini chooses facial expressions
- Gemini generates supporting visuals
- MoviePy stitches together overlays, expressions and narration
- ZapCap adds captions
- Finished Instagram Reel appears

Looking at it written down makes it sound unnecessarily complicated.

It probably is.

But it works.

---

# MoviePy Tried To Destroy My Spirit

There was one evening where I rendered a video.

MoviePy looked at my computer...

...looked back at me...

...and estimated **32 hours remaining.**

Thirty-two.

Hours.

Apparently transparent PNG overlays, alpha compositing and hundreds of tiny clips are not exactly MoviePy's favourite hobby.

A significant amount of optimization later, I managed to bring render times back down to something that didn't require emotional support.

Progress.

---

# The Funniest Part Wasn't The Code

It was writing the personalities.

I spent an unreasonable amount of time debating whether Boojho should say:

> "Bro..."

or

> "Bruh..."

These are apparently the important engineering decisions.

Eventually they became their own characters.

Paheli is quick, sarcastic and somehow always knows the answer.

Boojho asks exactly the question everyone watching is secretly thinking.

He's curious.

Slightly dramatic.

Occasionally dumb.

But never so dumb that you stop rooting for him.

The chemistry ended up being far more important than the technology.

---

# The Unexpected Result

This stopped feeling like an AI video generator surprisingly quickly.

It started feeling like a tiny animation studio.

Today I can feed it almost any programming concept—

- Cookiecutter
- Caching
- API Throttling
- Docker
- Git
- Webhooks
- Rate Limiting

—and within a few minutes it writes the script, generates expressive conversations, creates visuals, syncs character expressions, renders everything together and exports a finished vertical video.

Watching the first fully automated reel come together felt strangely magical.

Mostly because I knew how many tiny pieces had to cooperate for that one minute of video to exist.

---

# Where This Goes Next

Like most side projects, this one immediately gave me five more bad ideas.

What if Tom and Jerry explained operating systems?

What if Sherlock Holmes taught machine learning?

What if Motu and Patlu discussed Kubernetes?

What if two aliens explained human technology?

These are objectively ridiculous questions.

Which probably means one of them will become my next project.

Because that's usually how my favourite things begin.

Not with a product roadmap.

Not with market research.

Just with one stupid thought that refuses to leave me alone.

This one started because I wondered what would happen if two forgotten NCERT characters started explaining software engineering.

Somehow...

it worked.