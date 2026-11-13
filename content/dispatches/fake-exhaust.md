---
title: The Bike Has No Engine. It Has an Exhaust Anyway.
dek: a 2 inch speaker, a tri-oval can and a lot of black paint
date: 2026-11-13
section: lab-notes
weight: 40
tags: [hardware, ebike, 3d printing]
about: ebike
hero: /img/lab_notes_images/fake_exhaust_dotted.png
hero_focus: "50% 50%"
hero_caption: painted, detailed and still pretending to have an engine
---

Okay so here's the thing about an electric bike. There is no exhaust. There is nothing to exhaust. The motor sits in the wheel and hums quietly to itself like it's embarrassed to be there.

I wanted an exhaust anyway.

The idea is simple enough: two fake 3D printed exhausts under the seat, each one hiding a speaker inside, with the can working as an acoustic chamber. Riding songs when I want them, fake engine sounds when I want those, and from the outside it just looks like a bike that has a pipe.

### Too big, then just right

The first plan had 4 inch car speakers and a proper amplifier board in it. Then I tried to imagine fitting a 4 inch speaker inside something that is supposed to look like an exhaust, and the plan quietly left the room. It was also costly for a first build. The sound quality of a cheap under-₹1k Bluetooth speaker is honestly enough for this, so I went small: 2 inch speakers and tiny MAX98357A amps. We can go bigger later if we want.

### Too plain, then not

The first 3D model was two round pipes side by side. Very cylindrical. Very plain. It looked like plumbing. So I found a photo of an Akrapovič can and said "this shape".

The new one has a tri-oval body, a slanted end cap, a perforated face plate and a teardrop shaped outlet. I modelled one single unit so I can print two and space them however the frame wants.

Printed it, and the speaker did not fit. (They usually don't, on the first try.) I cut about 3 cm off the canister and now it sits in there properly. Then black paint, silver detailing on top, and the paintwork is done.

### What's inside

The speaker has already had its first test tones through an ESP32 and one of those little amps. It sounds good, it just needs more volume, which the amp's gain pin will sort out later.

The fake engine itself is being built as a virtual engine, and I made a little web bench to try out profiles on it: a thumper, a V-twin, an inline-four, a two-stroke, and one trying very hard to be a Royal Enfield going dug dug at idle. The crackles on throttle off sounded bad, so they got removed.

Next up is getting that engine onto the ESP32, and then Bluetooth music.

More when there's more...
