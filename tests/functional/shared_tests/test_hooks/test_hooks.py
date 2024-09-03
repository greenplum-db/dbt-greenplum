"""
This file needs to be in its own directory because it uses a `data` directory.
Placing this file in its own directory avoids collisions.
"""

from dbt.tests.adapter.hooks.test_model_hooks import (
    BasePrePostModelHooks,
    BaseHookRefs,
    BasePrePostModelHooksOnSeeds,
    BaseHooksRefsOnSeeds,
    BasePrePostModelHooksOnSeedsPlusPrefixed,
    BasePrePostModelHooksOnSeedsPlusPrefixedWhitespace,
    BasePrePostModelHooksOnSnapshots,
    BasePrePostModelHooksInConfig,
    BasePrePostModelHooksInConfigWithCount,
    BasePrePostModelHooksInConfigKwargs,
    BasePrePostSnapshotHooksInConfigKwargs,
    BaseDuplicateHooksInConfigs,
)
from dbt.tests.adapter.hooks.test_run_hooks import (
    BasePrePostRunHooks,
    BaseAfterRunHooks,
)

def _greenplum_check_model_hooks(self, state, project, host, count=1):
    # This function is taking from dbt.tests.adapter.hooks.test_model_hooks.BaseTestPrePost but
    # change ctx["target_type"] and ctx["target_user"].
    ctxs = self.get_ctx_vars(state, count=count, project=project)
    for ctx in ctxs:
        assert ctx["test_state"] == state
        assert ctx["target_dbname"] == "dbt"
        assert ctx["target_host"] == host
        assert ctx["target_name"] == "default"
        assert ctx["target_schema"] == project.test_schema
        assert ctx["target_threads"] == 4
        assert ctx["target_type"] == "greenplum"
        assert ctx["target_user"] == "gpadmin"
        assert ctx["target_pass"] == ""

        assert (
            ctx["run_started_at"] is not None and len(ctx["run_started_at"]) > 0
        ), "run_started_at was not set"
        assert (
            ctx["invocation_id"] is not None and len(ctx["invocation_id"]) > 0
        ), "invocation_id was not set"
        assert ctx["thread_id"].startswith("Thread-")

def _greenplum_check_run_hooks(self, state, project, host):
    # This function is taking from dbt.tests.adapter.hooks.test_run_hooks.BasePrePostRunHooks but
    # change ctx["target_type"] and ctx["target_user"].
    ctx = self.get_ctx_vars(state, project)

    assert ctx["test_state"] == state
    assert ctx["target_dbname"] == "dbt"
    assert ctx["target_host"] == host
    assert ctx["target_name"] == "default"
    assert ctx["target_schema"] == project.test_schema
    assert ctx["target_threads"] == 4
    assert ctx["target_type"] == "greenplum"
    assert ctx["target_user"] == "gpadmin"
    assert ctx["target_pass"] == ""

    assert (
        ctx["run_started_at"] is not None and len(ctx["run_started_at"]) > 0
    ), "run_started_at was not set"
    assert (
        ctx["invocation_id"] is not None and len(ctx["invocation_id"]) > 0
    ), "invocation_id was not set"
    assert ctx["thread_id"].startswith("Thread-") or ctx["thread_id"] == "MainThread"


class TestPrePostModelHooks(BasePrePostModelHooks):
    # Greenplum-Specific: using greenplum configuration
    def check_hooks(self, state, project, host, count=1):
        _greenplum_check_model_hooks(self, state, project, host, count)


class TestHookRefs(BaseHookRefs):
    # Greenplum-Specific: using greenplum configuration
    def check_hooks(self, state, project, host, count=1):
        _greenplum_check_model_hooks(self, state, project, host, count)


class TestPrePostModelHooksOnSeeds(BasePrePostModelHooksOnSeeds):
    pass


class TestHooksRefsOnSeeds(BaseHooksRefsOnSeeds):
    pass


class TestPrePostModelHooksOnSeedsPlusPrefixed(BasePrePostModelHooksOnSeedsPlusPrefixed):
    pass


class TestPrePostModelHooksOnSeedsPlusPrefixedWhitespace(
    BasePrePostModelHooksOnSeedsPlusPrefixedWhitespace
):
    pass


class TestPrePostModelHooksOnSnapshots(BasePrePostModelHooksOnSnapshots):
    pass


class TestPrePostModelHooksInConfig(BasePrePostModelHooksInConfig):
    # Greenplum-Specific: using greenplum configuration
    def check_hooks(self, state, project, host, count=1):
        _greenplum_check_model_hooks(self, state, project, host, count)


class TestPrePostModelHooksInConfigWithCount(BasePrePostModelHooksInConfigWithCount):
    # Greenplum-Specific: using greenplum configuration
    def check_hooks(self, state, project, host, count=1):
        _greenplum_check_model_hooks(self, state, project, host, count)


class TestPrePostModelHooksInConfigKwargs(BasePrePostModelHooksInConfigKwargs):
    # Greenplum-Specific: using greenplum configuration
    def check_hooks(self, state, project, host, count=1):
        _greenplum_check_model_hooks(self, state, project, host, count)    


class TestPrePostSnapshotHooksInConfigKwargs(BasePrePostSnapshotHooksInConfigKwargs):
    pass


class TestDuplicateHooksInConfigs(BaseDuplicateHooksInConfigs):
    pass


class TestPrePostRunHooks(BasePrePostRunHooks):
    # Greenplum-Specific: using greenplum configuration
    def check_hooks(self, state, project, host):
        _greenplum_check_run_hooks(self, state, project, host)


class TestAfterRunHooks(BaseAfterRunHooks):
    pass
