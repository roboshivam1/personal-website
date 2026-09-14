---
title: SLATE
dek: Study tools mark your answer wrong. SLATE wants to know why you were so confidently wrong in the first place.
date: 2026-09-13
status: shipped
stack: [Python, FastAPI, Jinja2, HTMX, SQLite, Pydantic, Anthropic Claude, Gemini TTS, Manim]
weight: 20
tags: [hackathon, LLM, edtech, Python]
hero: /img/slate_dotted.png
hero_focus: "50% 50%"
hero_caption: SLATE - Structured Learning & Adaptive Teaching Engine
links:
  - label: Repo
    url: https://github.com/roboshivam1/SLATE
---

*36 hours (on paper, about 20 really), to build a study tool that argues with your misconceptions instead of just marking them wrong.*

---

It started with a 106-page PDF and the specific dread of reading a hackathon problem statement booklet at midnight, hunting for the one theme that wouldn't make us just another NotebookLM knockoff with a different colour scheme.

Fintech, Supply Chain, Cybersecurity, Healthcare, Blockchain, Sustainability, Agritech, Disaster Management - Team **Null Pointers** (TEAM161, if you're keeping score) scrolled past all of them and stopped on Edtech PS #7: *AI Native Learning Workspace for Any Study Material.* Which sounds thrilling until you realise "chat with your PDF" has been built roughly four thousand times, most recently by Google, who has slightly more engineers than we did.

So the actual hackathon wasn't "build a study bot." It was "find the one thing every study bot forgets to do, and build that instead."

## The thing every study bot forgets to do

Here's the thing they all forget: correcting an answer doesn't correct a belief.

You get a question wrong, the tool shows you the right answer, everyone moves on feeling productive. Except the wrong idea that produced the wrong answer is still fully intact in your head, patiently waiting to cause the exact same mistake again next week - Groundhog Day, minus the character development, minus Bill Murray, plus a pop quiz.

SLATE's entire personality is built around refusing to let that happen. Its unit of state isn't the document you uploaded - it's *you*, specifically which wrong idea you're currently carrying about which concept, tracked and updated every time you open your mouth (well, keyboard) about it. Wiping the actual slate clean, not just the whiteboard. I didn't pick the name for the pun. The pun found me and I let it stay. oh sounds too poetic, actually its just that the name was good and also it was relating with my old project - CHALKDUST which was reused in SLATE. Oh you dont know what CHALKDUST is? haha. bwah. lol. Its just a manim video generator in python that I built some while ago. go smash that star button on Github SMASHERS. (dani reference... DaniDev not daniels.)(tf am i doing with my website man, i really hope a recruiter doesnt come accross this.)

## Thirty-six hours, no safety net

HackX gave us one sprint, not a warm-up round - 36 hours to build it, pitch it, and have a genuinely live, working product to show, demoed off my own laptop, no VPS quietly holding things together in the background if the auditorium WiFi decided to have main character energy.

This was not Tony Stark building a suit in a cave with a box of scraps. This was building a diagnosis engine in a lecture hall with a power bank, and the growing suspicion that the cave, at least, didn't have two hundred other teams' laptops fighting it for the same router.

My teammates took the frontend - shoutout to Tanmay and Kunal for a fire design language and an even more crazier landing page. I took the backend and the part of the system that had to actually be correct under judges' eyes, which meant most of those 36 hours went into making sure the diagnosis engine wouldn't do anything embarrassing live on stage.

## The loop

Every concept in every document you upload goes through the same pipeline:

```
upload a PDF
  └─ concepts extracted, each with a closed set of likely misconceptions
      └─ you explain the concept in your own words
          └─ the misconception is named, quoting your own sentence as evidence
              └─ targeted remediation for that exact belief
                  └─ a retest aimed at the same gap
                      └─ mastery state updates
```

Two stages ride this loop. **LEARN** writes your notes, your audio briefings, your animated video briefings, and gets lazier or more thorough depending on what you've already proven you know. **DIAGNOSE** is the misconception hunt itself, and whatever DIAGNOSE finds is what LEARN writes about next. Not two features shipped side by side - one is downstream of the other, like a sequel that actually bothered reading the first movie's script.

## Rules I made the model follow (it did not enjoy this)

The dangerous thing about asking an LLM to diagnose your misconceptions is that it's extremely good at confidently inventing one you don't actually have. Left alone, it will tell you you're wrong for a reason it made up, with the calm authority of a horoscope. So the whole backend runs on one rule: **the model is allowed to reason and narrate. It is not allowed to decide or compute anything that matters.**

A few of the leashes I put on it, assembled at hackathon speed and somehow still holding:

- The list of possible misconceptions per concept gets frozen the moment the document is ingested, and locked into a Pydantic `Literal` - basically a nightclub bouncer with the guest list memorised, who will not be talked into anything no matter how confidently you argue your case at the door. The model can be wrong about *which* misconception you have. It cannot invent a new one and sweet-talk its way past the rope.
- Every diagnosis has to quote your own words back at you as evidence - Law & Order rules: no citation, no conviction. Code checks the quote actually exists in what you wrote. If it doesn't, confidence drops and the citation vanishes. Below 0.6, the UI downgrades from a verdict to a shrug - it says *possible*, not *you clearly believe*, which is about as close as a hackathon project gets to reasonable doubt.
- Remediation is never allowed to just give up. It falls down a ladder - animated video, then a generated illustration, then plain text - Batman's utility belt logic: if the first gadget doesn't fire, there's already a backup clipped on.
- Any SVG the model generates gets run through a whitelist validator - approved tags, approved attributes, approved colours - with one chance to fix itself before it's demoted to text. Broken markup never makes it to your screen. No rogue rectangles.

None of this is glamorous. All of it is the actual reason the demo didn't fall over.

## Where CHALKDUST sneaks back in

Buried in the file tree is a folder called `chalkdust/` - the "vendored animation renderer." That's not a licensed library. That's my *other* project, the educational-video generator I built with Manim, smuggled into SLATE's backend as a dependency, because I already had a tool that turns "explain this concept" into an animated video, and building a second one from scratch with the hackathon clock running felt like a personal attack on myself. So SLATE's video briefings are, quietly, CHALKDUST in a trench coat and a fake moustache, pretending to be a new hire. The crossover episode nobody commissioned, delivered anyway, on schedule, to an audience of judges who had no idea it was one.

## The ending, honestly

SLATE survived to the final demo, ran live off my laptop exactly as planned, and didn't place. Rocky didn't win his first fight either, and that one had a training montage and Sylvester Stallone's cheekbones working in its favour. We had a Pydantic schema and a very tired teammate.

What's staying with me regardless: the LEARN/DIAGNOSE split, the "quote yourself or it doesn't count" evidence rule, and the fallback ladder are all things I'd build exactly the same way again with no hackathon clock breathing down my neck. What I'd actually redo is the workspace itself - right now it's very good at telling you what's wrong with your thinking, and not nearly enough fun to sit inside while it does that.

Still the closest thing I've built to a tool that argues with *why* you're wrong instead of just marking the box red. Which, given the name, is either extremely on-brand or a pun I should have seen coming from further away.