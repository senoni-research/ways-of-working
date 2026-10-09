# M04 — Build a bounded resource estimate

**Use when:** a supported one-stage molding example has reviewed mass, cycle, cavity, yield and rate inputs. **Public context:** [[CV04]], [[CV06]]. **Implementation:** original expected-value equations; not an industrial process simulator.

Fix the material and process boundary first. This reference assumes part mass per attempted cavity, runner mass per shot, no recycled feed or scrap credit, and a uniform good-output fraction. Time includes running but not quality loss or setup. Rates describe the same resources as the recorded time. Different conventions require normalization or a new model.

Compute expected shots, material consumption and run hours. Add separate setup events based on the good-unit batch plan. Charge setup crew separately from run operator fraction. Reject separate labor when the machine rate is declared labor-inclusive. Show material, run, setup and tooling as separate items before a total.

Check sufficient capacity including setup. Do not let quantity grow beyond feasible time while a per-unit graph suggests endless improvement. Do not infer machine selection, engineering equivalence, tooling life or availability from the arithmetic.

**Output:** a labeled scenario estimate, intermediate resource quantities and applicability limits. **Tests:** B03–B09, B15 and C06. **Do not use:** for multi-stage rework, heterogeneous cavities, recycling, mold-flow, safety compliance or supplier-profit assertions. Those need additional evidence and contracts.
