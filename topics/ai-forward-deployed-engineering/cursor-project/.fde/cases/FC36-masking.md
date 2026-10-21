# FC36 — Masking before the model

**Module:** 75, customer data. **Reference:** `reference/customer_data.py`. **Specs:** FB88.

**Input.** A claim description that gives the customer's name, postcode, phone number, email address and card number, and the name of a friend who saw the fault happen. The customer record knows her name.

**Expected answer.** The text sent to the model:

> [NAME-1] here. My battery died on the canal path near [POSTCODE-1]. Call me on [PHONE-1] or email [EMAIL-1]. I paid with card [CARD-1]. My friend Tom Reed saw it happen.

The mapping from each placeholder to its value stays on the desk's side, and putting the values back gives the original text.

**What it shows.** Masking reduces what a third-party model sees; it doesn't make the text anonymous. The friend's name passes through because nothing knew it. Decide what may go to a provider from its recorded terms (FC34), and mask what doesn't need to go. The patterns are examples for these cases, not a complete detector.
