import pytest
import yaml
import os
import pytest
from py._xmlgen import html

@pytest.mark.hookwrapper
def pytest_runtest_makereport(item):
    pytest_html = item.config.pluginmanager.getplugin('html')
    outcome = yield
    report = outcome.get_result()
    report.nodeid = report.nodeid.encode("utf-8").decode("unicode_escape")

@pytest.fixture(scope="session")
def env(request):
    config_path = os.path.join(request.config.rootdir,
                               "config",
                               "test",
                               "config.yaml")
    with open(config_path) as f:
        env_config = yaml.load(f.read(), Loader=yaml.SafeLoader)
    return env_config


@pytest.fixture(scope="function")
def preparation(self):
    print("在数据库中准备测试数据")
    test_data = "在数据库中准备测试数据"
    yield test_data
    print("清理测试数据")
