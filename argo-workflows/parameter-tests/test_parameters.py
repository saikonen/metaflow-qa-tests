from time import sleep
from datetime import datetime
import pytest
from metaflow import Deployer, namespace, Flow
from payloads import PAYLOADS
import os

ROOTPATH = os.path.dirname(__file__)

# TODO: Add coverage for dashed params and double-quoted strings!

def test_events():
    try:
        deployed_event_flow = Deployer(flow_file=os.path.join(ROOTPATH, "eventflow.py")).argo_workflows().create()
        deployed_trigger_flow = Deployer(flow_file=os.path.join(ROOTPATH, "triggering_flow.py")).argo_workflows().create()

        # run the flow that sends an event.
        triggered_run = deployed_trigger_flow.trigger()

        run = wait_for_result(triggered_run, timeout=180)
        assert run.successful
    
        # Await the event triggered flows.
        current_ts = run.created_at # rough estimate on when event triggered flows should start kicking off.

        runs = wait_for_runs_after_ts(deployed_event_flow.flow_name, tag=None, after_ts = current_ts, expected_runs=len(PAYLOADS), timeout=120)

        finished_runs = [wait_for_run_to_finish(run, timeout=120) for run in runs]

        for run in finished_runs:
            assert run.successful
    finally:
        deployed_trigger_flow.delete()
        deployed_event_flow.delete()

def test_cron():
    try:
        deployed_cron_flow = Deployer(flow_file=os.path.join(ROOTPATH, "cronflow.py")).argo_workflows().create(tags=["test_suite_cron"])

        run = wait_for_run(
            flow_name=deployed_cron_flow.flow_name,
            tag="test_suite_cron",
            timeout=2*60+10 # 2 minutes for the test cron flow.
        )

        assert run.successful
    finally:
        deployed_cron_flow.delete()


def test_base_params():
    try:
        deployed_flow = Deployer(flow_file=os.path.join(ROOTPATH, "paramflow.py")).argo_workflows().create()
        triggered_run = deployed_flow.trigger()

        run = wait_for_result(triggered_run)
        assert run.successful
    finally:
        deployed_flow.delete()


# Helpers

def wait_for_result(triggered_run, timeout=60):
    slept = 0
    while triggered_run.run is None and slept < timeout:
        slept += 10
        sleep(10)
    
    if triggered_run.run is None:
        raise TimeoutError("Waiting for flow failed. Waited for %s seconds with no results" % timeout)
    
    run = wait_for_run_to_finish(triggered_run.run, timeout)

    return run

def wait_for_run(flow_name, tag=None, timeout=60):
    namespace(tag)
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
        slept += 10
        sleep(10)
    
    if run is None:
        raise TimeoutError("Found no new run in the span of %s seconds. Timed out." % timeout)
    
    run = wait_for_run_to_finish(run, timeout)

    namespace(None)
    return run

def wait_for_runs_after_ts(flow_name, tag=None, after_ts=None, expected_runs=1, timeout=60):
    namespace(tag)
    current_ts = after_ts or datetime.now()
    runs = []
    pathspecs = set()
    slept = 0
    while len(runs)<expected_runs and slept < timeout:
        try:
            flow = Flow(flow_name)
        except Exception:
            flow = None
        
        if flow is not None:
            for run in flow.runs():
                if run.created_at < current_ts:
                    break # we're iterating too old runs already
                
                if run.pathspec in pathspecs:
                    continue # already covered this run
                
                pathspecs.add(run.pathspec)
                runs.append(run)
                if len(runs)==expected_runs:
                    break # we have enough runs gathered
        if len(runs)==expected_runs:
            break # we have enough runs gathered
        
        slept += 10
        sleep(10)

    if len(runs)!=expected_runs:
        raise TimeoutError("Could not gather %s runs in %s seconds" % (expected_runs, timeout))
    
    namespace(None)
    return runs

def wait_for_run_to_finish(run, timeout=60):
    slept = 0
    while not run.finished and slept < timeout:
        slept += 10
        sleep(10)

    if not run.finished:
        raise TimeoutError("Triggered run did not finish in time. Waited for %s seconds for the run to finish" % timeout)
    
    return run

if __name__=="__main__":
    test_events()