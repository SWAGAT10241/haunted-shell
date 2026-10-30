## Description
<!-- Provide a brief description of the changes introduced by this pull request. -->

## Type of Change
- [ ] 🐛 Bug fix (non-breaking change which fixes an issue)
- [ ] ✨ New feature or spectral persona
- [ ] 🔒 Security or privacy enhancement
- [ ] 📚 Documentation update
- [ ] 🧪 Testing improvement

## Security & Air-Gap Checklist
- [ ] **Zero Telemetry Guarantee:** This PR introduces NO remote network requests, tracking, or telemetry sinks.
- [ ] **Secret Safety:** No private tokens, credentials, or keys are exposed.
- [ ] Tested locally with `haunt airgap`.

## Testing Done
- [ ] Unit tests added / updated in `tests/test_haunt.py`
- [ ] All tests passing (`pytest tests/`)
- [ ] Tested CLI commands manually (`haunt shell`, `haunt whisper`, `haunt exorcise`)
