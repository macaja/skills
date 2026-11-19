---
name: explain-me
description: Explains a concept, a system, a piece of code, a document or a previous answer so it is easy to understand, climbing a fixed ladder of formats - writing that is about 80% of the way to ASD-STE100 Simplified Technical English, then a diagram, then an interactive web page on claude.ai, and last an explainer video. Use it whenever the user says "explain me", "explícame", "explain it like an aircraft manual", "in STE", "ASD-STE100", "I don't get it", "say it simpler", says an answer was hard to read, or asks for an explanation as a diagram, a web page or a video.
---

# Explain me

As models do more of the work, more of our time goes to understanding what they produce. This skill makes that easier with a ladder of output formats, from plain to rich. Each rung is easier to take in than the one before it, and also costs more to make.

`assets/reference.svg` is a one-page visual summary of this skill: the ladder, the rules to keep and relax, the limits, the verb forms, common words and two before-and-after examples. `references/ste-rules.md` has the full, strict ASD-STE100 sheet as text.

## The ladder

The order is always the same:

1. **Text**: writing at about 80% of ASD-STE100.
2. **Diagram**: when text alone is not enough.
3. **Interactive web page**: published on claude.ai.
4. **Video**: last, only when the user asks for it.

| Rung | Use it when | How |
|---|---|---|
| 1. Text | Default. Any explanation. | About 80% of ASD-STE100, see below. |
| 2. Diagram | The subject has parts that connect: a flow, a sequence, a hierarchy, a request going through layers, a before and after. | In a terminal, draw it with box-drawing characters inside a code block. Do not use Mermaid in chat, because the terminal does not render it. |
| 3. Interactive web page | The user asks for "HTML" or a "page", the subject is better understood by interacting with it (step through a process, toggle a setting, move a slider), or it does not fit on one screen. | Publish it on claude.ai with the Artifact tool, and follow that tool's own instructions. If the Artifact tool is not available, write one self-contained `.html` file and open it. |
| 4. Video | Only when the user asks for a video. | See "Explainer videos" below. |

Start at the rung the user asks for. When they do not name one, start with text, and add a small diagram when the subject has structure. Finish with one line that offers the next rung up, for example "Do you want this as an interactive page on claude.ai?". Do not climb on your own past the diagram, because the page and the video take time the user did not ask for.

The thing to explain is often your own previous answer, a file, or output from a tool. Explain what is there. Do not add new claims to make the explanation look complete.

## Text: about 80% of ASD-STE100

ASD-STE100 is a controlled language for aircraft maintenance manuals. It has writing rules and a dictionary of about 900 approved words, each with one meaning. Models know it well, and its limits force a clean style. The full spec is very strict, so aim for about 80% of it. In practice that means: keep the structure rules, and relax the dictionary.

**Keep these rules:**

- Write one topic in each paragraph, with a maximum of 6 sentences.
- Keep sentences short: a maximum of 20 words for instructions and steps, 25 words for descriptions.
- Put one instruction in each sentence.
- Use the active voice. Use the imperative for steps ("Run the migration.").
- Use simple tenses: present, past, future. Avoid the progressive ("is running") and the perfect ("has run") when a simple tense says the same thing.
- Use one word for one thing. When you call it "the session token" once, do not call it "the auth token" later.
- Prefer the common word to the formal one: "start", not "commence"; "use", not "utilize"; "make sure", not "ensure"; "before", not "prior to"; "about", not "approximately"; "to", not "in order to".
- Keep noun clusters to 3 words or fewer. Break up "user session token refresh handler" into "the handler that refreshes the session token of the user".
- Do not drop "the", "a" or "this". Short is good, telegraphic is not.
- Use a vertical list when there is a sequence or more than three items.
- For a warning, give the command first and then the risk: "Do not run this on production. It deletes all rows."

**Relax this:** a technical word outside the approved dictionary is fine when no simple word says the same thing. Code names, commands, product names and error messages stay exactly as they are; in STE terms they are technical names.

Use the strict, full spec only when the user asks for "strict" or "full" ASD-STE100. Then read `references/ste-rules.md` for the complete sheet.

**Why not always strict:** with a very small vocabulary, specific facts fall out of the text. After you write, check that every fact from the source is still in your explanation: names, numbers, conditions, exceptions.

### Example

The example from the reference sheet:

> Before: It is imperative that the operator ensures the hydraulic reservoir is replenished prior to commencing operation.
>
> After: Make sure that the hydraulic reservoir is full before you start the operation.

The same idea for code:

> Before: The middleware is responsible for ensuring that requests which have not been authenticated are being rejected prior to reaching the handler, utilizing the session token validation mechanism.
>
> After: The middleware rejects requests that are not authenticated. It does this before the request gets to the handler. To decide, it validates the session token.

## Other languages

STE is an English standard, and its dictionary only covers English. When the user writes in another language, answer in that language and apply the structure rules: short sentences, active voice, one idea per sentence, one word for one thing, and the common word over the formal one. In Spanish, for example: "usar", not "utilizar"; "antes de", not "con anterioridad a"; "empezar", not "dar comienzo a"; "asegurate de", not "es imperativo garantizar".

## Explainer videos

The style to aim for is a 3Blue1Brown video: animations made with the Python library Manim, with a narrated voice.

1. Check what is installed before you write anything: `manim`, `ffmpeg`, and an `ELEVENLABS_API_KEY` environment variable for the narration. Tell the user what is missing and ask before you install it.
2. When there is no ElevenLabs key, offer a free voice that runs on the machine, for example macOS `say` or Piper.
3. Write the script first, in the STE style above, and show it to the user. A script change is cheap; a render is not.
4. Make one Manim scene for each idea, render each scene with its narration, and join them with `ffmpeg`.

## Check before you send

- Every fact from the source is still there.
- No sentence has more than 25 words, or 20 for a step.
- The same thing has the same name from start to end.
- The answer ends with a one-line offer of the next rung up.
