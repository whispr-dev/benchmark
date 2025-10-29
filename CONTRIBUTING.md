CONTRIBUTING.md
# Contributing

Thanks for improving the Cross-Platform SIMD RNG Benchmark Visualizer!

## Code Style
- Follow **PEP 8** and **Black** formatting.
- Keep imports clean and grouped (stdlib → third-party → local).
- Use `snake_case` for variables, `PascalCase` for classes.
- Avoid hardcoding file paths; use `os.path.join()`.

## Development Workflow
1. Fork the repo and create a feature branch:
   ```bash
   git checkout -b feature/your-feature


Make changes and test locally.

Commit with clear, conventional messages:

feat: add dark theme color presets
fix: correct font overlap in legend


Push and open a PR to main.

Testing

Before PR submission:

python plot-cross-platform-adv.py --baseline windows-msvc --multi-panel --top3-table


Ensure it completes without warnings.

Documentation

If you add or modify features, update README.md accordingly.

Communication

Use GitHub Issues for:

Feature requests

Bug reports

Clarifications or feedback


---