---
title: Teaching the Internet to Forget Me
dek: five agents, one chat and a worrying amount of coffee bites
date: 2026-10-30
section: lab-notes
weight: 40
hero: /img/lab_notes_images/fetchathon_dotted.jpg
hero_focus: "50% 50%"
hero_caption: team forgetters
tags: [hackathon, agents, coffee bites, forgetme]
---

Okay so last Saturday was Fetch-A-Thon 3.0, the Fetch.ai Innovation Lab's AI agent hackathon. One day, about seven hours of actual building, and a challenge that basically said: build an agent that does something, not just talks about it.

Madhura and I built **ForgetMe**. You give it your email inside ASI:One and it finds every data breach you've been part of, tells you which accounts actually matter, and then emails the companies a formal "please delete me" letter. Only after you say yes, obviously. It's five agents in a trench coat: one finds the breaches, one judges them, one writes the letters, one chases the companies that ignore you, and one talks to you and pretends the other four don't exist.

### Things that went wrong, in order

The breach database we planned on wanted a 52 dollar yearly subscription, at 10:30 in the morning. We found a free one by 10:33. Python 3.14 decided agents shouldn't be allowed to start at all. Then Stripe renamed two of its own settings on us mid-build, one after the other, like it knew. (I'd like it noted that every error message was extremely polite about it.)

### Things that worked

All of it, by the end. Little cards inside the chat with checkboxes, a privacy score out of 100, a warning label for crypto accounts, a receipt for every deletion request, and a paid tier running on Stripe test mode. The agents now live on my JARVIS server, in their own little room, with a strict rule against touching JARVIS's things.

The whole day was fuelled by Coffee Bites. Not coffee. Coffee Bites, the candy. Madhura and I went through an amount I am choosing not to count, on the grounds that the number would become evidence.

Result: [TK: how it went on the 28th]

Honestly the best part was the first test run, my own email coming back with breaches from accounts I didn't even remember making. Somewhere out there a website from my past still knows things about me. ForgetMe's coming for it.

More when there's more...
