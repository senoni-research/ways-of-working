# Attribution and reuse

Senoni Research authored the selection, synthesis, instruction packaging, examples and tools in this pack. The engineering practices are not claimed as Senoni inventions. This is an independent adaptation, not an official framework, certification, collaboration or endorsement by any cited author or organisation.

## Source basis

The method sources are public. Agent design and context engineering rest on Anthropic's engineering articles (FD01, FD02, FD03a, FD13), Philipp Schmid (FD03b), OpenAI's practical guide (FD04) and Walden Yan at Cognition (FD14). Working with a coding agent rests on Anthropic's Claude Code guidance (FD05a, FD05b) and the `AGENTS.md` format (FD06). Evaluation rests on Hamel Husain (FD07), Evan Miller (FD08), Lianmin Zheng and colleagues (FD09), Jacob Cohen and the scikit-learn documentation (FD10a, FD10b), Edwin B. Wilson and Lawrence D. Brown, T. Tony Cai and Anirban DasGupta (FD22a, FD22b), and Yue Jia and Mark Harman on mutation testing (FD25). Retrieval rests on Patrick Lewis and colleagues (FD11) and Stephen Robertson and Hugo Zaragoza (FD12). Security rests on Simon Willison (FD15), the OWASP Gen AI Security Project (FD16) and Luca Beurer-Kellner and colleagues (FD17). Risk, reliability and operations rest on NIST (FD18a, FD18b), Google's two SRE books (FD19a, FD19b), the AWS Generative AI Lens (FD20), Malcolm Featonby and Marc Brooker in the Amazon Builders' Library (FD27, FD29), John D. C. Little (FD23a, FD23b) and the OpenTelemetry GenAI semantic conventions (FD28). Customer data rests on the GDPR (FD24a) and the UK Information Commissioner's Office (FD24b).

Three role descriptions describe the forward deployed engineer's work: Palantir's blog post (FD21a) and archived copies of two job postings (FD21b, FD21c). They are cited for what the role involves, not as evidence that any practice works. One vendor page (FD26) is cited only for how a market term is used.

The documentation records (H) point to the official pages of the tools the examples mention. A module may cite one only after its page has been re-read and its scope recorded; the builder refuses a citation of a record that is still only link-checked. Twenty-eight have been re-read. Twelve for the first two releases: Claude Code's memory page, OpenAI's function calling, structured outputs and reasoning guides, Pydantic's validators, the Claude Agent SDK's Python reference, OpenRouter's usage accounting, prompt caching and provider routing pages, Anthropic's prompt caching page, LangGraph's graph API, persistence, interrupts, durability and error pages, the 2025 revisions of the MCP specification with their transports and security guidance, Langfuse's tracing, sessions and experiments pages, PostgreSQL's INSERT and explicit locking pages, SQLite's transaction page with Python's `sqlite3` documentation, and the AgentCore Memory guides and data-plane references. Sixteen for 0.3.0: Cedar's overview, authorization and validation pages, AgentCore Policy's scope page, Python's `hmac` and `secrets` documentation, Secrets Manager's rotation pages, IAM's security best practices, the SigV4 signing pages, GitHub's OpenID Connect pages, Lambda's alias, weighted alias and reserved concurrency pages with Mangum's lifespan page, Supabase's connection page, AgentCore pricing, CloudWatch's missing-data and alarm evaluation pages, AWS Budgets' cost management page and CostTypes reference, CDK's bootstrapping page, Resource Explorer's ListResources and immediate discovery pages, AgentCore Runtime's contract, lifecycle, long-running, auth, session, V2 and versioning pages, and AgentCore Identity's workload access token page. OpenAI's data controls page and OpenRouter's data collection page were added to their records. For the remaining seven, only the addresses and titles were checked.

The warranty desk in the cases and reference code is an original synthetic example. Its business, claims, terms and amounts are invented for this pack.

The [source register](SOURCE_REGISTER.md) gives each record's inspection level, inspected scope, use and limits. Some records are bibliographic only, because the original is behind a paywall; the register says so.

## How the practices were selected

The maintainer chose which practices to cover while taking Ed Donner's course "AI FDE: The Forward Deployed Engineer & Agentic AI Architect". The course is acknowledged as where the selection started, and only that:

- No course material is reproduced or adapted: no lectures, transcripts, slides, notebooks, code, data, briefs, or the course's fictional company and its records.
- Every practice rests on a public source in the register, or is labelled as Senoni's own choice and backed by an original synthetic case.
- Ed Donner has not reviewed, approved or endorsed this pack, and nothing in it is presented as his teaching.

## Labels in the modules

A practice that adapts a source cites it with its register ID. A practice marked "Senoni" is our own choice: a rule, threshold or design the sources don't state. Exact source wording is quoted and attributed; a paraphrase is never presented as a quotation.

## Reuse

We do not redistribute the cited publications, job postings, documentation, datasets or code. A citation is not a licence grant, and source works keep their own terms. The repository's MIT licence covers this original package; it does not relicense external publications, data, marks or logos. Raw working copies of sources are kept in the repository's git-ignored `workspace/` and are not part of any deliverable.

The Carey, Vandeput and cost packs keep their own authorship chains and scopes. Installing this pack beside them does not make it their work, or them part of it.

Future additions need point-of-use credit, primary authors where available, inspected scope and a version or date. Keep an indirect account distinct from the original. Preserve conflicting interpretations rather than attribute a reconciled opinion to everyone.
