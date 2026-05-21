# English Tech Deep-Dive Module

> Strategy module for high-signal, English-language practitioner writing and big-tech engineering content.

**Trigger scenarios**: architecture deep-dives, postmortems, "how a real company built X", named-author opinion pieces, canonical web-platform/tutorial references, curated launch/show-your-work, weekly digests of what shipped, senior-engineering and eng-leadership writing. Use this module *in addition to* `github-debug` and `stackoverflow` when the question is "how do experienced practitioners think about this?" rather than "what's the fix for this error?".

## Sources (English Practitioner & Deep-Dive Tech)

### Curated discussion (higher signal than general aggregators)
- **Lobsters** (lobste.rs) - invite-only, programming-focused link aggregator; smaller than HN but a higher density of deep-technical comments from domain experts. Tag-filterable (e.g. `lobste.rs/t/rust`); slower front page so stories breathe for days. Use `site:lobste.rs` for narrow topic searches.
- **Hacker News - Show HN & Ask HN** (news.ycombinator.com) - `Show HN` surfaces practitioner-built projects with technical critique in comments; `Ask HN` surfaces experience-based answers from senior engineers. Search via `hn.algolia.com` with `story_text:` / `points>N` filters for high-quality threads.
- **Reddit (senior subs)** - prefer `r/ExperiencedDevs`, `r/programming`, `r/SoftwareEngineering`, `r/devops`, `r/MachineLearning`,`r/LocalLLaMA` and language-specific subs (`r/rust`, `r/golang`, `r/reactjs`). Skip generalist subs for technical depth.

### Big-tech engineering blogs (production-scale "how we built it")
- **Netflix TechBlog** (netflixtechblog.com) - distributed systems, ML platforms, data infra at streaming scale
- **Uber Engineering** (uber.com/blog / eng.uber.com) - backend, data platform, ML, Go, microservices at marketplace scale
- **Stripe Engineering** (stripe.com/blog/engineering, stripe.dev) - payments infra, Ruby/Sorbet, API design, ML for fraud
- **Cloudflare Blog** (blog.cloudflare.com) - networking, edge compute, security, Rust at internet scale
- **GitHub Blog - Engineering** (github.blog/engineering) - dev platform internals, search, scaling Rails
- **Vercel Engineering** (vercel.engineering) - frontend infra, Next.js internals, AI SDK
- Also useful: Discord, Figma, Canva, Meta, Google, Microsoft, AWS Builders' Library, Slack, Shopify, Airbnb, Dropbox, LinkedIn engineering blogs (most live at `<company>.engineering` or `engineering.<company>.com`)

### Named-author / practitioner blogs (opinionated, deep)
- **Martin Fowler** (martinfowler.com) - patterns, refactoring, architecture, evolving practice (canonical)
- **Julia Evans** (jvns.ca) - debugging, systems, networking explained from first principles; also wizardzines.com
- **Dan Abramov** (overreacted.io) - React internals and frontend architecture from a former core-team author
- **Simon Willison** (simonwillison.net) - LLM tooling, SQLite/Datasette, daily TIL-style notes from a high-signal practitioner
- **Dan Luu** (danluu.com) - hardware/perf/CS data-driven essays; also maintains a well-known reading list of programming blogs
- **Eli Bendersky** (eli.thegreenplace.net), **Bryan Cantrill** (bcantrill.dtrace.org), **Drew DeVault** (drewdevault.com), **Hillel Wayne** (hillelwayne.com), **Fabien Sanglard** (fabiensanglard.net) - additional exemplars across systems, formal methods, low-level
- Curated index: **awesome-personal-blogs** (github.com/matt0x6F/awesome-personal-blogs) - when you don't know whose blog to search

### Long-form newsletters (curated weekly synthesis)
- **The Pragmatic Engineer** (newsletter.pragmaticengineer.com) - Gergely Orosz, Big Tech / startup engineering and leadership deep-dives; original reporting often weeks ahead of mainstream
- **TLDR Dev** (tldr.tech/dev) - 5-min daily roundup of the most-discussed dev links
- **Pointer** (pointer.io) - "reading club for software developers"; curated summaries of high-level engineering posts
- **Console.dev** (console.dev) - weekly devtools reviews; good for discovering practitioner-built tools
- **Engineer's Codex** (read.engineerscodex.com) - explains how real companies build systems
- **Bytes** (bytes.dev), **JavaScript Weekly**, **Ruby Weekly**, **Postgres Weekly** etc. (cooperpress.com) - per-language curated weeklies

### Canonical tutorial / reference properties (not Q&A)
- **MDN Web Docs** (developer.mozilla.org) - de facto reference for HTML / CSS / JS / web APIs
- **web.dev** (web.dev) - Chrome team guidance on perf, Core Web Vitals, PWAs, accessibility
- **CSS-Tricks** (css-tricks.com) - long-form CSS / frontend articles and guides
- **Smashing Magazine** (smashingmagazine.com) - in-depth frontend & UX articles
- **JavaScript.info** (javascript.info) - the modern JavaScript tutorial; canonical from-scratch reference
- **Real Python** (realpython.com) - high-quality long-form Python tutorials
- **freeCodeCamp** (freecodecamp.org/news) - tutorial-heavy articles across the stack
- **The Rust Book / Rustonomicon, Go by Example, Python docs HOWTOs** - language-canonical long-form

### Show-your-work / launch venues (find what practitioners are building)
- **Show HN** (news.ycombinator.com/show) - dev-tools, OSS, APIs validated by technical commenters
- **Product Hunt** (producthunt.com) - broader launch audience; useful for SaaS/consumer-tech discovery, less for raw technical critique
- **Indie Hackers** (indiehackers.com) - bootstrapped/solo-founder community; transparency on revenue and build journeys
- **Lobsters "show" tag** (lobste.rs/t/show) - smaller volume, higher quality of feedback than PH

## Query Strategy (Practitioner & Deep-Dive Research)

- **Target the venue, not just the keyword**: prefer `site:lobste.rs <topic>`, `site:martinfowler.com <topic>`, `site:netflixtechblog.com <topic>` over bare keyword search. Big-tech eng blogs and named-author sites are crawled but rank poorly on plain queries.
- **For "how does company X scale Y"**: search the company's engineering blog directly (`<company>.engineering`, `engineering.<company>.com`, `<company>.com/blog/engineering`) before falling back to web search.
- **For opinionated / canonical takes**: search named-author blogs by topic - e.g. `Martin Fowler microservices`, `Julia Evans tcpdump`, `Dan Abramov useEffect`. The author's name acts as a quality filter.
- **For HN/Lobsters discussion mining**: use `hn.algolia.com` with `points>100` or `comments>50`; on Lobsters use full-text search at `lobste.rs/search`. Read the *comments*, not just the linked article - often where the real expertise surfaces.
- **For "what shipped this week / what are people using"**: scan the latest Pragmatic Engineer, TLDR Dev, Console.dev, and Bytes issues; faster than searching.
- **For tutorial / reference questions**: prefer MDN, web.dev, JavaScript.info, Real Python over blog posts of unknown provenance - they're maintained and version-current.
- **Cross-reference long-form pieces against HN/Lobsters comment threads** to surface caveats, corrections, and counter-takes the original author didn't address.
- **Date-check aggressively**: a 2017 blog post on async Python, React hooks, or Kubernetes is often actively misleading. Prefer the most recent canonical reference (MDN/web.dev) or a post dated within the last 18-24 months.
- **For practitioner-built tools**: check Show HN, Console.dev, and Lobsters' `show` tag before generic product directories; the curation filters out marketing-first listings.

## When NOT to use this module

- Exact error messages, stack traces, bug reproductions -> use `github-debug.md`
- "How do I do X in language Y" code-snippet questions -> use `stackoverflow.md`
- Citations / formal research / benchmarks with methodology -> use `academic-papers.md`
- General news, product comparisons, broad Reddit/Discord/X/Medium sweeps -> use `general-web.md`
