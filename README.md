#### Development setup

This assumes you have postgresql running locally, and have pipenv installed.

- `make install` to install dependencies
- copy `.env.def` file to `.env` and replace postgres connection and recaptcha settings.
  For development env, email/smtp settings can be left empty, emails are printed out in the console.
- `make migrate`
- `make run`
