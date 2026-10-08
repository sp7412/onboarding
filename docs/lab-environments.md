# Lab environments

The labs support two low-friction paths in addition to a normal local virtualenv.

## Codespaces / dev container

Use the repository's dev container when you want the **full environment** on a new
laptop or in GitHub Codespaces.

1. Open the repository in GitHub Codespaces.
2. Let the dev container finish creating the Python 3.12 environment.
3. Run the notebooks from the labs directory with Jupyter, or use the repository's
   normal offline test commands.

The container installs the same `requirements.txt` used by the local setup. It
does not provide API keys; live exercises still require personal credentials in
a local `.env` and should use fictional data.

## Google Colab

Use an **Open in Colab** badge on a notebook when you want to run one lab from
a phone, tablet, or unfamiliar machine without setting up the repository first.

Each lab notebook begins with a Colab-aware setup cell. In Colab, it clones the
public repository, installs `requirements.txt`, and changes into the repository
root. Outside Colab, that cell is a no-op.

Colab runs are offline-first just like local runs. Optional live cells still
require your own API keys and should never contain employer or customer data.

### Which path should I use?

| Need | Best path |
|---|---|
| Work through many labs or modify code | Codespaces / dev container |
| Reproduce the full repository environment | Codespaces / dev container |
| Try one notebook quickly | Google Colab |
| Phone or unfamiliar machine | Google Colab |
| Offline tests and repository changes | Codespaces / local environment |
