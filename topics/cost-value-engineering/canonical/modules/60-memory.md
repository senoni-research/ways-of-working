# Project and case memory

## A small versioned record, not an automatic belief machine

Use an approved relational store or ordinary versioned records for the first prototype. A graph database is optional, not a prerequisite. Keep methodology guidance, customer-specific evidence, accepted operating rules and runtime model parameters separate. A code change to a template is not consent to persist supplier data.

Each case needs a stable ID; part and document revision; original quote references; normalized inputs; estimate/code version; information date; scoped assumptions; unresolved issues; reviewer corrections; approval status; and later outcomes if authorized. Record values with units and evidence roles. For production, retain appropriate access and retention policies, not merely a filename convention.

## Update cycle

Read relevant existing records, compare with the current documents, perform the task, identify what changed, propose a scoped update and persist only within the authorized policy. Concurrent reviewers must not silently overwrite each other; use an explicit version check or append-and-reconcile process. A correction should identify the previous value, new value, rationale, evidence and affected outputs.

Expire quote validity and time-scoped rates instead of silently carrying them into a new decision. Distinguish a temporary scenario from an accepted long-term parameter. “Try 30,000 units” changes the present scenario, not necessarily the demand plan. “Explore two cavities” is not approval to replace the tool.

## Precedent is not authority

Repeated assistant summaries are not independent observations. Another case involving the same document does not independently corroborate it. A supplier statement can support the supplier's declared offer but does not prove the physical factory assumptions. Independent measurement and engineering review have a different role; retain that distinction.

A model-originated proposal should not re-enter the evidence store as a customer-confirmed fact. Record derivation links, but do not let evidence provenance become a long chain of mutually citing generated summaries. Follow important claims back to an actual document, observation or explicit decision.

This discipline is compatible with the separate Carey-inspired WoW pack's attention to scoped corrections and context. It is not an implementation of Carey's personalized-memory algorithm, a claim of his endorsement, or a reason to load that entire pack for quote arithmetic.

## Typed corrections and scoped precedents

A correction is an event with a type—data, assumption, requirement, commercial judgment or policy change—and each type has an owner and a retention rule ([[55-buyer-decision-and-handoff]]). Store the prior and proposed values, reason, evidence, actor, scope, the revision corrected and whether an approval was invalidated. A commercial judgment is a rationale, not a cost fact; store it as a precedent with its scope. Three identical overrides are three precedents, not a rule; promotion to a rule needs the policy owner's explicit approval and an effective date. Concurrent edits to the same revision are a conflict to reconcile, not a last-writer-wins update.

## Public/private separation

The public method contains only original general guidance, permitted references and synthetic examples. Product development may remain private. Customer evidence must stay out of public handbooks, pull-request comments, test fixtures, screenshots and deployment previews. Raw source publications are not automatically redistributable because they are readable on the web.

A public marketing page may link to the public research organization while its own source lives in a private personal repository. That is a normal division of roles, not a reason to migrate ownership. Publishing site assets can trigger a deployment even if the repository is private. Review the deployment boundary explicitly.

Before staging, inspect file paths and contents, generated archives and images. A generic exclusion scanner can accept a private list outside the repository; it must not print the excluded terms or store the list in tracked tests. A string scan does not detect every identifying example or unauthorized reuse, so semantic review is still required. Never place raw customer data in the source tree just because `.gitignore` will later be added.
