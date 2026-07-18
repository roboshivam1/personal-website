---
title: "ACE - Air Cleansing Entity"
dek: "How four fourteen-year-olds bolted a filter to a set of wheels, measured airflow with a garbage bag, and drove it to IIT Madras."
date: 2023-01-28
status: shipped
stack: ['Arduino', 'Hardware', 'MQ135']
weight: 30
tags: [arduino, air-quality, robotics, carpentry, competition]
hero: /img/final_rover_dotted.jpg
hero_focus: "50% 50%"
hero_caption: ACE - Air Cleansing Entity
links:
  - label: Build gallery
    url: https://aceairpurifier.netlify.app
---
Every air purifier I had ever seen just sat in a corner and sulked. You put it in one spot, it cleaned the air in a two-metre radius around itself, and the rest of the room was on its own. When our team got the problem statement for the Junior Make-A-Thon — *design a machine that can gauge and improve the air quality of a small room* — that was the first thing we latched onto. Not "how do we filter air better," but "why doesn't the thing *move*?"

That one question is basically the whole project. Everything else was us spending three weeks figuring out how to earn it.

There were four of us — Lokavya, Hridyansh, Bhomik, and me — and we were fourteen. We called ourselves the Imaginators, which felt very cool at the time, and we called the machine **ACE**: Air Cleansing Entity. A self-driving air purifier rover. Say it out loud a few times and it either sounds brilliant or insane, and honestly for most of the build we weren't sure which.

## Reading first, building second

Before any of us touched a wire, we went down a rabbit hole on why smoke is actually bad for you. It's not the smell — it's PM2.5, particulate matter about 2.5 microns across, small enough to get deep into your lungs and cause respiratory and cardiovascular disease. India was 5th on the global pollution rankings the year we looked it up; 21 of the 30 most polluted cities in the world were here. That number stopped feeling like a slide bullet and started feeling like the reason we were doing this.

The other useful thing that came out of the research was the filter plan. Proper HEPA filters are excellent and also expensive, and we were fourteen with a budget measured in pocket money. So we split the filtration into two ideas we *could* afford:

- **N-95 mask fabric**, for the fine particles. The meltblown fabric inside an N-95 mask catches particles down to around 0.1 micron — the same principle a HEPA filter runs on, just far cheaper. We layered it three deep: two meltblown sheets for the tiny stuff, a cotton layer in front for the big stuff.
- **Activated carbon granules**, for the gases and smells. Each gram has a surface area of over a thousand square metres hiding in microscopic pores, and it traps molecules by adsorption — they just stick to the surface. It's genuinely one of the coolest materials I've ever held in my hand, and it looks like gravel.

Sourcing the meltblown fabric was its first real lesson in *the thing you need is never sold in the quantity you want*. This was the part I didn't expect to enjoy and ended up loving — calling vendors, getting passed to a small factory, explaining that no, I did not want ten thousand masks, I wanted a few sheets of the fabric *from inside* the masks, and could they possibly sell me that. Some hung up. One didn't. That's how supply chains work when you're a kid, apparently: you just keep calling until someone finds you funny enough to help.

## Two machines pretending to be one

ACE was really two builds stacked on top of each other.

**The filtration unit** was the top half: the three-layer N-95 filters and the activated carbon filter, two beefy 12V DC axial fans (15×15×5 cm, 1.8 A each) to pull air in one side and push it out the other, an MQ135 gas sensor sniffing the air, and a little 16×2 LCD to display the reading. Air comes in dirty, crosses cotton → meltblown → carbon → meltblown, leaves cleaner. Simple to describe, fiddly to seal, because air is a coward and will always find the one gap you forgot to glue instead of going through the filter you spent a week making.

**The mobility unit** was the bottom half, and this is where the "learned to walk" part lives: an Arduino UNO with a motor shield, four DC motors driving four wheels, and an ultrasonic sensor mounted on a servo so it could sweep left and right, spot a wall coming, and turn before it drove into it. The dream was for ACE to wander a room on its own and clean air everywhere instead of one lucky corner.

Wiring the mobility unit is where I aged a year. Four motors, two battery packs, a servo, an ultrasonic sensor, all crammed into a wooden box, all of it needing to share grounds without shorting. I drew the circuit out by hand — I still have the notebook page, it looks like a spider fell in ink and panicked — and then soldered it, and then it didn't work, and then I found the one cold joint, and *then* it worked. Programming the obstacle-avoidance logic was the fun kind of frustrating: read the distance, if something's close, stop, look both ways, turn toward whichever side is more open, go. Watching it dodge a chair leg the first time genuinely felt like magic.

## The garbage bag experiment

At some point a judge was obviously going to ask "okay, but how much air does it actually clean?" and we realised we had no idea. We had built the whole thing on vibes and had never measured it.

So we improvised the most fourteen-year-old solution possible: we took a large polythene bag, held it over the purifier's outlet, and timed how long ACE took to inflate it completely. Then we treated the bag as a cylinder, measured its radius (≈34 cm) and height (≈67 cm), and did the maths.

```
Volume  = πr²h = 3.14 × 34 × 34 × 67 ≈ 243,322 cm³ ≈ 0.2433 m³
Time    ≈ 8 seconds to fill
Rate    = 0.2433 / 8 ≈ 0.0304 m³/s
        × 3600 ≈ 109.5 m³/hr
```

**≈110 cubic metres of air an hour**, measured with a garbage bag and a stopwatch. Is it a lab-grade number? Absolutely not. Did it hold up when a judge asked? It did, because we could show exactly how we got it and why the assumptions were reasonable. I've since learned that "here's my scrappy method and here's where it's shaky" beats "here's a precise number I can't defend" every single time.

## Wood, acrylic, and a logo painted at 1 a.m.

The whole thing needed a *body*, and none of it was going to come from a shop. We built the frame out of wood, cut and fitted an acrylic sheet for the top so you could see the filters, mounted the fans, and figured out — through trial, error, and a concerning amount of hot glue — how to hold three flimsy homemade filters upright in a moving vehicle without them flopping over.

Then we painted it black and put a big graffiti-style **ACE** logo on the side, because if you've built a self-driving air purifier you are legally required to make it look cool. That logo was not in the budget, the plan, or the presentation. It was the best decision we made.

## What it cost, and how it ended

Grand total: **₹10,725** — about ₹4,545 for the purification half and ₹6,180 for the mobility half. Under twelve thousand rupees for a mobile, sensing, self-navigating air purifier we built from mask fabric and gravel. I'm still a little proud of that line.

We took ACE to Shaastra at IIT Madras and came away **runner-up**. Standing there explaining the filter stack and the garbage-bag experiment to actual engineers, at fourteen, is a memory I still reach for when I need to remember why I build things.

## What I'd do differently

I'm not going to pretend ACE was flawless, because the fun of a build log is the honesty. Two real problems:

- **It got stuck.** The ultrasonic sensor avoided walls fine, but a bed frame or a couch leg could still trap it. Room-mapping — the kind you'd do now with a Raspberry Pi and a proper SLAM setup instead of one sweeping sensor — would fix most of it.
- **It needed babysitting.** Homemade filters clog, and a machine that drives around a household is a machine that will eventually drive off a step. Maintenance was real.

But those are the notes of someone who'd build it again, not someone who regrets it. ACE was the project where I first did *all* of it — the reading, the circuit, the code, the carpentry, the paint, the phone calls to factories, the standing-up-and-explaining. It's the reason the rest of the things on this site exist. Not bad for a purifier that decided to get up and walk.