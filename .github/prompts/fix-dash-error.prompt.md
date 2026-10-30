---
description: Fix a Dash error from the dev tools or the terminal
agent: agent
argument-hint: paste the error text
---
My Dash app `${input:file:my_app.py}` shows this error:

```
${input:error:paste the error text from the red box in the dev tools, or from the terminal}
```

1. Explain in two or three sentences what the error means, in Dash terms (ids, properties,
   Inputs, Outputs, return values).
2. Fix the cause, not the symptom: no `try/except` that hides the error, no `suppress_callback_exceptions`
   unless the layout really is built by callbacks.
3. If `.github/skills/dash-app/check_app.py` exists, run it on the app and show its output.
