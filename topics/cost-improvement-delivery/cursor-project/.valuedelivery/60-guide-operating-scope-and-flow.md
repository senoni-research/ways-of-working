# Guidance: operating scope and flow

*Guidance only. No helper, schema or test implements flow mapping in this release.*

## When to read this

Read this chapter when the proposed change crosses several functions: customer requirement, product or part family, supplying operation, transport, receiving, inspection, storage, point of use, engineering change and the owner of the resulting benefit. Map only the interfaces material to this decision, not the whole enterprise.

Value-stream mapping separates the current material and information flow from a proposed future state ([OPS01](90-sources.md#ops01)). The archetypes and review prompts below are this companion's original operationalisation, not a reproduced mapping standard, and no source diagram or template is included.

## Describe flows by the operating problem

Use descriptive, revisable archetypes. They are not a colour code and not a spend classification pretending to be a replenishment rule. Several can apply at once.

| Archetype | Main question | Typical evidence |
|---|---|---|
| Repetitive production input | Can supply follow the reviewed production requirement reliably? | demand and mix, replenishment behaviour, yield, stock exposure |
| Configurable or customer-specific option | Where is the configuration frozen and what lead time was promised? | option rules, configuration owner, order trigger, delivery responsibility |
| Development or change-controlled item | Is the revision qualified and ready for controlled introduction? | release state, tests, tooling, cutover, legacy stock |
| Low-value, transaction-intensive item | Is handling and administration out of proportion to the item economics? | orders, touches, transport and packaging, service constraints |
| Service-critical or intermittent item | What protects availability when demand is rare or uncertain? | criticality, substitution, repair route, service objective |

Explain the chosen treatment and review it after a material change. These categories do not replace forecasting or inventory policy; consume an approved planning policy where one exists.

## Work through the interfaces

Draw the current chain with named owners, triggers, waiting points, information revisions and exception loops. Ask the people doing the work to correct it. Mark what was observed and what was only described. Map the proposed change on the same boundary, so that work, cost or stock moved elsewhere stays visible. Waiting for a drawing clarification is a different queue from goods in transit.

## Output

An interface map and a short list of decision-critical unknowns attached to VDT01. Accepting the map authorises further analysis only. Reopen it when the customer promise, specification, site or horizon changes.
