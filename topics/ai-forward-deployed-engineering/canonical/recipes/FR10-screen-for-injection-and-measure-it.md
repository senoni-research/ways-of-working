# FR10 — Screen for injection and measure it

**Use when:** an agent reads text the system didn't write, such as claims, documents, emails or web pages. **Modules:** [[60-security-and-guardrails]]. **Sources:** [[FD15]], [[FD16]], [[FD17]], [[FD18b]], [[FD22b]]; the per-session check, the screening report and the red-team set are Senoni practice. **Reference:** `reference/guardrails.py`, cases FC22 and FC23.

1. List every tool one session holds, and mark which read private data, which read untrusted content and which can send data out. Count the customer's own text as untrusted.
2. If one session holds all three, remove a leg. Prefer breaking the way out, for example fixed messages to the customer on file instead of free text to any address.
3. Record the design that limits what untrusted text can make the agent do, such as a fixed action set validated in code. Name the wrong actions it still permits, such as a wrong choice among the permitted actions, and who or what catches each.
4. Only then add a screen, as one more layer.
5. Build a labelled set: attacks in every channel the agent reads, with several techniques each, and benign items from real traffic patterns.
6. Report misses by channel and technique, and false alarms, each with its n and Wilson interval. Report the upper bound where there were no misses.
7. Keep the attacks as a red-team set, and run it on every change to the prompt, tools or model.

**Output:** the trifecta check per session, the design decision, and the screening report. **Checks:** FB65, FB66, FB74, FB75. **Do not use:** a screen's score as the reason the design is safe; the design must hold when the screen misses.
