# Metaflow QA Tests

## Running Tests

Tests require a local Metaflow development environment with Argo Workflows infrastructure. All test commands must be run inside a `metaflow-dev shell` session.

### Environment activation

The dev environment is activated with two commands. Since `metaflow-dev shell` opens an interactive subshell, pipe commands into it via heredoc:

```sh
pyenv activate metaflow-localenv && cat <<'EOF' | metaflow-dev shell
<commands to run inside the shell>
EOF
```

### Running pytest

Inside the shell, use `python3 -m pytest` (not bare `pytest`):

```sh
pyenv activate metaflow-localenv && cat <<'EOF' | metaflow-dev shell
python3 -m pytest tests/ -v 2>&1
EOF
```

To run a specific test file:
```sh
pyenv activate metaflow-localenv && cat <<'EOF' | metaflow-dev shell
python3 -m pytest tests/argo_workflows/test_argo_basic.py -v 2>&1
EOF
```

To run a single parametrized test, quote the test ID (zsh requires this for brackets):
```sh
pyenv activate metaflow-localenv && cat <<'EOF' | metaflow-dev shell
python3 -m pytest "tests/argo_workflows/conditional_tests/test_conditionals.py::test_conditional_flows[conditionalFlow.py]" -v 2>&1
EOF
```

### Inspecting Argo Workflows directly

Argo workflows run in the `default` Kubernetes namespace. Useful commands (these don't need metaflow-dev shell):

```sh
# List all workflows
argo list

# Get workflow details
argo get <workflow-name>

# Check workflow status as JSON
kubectl get workflow <workflow-name> -o json

# List running workflows
argo list --status Running
```

Workflow metadata maps to Metaflow via annotations:
- `metaflow/flow_name` — the Metaflow flow class name
- `metaflow/run_id` — format is `argo-<workflow-name>`
- Workflow phases: `Running`, `Succeeded`, `Failed`, `Error`

## Project Structure

- `tests/conftest.py` — session-scoped `test_id` fixture for namespace isolation
- `tests/argo_workflows/utils.py` — shared wait/poll utilities (polls Argo via kubectl for fast failure detection)
- `tests/argo_workflows/test_argo_basic.py` — deploy + trigger + run tests for basic flows
- `tests/argo_workflows/parameter_tests/` — event triggers, cron schedules, parameter passing
- `tests/argo_workflows/conditional_tests/` — conditional step branching
- `tests/argo_workflows/deploy_time_triggers/` — deploy-time trigger configuration (no run waiting)
- `tests/basic/` — local `Runner` tests (no Argo needed)
- `tests/kubernetes/` — Kubernetes `Runner` tests
- `tests/flows/` — shared flow definitions used by multiple test suites

## Test Patterns

**Argo tests** follow this pattern: deploy flow via `Deployer`, trigger it, poll for completion via `utils.py` helpers, assert results, then delete the deployment in a `finally` block.

**Deploy-only tests** (e.g., deploy_time_triggers) only verify that `Deployer.create()` succeeds or fails as expected, without running the flow.

**Failure tests** verify that certain flows fail to deploy (`test_failing_conditional_flows`) or that runs fail as expected (`test_bug_conditional_flows`).
