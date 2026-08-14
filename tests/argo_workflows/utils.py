from metaflow import namespace, Flow
from datetime import datetime
from time import sleep
import subprocess
import json

POLL_INTERVAL = 2  # seconds between polls


def get_argo_workflow_phase(flow_name):
    """
    Query Argo directly via kubectl to get the workflow phase for a flow.
    Returns (phase, workflow_name) or (None, None) if not found.
    Phases: Running, Succeeded, Failed, Error
    """
    try:
        result = subprocess.run(
            [
                "kubectl",
                "get",
                "workflows",
                "-o",
                "json",
                "--sort-by=.metadata.creationTimestamp",
            ],
            capture_output=True,
            text=True,
            timeout=10,
        )
        if result.returncode != 0:
            return None, None

        data = json.loads(result.stdout)
        # Find the most recent workflow for this flow name
        for item in reversed(data.get("items", [])):
            annotations = item.get("metadata", {}).get("annotations", {})
            if annotations.get("metaflow/flow_name") == flow_name:
                phase = item.get("status", {}).get("phase", "")
                wf_name = item["metadata"]["name"]
                return phase, wf_name
    except Exception:
        pass
    return None, None


def get_argo_workflow_phase_by_name(workflow_name):
    """Get the phase of a specific Argo workflow by its name."""
    try:
        result = subprocess.run(
            ["kubectl", "get", "workflow", workflow_name, "-o", "json"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        if result.returncode != 0:
            return None
        data = json.loads(result.stdout)
        return data.get("status", {}).get("phase", "")
    except Exception:
        return None


def wait_for_result(triggered_run, timeout=60):
    "Wait for a TriggeredRun to have an executing run attached to it"
    slept = 0
    while triggered_run.run is None and slept < timeout:
        sleep(POLL_INTERVAL)
        slept += POLL_INTERVAL

    if triggered_run.run is None:
        raise TimeoutError(
            "Waiting for flow failed. Waited for %s seconds with no results" % timeout
        )

    run = wait_for_run_to_finish(triggered_run.run, timeout)

    return run


def wait_for_run(flow_name, ns=None, timeout=60):
    "Wait for a Run for a flow name to start executing in the given namespace"
    namespace(ns)
    slept = 0
    current_ts = datetime.now()
    run = None
    while slept < timeout:
        try:
            latest_run = Flow(flow_name).latest_run
        except Exception:
            latest_run = None

        if latest_run is not None and latest_run.created_at > current_ts:
            run = latest_run
            break

        # Check Argo directly - if the workflow already finished,
        # Metaflow should have recorded it soon; no point waiting the full timeout
        phase, _ = get_argo_workflow_phase(flow_name)
        if phase in ("Succeeded", "Failed", "Error"):
            # Give Metaflow a few more seconds to sync before giving up
            if slept > 15:
                break

        sleep(POLL_INTERVAL)
        slept += POLL_INTERVAL

    if run is None:
        raise TimeoutError(
            "Found no new run in the span of %s seconds. Timed out." % timeout
        )

    namespace(None)
    return run


def wait_for_runs_after_ts(
    flow_name, ns=None, after_ts=None, expected_runs=1, timeout=60
):
    """
    Wait for a number of runs for a flow name to start executing
    after a given timestamp in the specified namespace
    """
    namespace(ns)
    current_ts = after_ts or datetime.now()
    runs = []
    pathspecs = set()
    slept = 0
    while len(runs) < expected_runs and slept < timeout:
        try:
            flow = Flow(flow_name)
        except Exception:
            flow = None

        if flow is not None:
            for run in flow.runs():
                if run.created_at < current_ts:
                    break  # we're iterating too old runs already

                if run.pathspec in pathspecs:
                    continue  # already covered this run

                pathspecs.add(run.pathspec)
                runs.append(run)
                if len(runs) == expected_runs:
                    break  # we have enough runs gathered
        if len(runs) == expected_runs:
            break  # we have enough runs gathered

        sleep(POLL_INTERVAL)
        slept += POLL_INTERVAL

    if len(runs) != expected_runs:
        raise TimeoutError(
            "Could not gather %s runs in %s seconds" % (expected_runs, timeout)
        )

    namespace(None)
    return runs


def wait_for_run_to_finish(run, timeout=120):
    "Wait for a Run to finish, with fast failure detection via Argo"
    # Try to extract the Argo workflow name from the run ID for direct status checks
    argo_wf_name = None
    try:
        run_id = run.id
        if run_id.startswith("argo-"):
            argo_wf_name = run_id[len("argo-") :]
    except Exception:
        pass

    slept = 0
    argo_done = False
    while not run.finished_at and slept < timeout:
        # Check Argo workflow status directly for fast failure detection
        if argo_wf_name and not argo_done:
            phase = get_argo_workflow_phase_by_name(argo_wf_name)
            if phase in ("Succeeded", "Failed", "Error"):
                argo_done = True
                # Argo is done; give Metaflow a few seconds to sync before giving up
                argo_sync_deadline = slept + 15

        if argo_done and slept >= argo_sync_deadline:
            break

        sleep(POLL_INTERVAL)
        slept += POLL_INTERVAL

    if not run.finished_at:
        if argo_done:
            raise RuntimeError(
                "Argo workflow %s finished with phase '%s' but Metaflow did not record completion within %s seconds"
                % (argo_wf_name, phase, timeout)
            )
        raise TimeoutError(
            "Triggered run did not finish in time. Waited for %s seconds for the run to finish"
            % timeout
        )

    # We record an exception but finish test flows in order to get a faster test result,
    # instead of having to wait for a timeout
    test_failure = getattr(run.data, "test_failure", None)
    if test_failure is not None:
        raise test_failure

    return run
