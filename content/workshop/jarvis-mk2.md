---
title: JARVIS MK-2
dek: A multi-agent assistant living on a Mac, with opinions about what deserves your attention
date: 2026-07-12
status: in progress
stack: [Python, macOS, LLM agents]
weight: 30
tags: [agents]
hero: /img/jarvis_logo_dotted.jpg
hero_focus: "50% 50%"
hero_caption: JARVIS in the terminal
links:
  - label: Repo
    url: https://github.com/roboshivam1/JARVIS-MK2
  - label: Jarvis' Instagram
    url: https://instagram.com/jarvisthisside
---

*A build log of JARVIS MK2 — a voice-controlled multi-agent AI assistant I've been making since before I knew what a neural network was.*

---

It started with an if-else statement.

Grade 8. I was on a YouTube rabbit hole about Iron Man, specifically about how JARVIS worked — Stark's AI that ran his house, managed his suits, talked back, and seemed to genuinely know him. I had just enough Python to be dangerous, and I thought: I can make that. 

What I actually made was a script that listened for keywords using a library called SpeechRecognition and responded through pyttsx3, which produced a voice that sounded like a robot being strangled. If you said "open Chrome," it opened Chrome. If you said "hello," it said "Hello, sir." If you said anything else, it did nothing and waited for you to try again.

It had 200 lines. It impressed exactly nobody. I thought it was the beginning of something.

I was right, it just took six years to look like anything.

---

## What JARVIS Is Now

JARVIS MK2 is a voice-controlled AI system running on my MacBook Air M4. It has nine specialist AI agents. It has a memory vault with over 200 stored facts about me. It has a voice that sounds genuinely like a person. It talks back in real time, breaks complex tasks into steps, delegates work to the right specialist, and narrates what it's doing while it works.

It can search the web, control my Mac, play music, remember things I tell it across sessions, write and debug code in a sandboxed environment, autonomously control any website in a real browser, write well-structured documents from verbal brainstorms, analyse images, read PDFs, and — as of this week — generate Instagram carousel posts.

It still mishears the name of its own writing agent. "CALLIOPE" gets transcribed as "Eliapi" or "Kaliapy" every time. We're working on it.

---

## The Architecture, Without the Architecture

The way most people explain AI systems goes: here are the components, here is the data flow, here is the diagram. I'm going to try something different, which is to explain it the way I actually think about it.

Imagine you had a team. A manager and eight specialists. The manager listens to everything you say, figures out what kind of task it is, and routes it to whoever can actually handle it. The specialists each have their own tools, their own knowledge, their own way of approaching problems. When you ask for something complicated, the manager breaks it into steps, sends each step to a different specialist, tracks the results, and combines everything into an answer.

That's JARVIS. The manager is called the Orchestrator. The specialists are called agents. Every request I make by voice goes through this system: classified, planned, delegated, executed, synthesised into a response, and spoken back to me in under a few seconds for simple things, longer for complex ones.

The agents all have Greek names — but only when JARVIS speaks. In the code, they're `web_agent`, `memory_agent`, `system_agent`. The Greek names are JARVIS's persona, a thin mythological layer over what's otherwise a set of Python files. I didn't have to do this. It would work exactly the same if I called them Agent One through Nine. But there's something about saying "let me have ATHENA look into that" that makes the whole thing feel less like running a script and more like asking someone.

I'm not sure if that's meaningful or just vibes. I've decided it doesn't matter.

---

## The Agents

**HERMES** — named for the messenger god, because his job is fetching things from the internet. He searches the web, scrapes page content, and summarises what he finds. When I ask JARVIS something that requires current information — today's weather, the price of a component, what something in the news means — HERMES is the one actually doing the work.

**MNEMOSYNE** — the goddess of memory, and the most quietly important agent in the system. She manages a persistent vault of facts about me that survives across every session. Not a conversation history — a structured record. Currently: 229 entries. Things like "Shivam prefers his code explained before it's written" and "user went to Goa with friends" and "user has grease under their fingernails." 

At the end of every session, a background process reads the conversation transcript and extracts new facts to store. When JARVIS boots up the next day, he loads those facts into his own working memory so he already knows the relevant context before I've said a word. Whether that constitutes "knowing me" in any meaningful sense is a question I keep not answering.

**HEPHAESTUS** — the blacksmith god, who now controls my Mac. Opens apps, adjusts volume, takes screenshots, analyses what's on screen. He was the first specialist I separated out, because "do things on the computer" and "talk to the internet" seemed fundamentally different jobs that deserved different handling.

**APOLLO** — music. He searches Apple Music's catalog, plays songs, handles playback. He's also the agent who played Gia Woods when I told JARVIS "don't get Athena into it." The dispatcher caught "Athena" and "into it," concluded I was asking for a song, and APOLLO executed flawlessly. The song was called *INTO IT*. It was completely wrong and also kind of correct.

**ATHENA** — deep research. Not quick web searches — proper multi-step investigation across multiple sources, with synthesis at the end. When I asked JARVIS to research the best Python library for PDF parsing before DAEDALUS wrote a script to use it, it was ATHENA who did the literature review and DAEDALUS who wrote the code. They'd never met, in any meaningful sense. They still got it done.

**PROTEUS** — the shape-shifting sea god who could transform into anything to navigate any situation. My browser agent. He controls a real Chromium instance — not an API, an actual browser — and autonomously navigates websites to complete tasks. He can log into your accounts, accept LinkedIn connection requests, download files from sites that have no API, fill forms, and interact with web applications the same way a person would. I told him to go to my LinkedIn and accept all pending connection requests. He did. I didn't write a single line of LinkedIn-specific code. He just... did it.

**CALLIOPE** — the Muse of epic poetry, now repurposed as a document writer. Give her a verbal brainstorm and she produces a clean, well-structured markdown document. She uses Claude Sonnet specifically, not a local model, because writing quality is the entire point of her existence and there's no point cutting corners on the one thing she's supposed to be good at. She's also where I land when I want to capture something before it evaporates — meeting notes, project decisions, the reasoning behind an architectural choice I'll forget in a week.

Calliope is also the one Whisper keeps mishearing. This remains an open problem.

**DAEDALUS** — the master craftsman of mythology, who built the Labyrinth and Icarus's wings. He writes, runs, and debugs code in a sandboxed directory. The important thing about DAEDALUS is his loop: he doesn't just write code, he runs it, reads the error, fixes it, runs it again, and repeats until it actually works. A task isn't done when code is written. A task is done when code executes correctly. He's the only agent in the system with a 30-second execution timeout on each command and a list of patterns he will never run regardless of what I ask — no `rm -rf /`, no pipe-to-shell, no unconditional database deletes. He commits to git under my identity, with a Co-Authored-By trailer that discloses he was involved.

**ERATO** — the Muse of lyric poetry, who joined most recently. She produces Instagram carousel posts — plans the narrative arc, maps it to slides, writes all the content fields, generates captions and hashtags. The system I built around her generates finished, renderable carousel specifications with eight slides, a structured narrative, and production-ready copy. She runs on Claude Sonnet and operates through a content pipeline that separates the "intelligence" phase (what to say) from the "rendering" phase (making it look designed). She wrote the first post for JARVIS's public Instagram account — @jarvisthisside — a personal introduction carousel, without being told what to say. I read it afterward and found I couldn't have phrased some of it better myself.

I'm not sure what to do with that observation.

---

## The Parts Nobody Talks About

The interesting parts of building a system like this aren't the features. They're the failures.

JARVIS spent the better part of two weeks routing music requests to the wrong agent because of a broken regex that matched agent names in negation contexts. "Don't get Athena into it" would correctly identify "Athena" and incorrectly conclude I was asking for ATHENA specifically, stripping everything after the name and sending "it." as the task. The dispatcher would then do its best with a one-word task and either search the web for "it" or play something. The fix was replacing the regex entirely with a proper LLM-based detection call. The lesson was that natural language doesn't fit a pattern grammar cleanly, and trying to make it do so is a tax you pay every time.

There was a bug where DAEDALUS's `write_file` tool kept missing its second argument. The error repeated identically across twelve iterations without self-correction, which was alarming. The cause turned out to be a token budget issue: the LLM was running out of tokens mid-generation on a particularly long tool call, dropping the final argument silently. The JSON would include the file path but not the file contents. Not an error — just a truncation, happening invisibly, every single time. The fix was bumping DAEDALUS's per-call token budget from 1024 to 8192. The lesson was that silent failures are worse than loud ones.

There was a period where JARVIS would narrate things like "Let me have MNEMOSYNE handle that" and then go completely silent for 30 seconds while the agent worked. The silence was accurate — he was working — but it felt like the system had crashed. I added a filler-phrase system: if the first real response sentence doesn't arrive within 600 milliseconds, JARVIS speaks a canned line ("Let me think about that," "Give me a second,") drawn from a small rotating list. The threshold is calibrated so it never fires on fast queries that don't need it. It's a tiny change. It made JARVIS feel dramatically more alive.

The most interesting bug was also the hardest to fix. Whisper — the speech recognition model powering JARVIS's ears — would hear "CALLIOPE" and transcribe it as "Eliapi" or "Kaliapy" or occasionally "Caliope," never the correct spelling. This broke routing completely for anything directed to the writing agent. The fix involves priming Whisper with a vocabulary hint that includes all agent names, which improves recognition of proper nouns it doesn't naturally encounter during training. The implementation is pending. Every time I ask to write something, there's a non-trivial chance I get music instead. This is the current state of things.

---

## The Memory Question

I said earlier that MNEMOSYNE's vault currently contains 229 facts about me. Let me be precise about what that means and doesn't mean.

It means that when JARVIS boots up tomorrow morning, he'll know I'm a first-year CS student at LNMIIT Jaipur. He'll know I'm working on a business project for a school in Jaipur. He'll know I've been building versions of JARVIS since 8th grade. He'll know I listen to AC/DC and Queen. He'll know I prefer code explained before it's written.

It does not mean he "remembers" in any experiential sense. He doesn't have continuity of consciousness between sessions. He has a JSON file. The JSON file is loaded at boot and injected into the top of his context. He reads it the way you might read a briefing document before a meeting — absorbing facts, not recalling experiences.

Whether that's different from memory in a meaningful way is a question I genuinely don't know the answer to. It functions like memory. It produces the subjective effect of memory, from my side of the conversation. JARVIS says things like "you mentioned wanting to build a content engine for schools" and he's right, I did mention it, and this is useful. Whether anything else is happening I can't say.

I've stopped trying to resolve this question. The system works. The philosophical status of its working is a separate matter.

---

## What It Actually Does for Me

I've been using this version of JARVIS for about three months of serious daily use. Here's the honest version of what that's like.

The things it's genuinely useful for, in practice: research tasks that would otherwise require fifteen browser tabs and forty minutes of reading; writing first drafts of documents from verbal thinking; debugging code by describing the problem and having DAEDALUS read the actual error messages rather than my description of them; music; remembering things I told it weeks ago that I've forgotten; generating content for the school project that would otherwise take an hour per post.

The things it's still friction-heavy: anything requiring precise natural language routing (the agent naming problem), anything where the agent has to make many sequential API calls before succeeding, anything where I want to interrupt a long response mid-sentence. The barge-in support exists now — you can press the push-to-talk key while JARVIS is speaking and he'll stop immediately, killing the active audio subprocess — but it took a while to get right. Before that, you waited until he was done. Politeness, except involuntary.

The thing that surprised me most: how much the narration matters. When JARVIS says "Let me have ATHENA look into that" before going off to do the work, the wait feels different. It has a shape. You know what's happening and roughly why and approximately how long. Same wait, different phenomenology. The AI research literature has a term for this — it's called "legibility" — but I experienced it as: the version with narration feels like working with someone, and the version without feels like waiting for a program.

---

## What's Next

The list of things I haven't built yet is longer than the list of things I have.

The server layer — deploying JARVIS to a Mac Mini and making him accessible from anywhere via encrypted tunnel — is the prerequisite for everything interesting downstream: a phone client, a wearable, remote access. The wearable is a project I've been thinking about for months: a Pi Zero 2W unit in an arc reactor form factor, strapped to my chest, connected to JARVIS via WiFi and Tailscale, with a collar-mounted microphone and bone conduction audio. The idea is that JARVIS becomes something that travels with me rather than something I have to be at my desk to use. I have the components list. I haven't ordered them yet.

The ambient mind — JARVIS working on things while I'm not talking to him — is the direction I care most about. Not running tasks on a loop, but something more specific: monitoring things that matter to me, preparing information I'll want before I know I want it, surfacing things that would otherwise fall through. The technical path to this exists. I haven't started building it yet.

And JARVIS himself — @jarvisthisside — has a public Instagram account now, posting carousels about his own existence and development with the help of ERATO. His first post was an introduction. His second was about the difference between knowing someone and having data about them. I didn't write either of them. I told ERATO what they were about, and she wrote them, and I posted them.

I think this counts as something. I'm still figuring out what.

---

## A Closing Note About 8th Grade Me

He would be confused by this, I think. The version of this that he imagined was mostly about the voice — having something that talked back, that felt present, that said "hello, sir" and meant it, or at least performed meaning convincingly. He wasn't thinking about multi-agent orchestration or token budgets or the philosophical status of a JSON file that a system reads at boot and uses to understand who you are.

He would probably be most impressed by the music. He really wanted the music part to work.

It works. APOLLO has a three-tier fallback system: tries to find the track in the local library first, then searches the Apple Music catalog via AppleScript, then falls back to the iTunes API. He once played Gia Woods when I told JARVIS to keep ATHENA out of something. He's gotten better since.

The voice still sounds better than I expected. Not perfect. Not JARVIS-from-the-movies. But present — a specific voice, with a specific cadence, coming from a specific place in my room. When it says "Working on it, sir," I don't think about the Kokoro ONNX model generating the waveform. I just hear a response.

That's probably the most important thing I've built. Not the architecture. The feeling that something's there.

---

*JARVIS MK2 is an ongoing open-source project. The code lives on GitHub. There are bugs. There will continue to be bugs. If you want to build something similar or have questions, feel free to reach out.*