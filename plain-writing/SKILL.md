---
name: plain-writing
description: Writes or rewrites any text in plain, direct language, following about 80% of ASD-STE100 Simplified Technical English. It works on documents, READMEs, specs, pull request descriptions and messages. It keeps every fact from the source, adds none, and draws a small box diagram only when words cannot carry a structure. Use it whenever the user asks to write something plainly, to rewrite or simplify a text or a file, says "escribilo simple", "reescribí esto", "lenguaje directo", "plain English" or "make this readable", or says a text is hard to read. To explain a concept or code to the user in chat, use explain-me.
---

# Plain writing

This skill writes text that a reader understands on the first read. It uses the same rules as the explain-me skill: about 80% of ASD-STE100, a controlled language for aircraft maintenance manuals.

The length of the result does not matter. It can be shorter or longer than the source. What matters is this: every fact from the source is in the result, and no new fact is.

## Two modes

| Mode | Use it when | The facts come from |
|---|---|---|
| Rewrite | The user gives you a text or a file to make plain. | That text, and only that text. |
| Write | The user asks for a new document. | What the user said, this conversation, and the files or code they point to. |

In write mode, a fact you need is sometimes not in the source. Then ask for it, or leave a visible gap such as `TODO: who approves this?`. Do not fill the gap with a guess.

## The steps

```text
┌──────────────┐    ┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│ 1. List the  │───►│ 2. Write     │───►│ 3. Check     │───►│ 4. Change    │
│    facts     │    │              │    │              │    │    note      │
└──────────────┘    └──────────────┘    └──────┬───────┘    └──────────────┘
                           ▲                   │ a fact is missing or new
                           └───────────────────┘
```

1. **List the facts.** Before you write, list every fact in the source: names, numbers, dates, conditions, exceptions, decisions, links, code names and commands. Keep this list for yourself. It does not go in the result.
2. **Write** with the rules below.
3. **Check.** Go through your list. Every fact must be in the result, with the same meaning. Then read the result and look for facts that are not on your list. Remove them, unless they are a definition (see "Explain big concepts"). Then run the checker script, see below.
4. **Change note.** In rewrite mode, finish your chat answer with 2 or 3 lines. Say what changed, and say if a fact had no clear place. The note goes in the chat, not in the file.

## Rules for the text

### The important thing first

Each document and each section starts with what the reader must know or do. The detail comes after. A reader who stops after the first paragraph must still have the main point.

### Sentences and paragraphs

- Write one topic in each paragraph, with a maximum of 6 sentences.
- Keep sentences short: a maximum of 20 words for instructions and steps, 25 words for descriptions.
- Put one instruction in each sentence.
- Use the active voice. Use the imperative for steps ("Run the migration.").
- Use simple tenses: present, past, future. Avoid the progressive ("is running") and the perfect ("has run") when a simple tense says the same thing.
- Do not drop "the", "a" or "this". Short is good, telegraphic is not.
- Use a vertical list when there is a sequence or more than three items.
- For a warning, give the command first and then the risk: "Do not run this on production. It deletes all rows."

### Words

- Use one word for one thing. When you call it "the session token" once, do not call it "the auth token" later.
- Prefer the common word to the formal one. For example: "start", not "commence"; "use", not "utilize"; "make sure", not "ensure"; "before", not "prior to"; "about", not "approximately"; "to", not "in order to".
- Keep noun clusters to 3 words or fewer. Break up "user session token refresh handler" into "the handler that refreshes the session token of the user".
- Code names, commands, product names and error messages stay exactly as they are.
- A technical word is fine when no simple word says the same thing.

### Explain big concepts

The first time a broad concept appears, add one sentence of context. Broad concepts are things like an architecture style, a design pattern, or how two systems work together. Do the same for every acronym: write it out the first time. For example: "The code uses a hexagonal architecture. In this design, the business rules talk to the outside only through interfaces they own."

A definition is not a new fact, because it does not change what the source says. Keep it general and true. When you are not sure what the source means by a term, ask.

## Diagrams

Add a diagram only when words cannot carry a structure well. Examples are a flow with branches, layers that call each other, a sequence across several systems, or a before and after. When three sentences say it, do not draw.

- **Few boxes.** Use 6 boxes or fewer. When you need more, make two diagrams, or leave out detail that the text already gives.
- **Box-drawing characters inside a `text` code block.** They look the same in a terminal, on GitHub and in an editor. Do not use Mermaid.
- **Short labels.** Put 1 to 4 words in each box. Put conditions on the arrows, or beside them, in plain words.
- **One sentence before the diagram** that says what it shows.
- **No new facts.** A diagram follows the same rule as the text. It shows facts from the source and nothing else.
- **Straight lines.** Every line of a box has the same width, so the borders line up.

The diagram in "The steps" above is an example of the right size.

## Other languages

ASD-STE100 is an English standard. When you write in another language, apply the same structure rules. Write short sentences in the active voice, with one idea each. Use one word for one thing, and the common word over the formal one. In Spanish, for example: "usar", not "utilizar"; "antes de", not "con anterioridad a"; "empezar", not "dar comienzo a". Also "hacer", not "llevar a cabo" or "realizar"; and "para", not "con el fin de".

## The checker script

The script `scripts/check.py`, in this skill's folder, does the counting for you:

```sh
python3 scripts/check.py path/to/file.md
pbpaste | python3 scripts/check.py -
```

It shows sentences over 25 words, paragraphs over 6 sentences, and formal words in English and Spanish with a common word to use. It skips code blocks, inline code, URLs, the frontmatter at the top of a file, and words in double quotes.

The script helps, but it does not decide. A long sentence in a table cell can stay, and so can a formal word inside a quote. It does not check facts: that is step 3, and only you can do it.

## Check before you send

- Every fact from the source is in the result, and no new fact is.
- You ran the checker, and you fixed each finding or kept it on purpose.
- Each diagram has 6 boxes or fewer, and its borders line up.
- In rewrite mode, the chat answer ends with the change note.
