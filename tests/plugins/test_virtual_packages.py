# -*- coding: utf-8 -*-
# Copyright (C) 2012 Anaconda, Inc
# SPDX-License-Identifier: BSD-3-Clause

import conda.core.index
import conda.exceptions
from conda.base.context import context
from conda.testing.solver_helpers import package_dict
from conda import plugins

import pytest


class VirtualPackagesPlugin:
    @plugins.register
    def conda_virtual_package_plugin(self):
        yield plugins.CondaVirtualPackage(
            name="abc",
            version="123",
        )
        yield plugins.CondaVirtualPackage(
            name="def",
            version="456",
        )
        yield plugins.CondaVirtualPackage(
            name="ghi",
            version="789",
        )


@pytest.fixture()
def plugin(plugin_manager):
    plugin = VirtualPackagesPlugin()
    plugin_manager.register(plugin)
    return plugin


def test_invoked(plugin, cli_main):
    index = conda.core.index.get_reduced_index(
        context.default_prefix,
        context.default_channels,
        context.subdirs,
        (),
        context.repodata_fns[0],
    )

    packages = package_dict(index)

    assert packages["__abc"].version == "123"
    assert packages["__def"].version == "456"
    assert packages["__ghi"].version == "789"