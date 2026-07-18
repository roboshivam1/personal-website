---
title: School Content Engine
dek: Teaching a machine how to make 'tasteful' school posters
date: 2026-07-12
status: shipped
stack: [Python, LLM agents, Jinja2]
weight: 30
tags: [Jinja2, LLM, Python]
hero: /img/school_content_dotted.png
hero_focus: "50% 50%"
hero_caption: A part of a carousel output
links:
  - label: Repo
    url: https://github.com/roboshivam1/School-Content-Engine
---

It started, like most of my projects do, with mild irritation.

I was scrolling through the Instagram page of a school here in Jaipur - I forget which one, they all look the same - and there it was. A photo of what I think was an annual day. Slightly blurry. Shot from the third row. Half a curtain in the frame. Uploaded, presumably, by a teacher who had forty other things to do that morning and correctly decided that cropping a photo was not going to be one of them.

And this is *everywhere*. Every school has an Instagram now, because parents look at it before admission season, and almost every school fills it with raw camera-roll dumps. Nobody has the time or the design chops to turn eighty photos of a sports day into something that looks like anyone cared. The photos exist. The care doesn't scale.

So I thought: what if I made the care scale.

## The plan, version zero

The pitch to myself was simple. You hand it a folder of raw event photos. Something reads them, figures out what happened, picks the good ones, arranges them into a proper branded carousel with captions, and hands back finished posts ready to upload. Photos in, content out, with the tedious middle part done by a machine instead of a tired human.

I already had JARVIS - my multi-agent system that does research and web tasks and pokes at my computer for me - so really this was just going to be one more agent bolted onto it. How hard could it be.

(You can hear the ominous music starting.)

## The Canva detour

My first instinct was Canva. They have an API. You design a template once, mark some slots as "fill this in later," and then pump data into those slots programmatically. Clean. Professional. Somebody else maintains the rendering.

I spent a happy afternoon reading their docs before the enthusiasm curdled. The API is gated behind an application process. There are rate limits. There's a whole dance of uploading assets, waiting for jobs, polling for exports. And the whole time a small voice was asking: *why am I renting a design tool to draw a rectangle with text on it?*

The thing I actually wanted was total control over how the posters looked, no dependency on anyone's approval queue, and templates I could version in git like real code. Canva gave me none of that.

Then it clicked. I already know a tool that's *phenomenal* at laying out rectangles with text on them, that every designer on earth already speaks, that costs nothing: a web browser.

## The trick that made everything work

Here's the whole idea, and it's almost embarrassingly simple.

I write the poster as an HTML page - same as any webpage, with CSS for the colours and fonts and layout. Then I open that page in an invisible browser, take a screenshot at exactly 1080×1080, and save it as an image. That's the poster.

That's it. That's the engine.

Everything a browser can do - gradients, fancy fonts, frosted-glass blur effects, precise layouts - my posters can now do, for free, with no third party anywhere near the critical path. And because the templates are just HTML files, I can loop over things, show a slide with three student photos or eight without making a new template, and tweak a design by editing a file instead of clicking around an app.

The moment the first screenshot popped out - a deep magenta card with a school's logo tucked in the corner and a headline in a serif font - felt genuinely good. It's a small thing. It's a picture of a rectangle. But it was *my* rectangle, and it came out of a script.

## Dumb parts, smart glue

The architecture I settled on has a nice shape to it, and I'm a little proud of the shape.

There are **dumb configs** - one file per school holding its colours, fonts, logo, hashtags, the tone it likes. There are **dumb templates** - the HTML, which knows nothing about any particular school. Neither of these thinks. They just sit there being data.

The intelligence lives in the middle. An AI reads the school's config and a folder of photos, and to it, a template looks like a form: *headline, date, student name, caption.* Its whole job is to fill in the form sensibly. It never touches the design; the designer (me) never touches the data (the AI). They meet in the middle and a poster falls out.

I split the actual work across three little workers, like an assembly line:

- The **vision worker** looks at the raw photos, throws out the blurry and the too-dark, and figures out what event this even was.
- The **content worker** decides what kind of post to make, writes the captions, and picks which photo goes on which slide.
- The **render worker** takes all that, stuffs it into the HTML, and screenshots the results at every size I need - square for the feed, tall for stories, tall-but-simpler for WhatsApp.

Photos in one end. Finished, captioned, branded posts out the other. When it worked end to end for the first time and spat out a five-slide carousel, I may have sat back in my chair like I'd personally invented photography.

## The part where it all went wrong (delightfully)

Of course it wasn't done. It's never done.

The first genuinely funny bug: the captions and the photos did not agree with each other. A slide showing kids at a photo booth would cheerfully announce that everyone was *splashing in the pool*. A slide of the actual pool would talk about *ice cream*. The machine was writing captions and handing out photos in two completely separate rooms, and nobody was checking that they matched. I had to sit them down and make them agree - the caption for a slide now has to point at the specific photo it's describing.

Then there was the time I fed it ninety-one photos of an event and it built a carousel out of, essentially, the worst ones. Turns out my "is this a good photo" test only measured whether the image was *sharp*, and a perfectly crisp photo of an empty chair beats a slightly soft photo of a child winning a race every single time by that measure. Sharpness is not the same as interestingness. Nobody tell my earlier self.

And burst shots. Oh, the burst shots. School photographers hold down the shutter, so you get the same moment eleven times in a row, and my carousel would proudly feature roughly the same photo across four slides. I ended up giving the system a sense of visual déjà vu - it now fingerprints each photo and quietly drops the near-duplicates, keeping only the best of each little burst.

Every one of these bugs was, in hindsight, me discovering that a task I do effortlessly with my eyeballs is secretly made of a dozen tiny judgments I never noticed I was making.

## Dressing it up

Once the plumbing was solid, I got to do the fun part: making it wear different outfits. A "design set" is just a folder of templates in a particular style - glassmorphism with its frosted glass, or a dark, gold-accented luxury look for a heritage school. A school picks its style in its config, or I override it per job, and the same photos and captions come out looking completely different. I have a running list of styles I want to build that is now longer than the amount of time I have to build them, which is exactly how these lists should be.

The other neat trick near the end: for chewing through ninety photos, I don't need to pay for a big cloud model to look at every single one. I can run a small vision model *on my own laptop*, for free, to do the first rough pass - "is this photo worth using, yes or no" - and only send the shortlist to the expensive smart model for final selection. Cheap labour does the sorting, the specialist does the judging. Feels like the right division of work.

## Where it is now

Right now it can take a folder of raw photos from a school event and hand back a properly designed, branded, captioned carousel in a couple of minutes, in whatever style you point it at, for Instagram and WhatsApp both. I've set it up with the branding of a couple of real schools to test it against, and watching it nail two completely different visual identities from the same code is the most satisfying part so far.

There's a whole list of things I still want - reels with music, a version that writes the WhatsApp parent-group message too, an actual agent sitting on top that notices an event happened and just *makes* the posts without me asking. It's nowhere near finished.

But it started with one blurry photo of an annual day and a small, ungenerous thought - *surely this can be better* - and it turned into a machine that quietly makes the care scale. That'll do for now.

I still think about that curtain in the frame, though. Somewhere out there, it's still half in every shot. I'm coming for it.