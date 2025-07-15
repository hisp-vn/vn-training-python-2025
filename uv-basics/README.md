# uv-basics

Basics commands for creating projects and installing deps using uv.

### Creating a new project

1. Basic app setup with `pyproject.toml` and `main.py`

```
uv init --app <name>
```

3. Basic (python) package setup with `pyproject.toml`, and a `src/NAME` setup for packages.

```
uv init --package <name>
```

3. Basic lib setup with `pyproject.toml`, and a `src/NAME` setup for libraries.

```
uv init --lib <name>
```

### Managing project dependencies

1. Add/remove a dependencies

```
uv add <dep-name>
uv remove <dep-name>
```

2. Add/remove a developer dependencies

```
uv add --dev <dep-name>
uv remove --dev <dep-name>
```
