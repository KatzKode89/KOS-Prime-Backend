# KOS-Prime Custom Game and App Maker

`tools/kos_maker.py` is a zero-dependency starter generator for instant local implementation. It creates a self-contained Python project for either a `game` or an `app`, including a runnable entrypoint, manifest, README, and Python ignore rules.

## Generate a game

```bash
python3 tools/kos_maker.py game "Crystal Runner" \
  --description "A lattice-powered exploration game." \
  --feature "Crystal movement" \
  --feature "PrimeBus events" \
  --output generated/crystal-runner
cd generated/crystal-runner
python3 main.py
```

## Generate an app

```bash
python3 tools/kos_maker.py app "Ship Console" \
  --description "A small KOS-Prime control console." \
  --feature "Health dashboard" \
  --feature "Voice packet preview"
```

The default destination is `generated/<name>`. Existing non-empty destinations are protected; use `--force` only when replacement is intentional.

Generated manifests identify the project kind and associate it with the `lattice` packet type and `KOSPrime.StackArchitectureMap` ontology segment. The generator does not create hidden services, credentials, network listeners, or external dependencies.