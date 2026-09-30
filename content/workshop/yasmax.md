---
title: YASMAX
dek: A CPU simulator that only ran on Windows, rebuilt to run in a browser tab. Nobody gave me the source code, so I had to interrogate the original.
date: 2026-09-30
status: shipped
stack: [Python, Pyodide, WebAssembly, JavaScript, Web Workers, pytest, GitHub Actions]
weight: 20
tags: [Python, Pyodide, education, reverse-engineering]
hero: /img/yasmax_dotted.png
hero_focus: "50% 50%"
hero_caption: YASMAX - Yet Another Simple Machine Architecture eXplorer
links:
  - label: Try it
    url: https://roboshivam1.github.io/YASMAX/
  - label: Repo
    url: https://github.com/roboshivam1/YASMAX
  - label: Offline download
    url: https://github.com/roboshivam1/YASMAX/releases
---

*A tiny CPU, a lab full of laptops that couldn't run it, and one very long weekend of typing instructions into the original and writing down what it said back.*

---

Our Computer Organisation & Architecture lab runs on a program called **YASMIN**. It simulates a small, friendly CPU: a handful of registers, a stack, a memory view, and a little red arrow pointing at the instruction that's about to run. You type assembly, press STEP, and watch the machine think. It's a genuinely good teaching tool, written by Besim Mustafa at Edge Hill University.

It also only runs on Windows.

Which is a problem the moment you own a MacBook, or run Linux, or simply want to do the lab homework somewhere that isn't the lab. Half the fun of a lab is discovering which laptops are not invited to the lab.

So I did the reasonable thing. I rebuilt the CPU window as a webpage.

## The rules of the job

Three rules, decided early, because a project like this can quietly turn into something else if you let it.

- **CPU window only.** YASMIN has more windows than a Windows machine. I rebuilt the one students actually live in.
- **Educational, free, non-commercial, and loudly credited.** YASMAX is a fan-made recreation. It is not affiliated with YASMIN, it says so in the footer, and the licence says so too.
- **It should look like the old one.** The interface deliberately matches the 7.2.27 look (a very specific shade of 2007 grey) while behaving like the newer 7.5.50 release. Students should recognise it on sight.

## No source code, so: interrogation

Here's the catch. I don't have YASMIN's source. What I have is the program itself, a lab machine, and a lot of curiosity.

So the method was old-fashioned detective work. Type something into the real thing, screenshot what happens, write it down, then teach my version to do the same. Some of the answers were delightful:

- `CMP #1, #1` is not allowed. At least one operand has to be a register. The comparison lecture I thought I was going to write did not survive contact with the assembler.
- `CMP #0, R00` with R00 at zero leaves the status register at `1`. That one number told me which bit is the Zero flag.
- Divide by zero does nothing. No crash, no error box, no drama. The register just stays where it was, with the calm of someone who has never been told no.
- Stepping onto `HLT` doesn't move the highlight. The CPU stays on it and pops up a runtime message.
- RESET PROGRAM clears the program stack and drags the highlight back to the top instruction.

Every line of that list is a test in the repo now. If YASMIN changes its mind about something, I'd like to find out from a failing test rather than from an angry student.

## The shape of it

Three layers, each unaware of the layers above it.

```
your click
  └─ vanilla JS UI (no framework, absolute pixel layout)
      └─ Web Worker (so a runaway program can't freeze the page)
          └─ Pyodide: Python compiled to WebAssembly
              └─ the engine: fetch → decode → execute
                  └─ a JSON snapshot goes back up to the screen
```

The important design decision was that **the CPU is pure Python and knows nothing about browsers.** The engine is a normal Python package with 198 tests that run under plain `pytest` on my laptop. It gets loaded into Pyodide only at the very end. The UI just sends it one of 31 whitelisted commands and paints whatever snapshot comes back.

That's what made the project tractable. I could get the CPU correct in a terminal, where debugging is civilised, and only then worry about pixels.

The worker matters more than it sounds. Students will write infinite loops, because everyone does. In a normal page that freezes the tab. Here it only freezes the worker, and STOP still works.

## What the CPU actually does

The engine models the whole instruction cycle, not just "run this line". Fetch, decode and execute are separate phases, so STEP can show you each one, and the Execution Unit tab lights up while it happens.

There are 47 instructions and 8 addressing modes. Labels take zero bytes. `$Label` operands resolve to addresses, and in the instruction dialog the control-transfer instructions get a dropdown of your labels, because typing `$L0` by hand is how typos are born.

Two details I like:

- **The stack grows up.** It starts at 8096 and moves two bytes per entry. `MSF` pushes the previous frame and a return slot, `CAL` fills the slot in, `RET` unwinds the frame. Popping an empty stack reports "Stack overflow", which is technically the wrong word and exactly what the original says.
- **Data memory is tagged.** A string is stored as `03`, then the ASCII, then `00`. An integer is `02 00 lo hi`. The machine remembers what it wrote, so the data-memory window can show you a number or a string instead of a wall of hex.

Also: the red PC arrow and the highlighted row are the same thing. Click an instruction and the arrow jumps there, and RUN starts from that row. I originally built them as two separate ideas, which is the sort of thing you only get wrong once, because the person testing it is standing in front of the real one.

## The bugs worth telling you about

**The empty dialog.** The Instruction dialog, the single most important window in the whole program, opened completely blank. No instructions, dead tabs, three buttons that did nothing. Cause: my browser was serving last week's copy of one JavaScript file, which had never heard of the newest command. Fix: a fallback, a guard, a server that refuses to cache, and a permanent respect for the phrase "hard refresh".

**The stuck RUN.** I reported that RUN froze the program and disabled all my buttons. I had written `L0:` followed by `JMP $L0`. That is an infinite loop. It worked perfectly. STOP would have fixed it. I'd like it noted that the bug report and the bug were the same person.

## The guesses

Some things I couldn't find out, either because I couldn't reach the machine again, or because nothing online documented them. Those I guessed, and then did the only honest thing: wrote every guess down in a table in the README, where anyone can check it against the real thing.

A few of them:

- What `OUT` prints for its second operand (I currently print the number for `0` and the character for `1`).
- Which status-register bits are Negative and Overflow. Zero is confirmed, the others aren't.
- The exact HLT message text.
- The frame layout of `MSF` / `CAL` / `RET`.
- How many ticks a full cycle takes (I picked three).

A simulator that quietly invents behaviour and presents it as fact is worse than having no simulator. So YASMAX has a list of things it isn't sure about, and a bug-report form specifically for "this is different from YASMIN". Every mismatch a classmate reports turns a guess into a fact.

## Getting it onto other people's laptops

An educational tool that takes twenty minutes to install has already lost. So the goal was: nothing to install.

- **Just open the link.** It's a static site on GitHub Pages. Every push runs the tests, builds, and deploys, so a broken engine never reaches the website.
- **Install it as an app.** It's a proper PWA, so Chrome and Edge offer an Install button and Safari has "Add to Dock". After the first load it works fully offline. I tested that by killing the server and the Wi-Fi, then running `MOV #7, R00`.
- **Download it.** Each release ships an offline zip with start scripts for Mac, Linux and Windows.

It bundles its own copy of Pyodide, so it doesn't depend on a CDN being awake. When a new version is deployed the footer politely says so instead of silently changing under you mid-exam.

Reloading the page clears your program, exactly like closing YASMIN does. SAVE writes a `.sas` file, and LOAD reads one, which is how you move work between machines.

## What it isn't (yet)

- Only the CPU window. No cache/pipeline animation beyond the Execution Unit, and no SHOW... windows.
- The newer 7.5.50 opcodes (CVS, CVI, LNS and friends) aren't in.
- I've tested it in Chromium. Safari and Firefox should work, and I would like that sentence to become a fact.
- Some behaviours are still guesses. See above.

## Why I built it

The honest answer is the usual one: mild irritation, then a slightly larger idea than the irritation deserved. A tool exists, it's good, and a chunk of the people who need it can't run it. That felt fixable.

The less honest answer is that I wanted to see how faithfully a machine I could only poke from the outside could be reconstructed. It turns out: quite faithfully, if you're willing to be very boring about writing down what happens when you press buttons.

The footer says *Assembled with ♥ by Shivam Kapoor*. The CPU Help tab adds *(and a lot of MOV instructions)*. Both are accurate.

Credit where it's due: **YASMIN** is the work of Besim Mustafa. YASMAX exists because his tool is worth using, and it's the reason I bothered.