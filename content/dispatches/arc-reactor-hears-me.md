---
title: The Arc Reactor Can Hear Me Now
dek: proof that Shivam Kapoor has a heart
date: 2026-11-06
section: lab-notes
hero: /img/lab_notes_images/arc-reactor-one_dotted.png
hero_focus: "50% 50%"
hero_caption: proof that Shivam Kapoor has a heart
weight: 40
tags: [jarvis, arc reactor, raspberry pi]
---

Okay so the arc reactor has been sitting on my desk for a while now. 3D printed shell, copper wound coils, looks exactly like the thing in the movie. Does absolutely nothing. It's the most convincing prop I own and that's kind of the problem, because it was never supposed to be a prop. It was supposed to be JARVIS, worn on my chest.

The plan was a Pi Zero 2 W. The Pi Zero 2 W, it turns out, is not available in India right now, at any price, from anyone. So I dug out an old Raspberry Pi 3 B+ I already had. Same family of chip, so if it works on this it'll work on the small one later. That's what I'm telling myself anyway.

### Bluetooth, the final boss

Getting my Boult earbuds to play sound from a Pi with no screen took longer than writing most of the actual code. First the Bluetooth wouldn't even turn on (it was blocked, by the Pi, for reasons). Then it refused to connect because the audio system only enables Bluetooth for someone "sitting at the computer", and logging in over SSH apparently doesn't count as sitting anywhere. Then it refused again because of a stale pairing. Three different errors, one pair of earbuds.

Then the first test: I made my Mac say a question out loud into a WAV file, copied it to the Pi, sent it to JARVIS, and his reply came back through the earbuds. It worked. The first word of every answer got eaten, but it worked.

### Hey JARVIS

Claude and I then wrote the actual client. Now the Pi listens for "hey jarvis" all the time, locally, and nothing leaves the device until it hears that. It chimes, I ask, I stop talking, it sends the question, JARVIS answers in my ear. Saying "hey jarvis" again while he's talking cuts him off, which is something I have wanted to do to a lot of people.

There are no LEDs yet (the first rings never worked, new ones are on the way), so for now it talks in chimes. Rising means listening, falling means sent, a low double means something broke.

The best part was the earbuds' own buttons. Play/pause starts a question, next switches the wake word on and off, previous shuts him up. So when I don't want to say "hey jarvis" out loud in a room full of people, I just tap my ear like a secret agent. A secret agent with call quality audio, because using the earbuds' mic forces them into phone call mode. That gets fixed when the proper mic shows up.

### What's next

The I2S mic and speaker arrive in a few days, which means proper sound quality, and songs straight off the 64 GB card. Then the LED rings, so it finally glows. Then maybe getting my e-ink watch to talk to it.

For now it's a Pi 3 on my desk, a pair of earbuds, and JARVIS answering when I call him. The reactor shell is still sitting right next to it, waiting for its electronics.

More when there's more...
