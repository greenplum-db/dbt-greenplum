# Contributing to `dbt-greenplum`

- [About this document](#about-this-document)
- [Getting the code](#getting-the-code)
- [Developing](#developing)
- [Testing](#testing)
- [Documentation](#documentation)
- [Submitting a pull request](#submitting-a-pull-request)


## About this document

This document is a guide for anyone interested in contributing to `dbt-greenplum`.
It outlines how to install `dbt-greenplum` for development,
run tests locally, update documentation, and submit pull requests.
This guide assumes users are developing on a Linux or MacOS system.
The following utilities are needed or will be installed in this guide:

- `pip`
- `virturalenv`
- `git`
- `changie`

If local functional testing is required, then a database instance
and appropriate credentials are also required.

In addition to this guide, users are highly encouraged to read the `dbt-core`
[CONTRIBUTING.md](https://github.com/dbt-labs/dbt-core/blob/main/CONTRIBUTING.md).
Almost all information there is applicable here.


## Developing

### Installation

1. Ensure the latest version of `pip` is installed:
   ```shell
   pip install --upgrade pip
   ```
2. Configure and activate a virtual environment using `virtualenv` as described in
[Setting up an environment](https://github.com/dbt-labs/dbt-core/blob/HEAD/CONTRIBUTING.md#setting-up-an-environment)
3. Install `dbt-greenplum` and development dependencies in the virtual environment
   ```shell
   pip install -e .[dev]
   ```

When `dbt-greenplum` is installed this way, any changes made to the `dbt-greenplum` source code
will be reflected in the virtual environment immediately.


## Testing

`dbt-greenplum` contains [unit](https://github.gwd.broadcom.net/TNZ/dbt-greenplum/tree/main/tests/unit)
and [functional](https://github.gwd.broadcom.net/TNZ/dbt-greenplum/tree/main/tests/functional) tests.


### Unit tests

Unit tests can be run locally without setting up a database connection:

```shell
# Note: replace $strings with valid names

# run all unit tests in a module
python -m pytest tests/unit/$test_file_name.py
# run a specific unit test
python -m pytest tests/unit/$test_file_name.py::$test_class_name::$test_method_name
```

### Functional tests

Functional tests require a database to test against. There are two primary ways to run functional tests:

- Tests will run automatically against a dbt Labs owned database during PR checks
- Tests can be run locally by configuring a `test.env` file with appropriate `ENV` variables:
   ```shell
   cp test.env.example test.env
   $EDITOR test.env
   ```

> **_WARNING:_** The parameters in `test.env` must link to a valid database.
> `test.env` is git-ignored, but be _extra_ careful to never check in credentials
> or other sensitive information when developing.

Functional tests can be run locally with a valid database connection configured in `test.env`:

```shell
# Note: replace $strings with valid names

# run all functional tests in a directory
python -m pytest tests/functional/$test_directory
# run all functional tests in a module
python -m pytest tests/functional/$test_dir_and_filename.py
# run all functional tests in a class
python -m pytest tests/functional/$test_dir_and_filename.py::$test_class_name
# run a specific functional test
python -m pytest tests/functional/$test_dir_and_filename.py::$test_class_name::$test__method_name
```


## Documentation

### User documentation

Many changes will require an update to `dbt-greenplum` user documentation.
All contributors, whether internal or external, are encouraged to open an issue or PR
in the docs repo when submitting user-facing changes. Here are some relevant links:

- [User docs](https://docs.getdbt.com/)
  - [Warehouse Profile](https://docs.getdbt.com/reference/warehouse-profiles/)
  - [Resource Configs](https://docs.getdbt.com/reference/resource-configs/)
- [User docs repo](https://github.com/dbt-labs/docs.getdbt.com)

### CHANGELOG entry

`dbt-greenplum` uses [changie](https://changie.dev) to generate `CHANGELOG` entries.
Follow the steps to [install `changie`](https://changie.dev/guide/installation/).

Once changie is installed and the PR is created, run:
   ```shell
   changie new
   ```
`changie` will walk through the process of creating a changelog entry.
Remember to commit and push the file that's created.

> **_NOTE:_** Do not edit the `CHANGELOG.md` directly.
> Any modifications will be lost by the consolidation process.


## Submitting a pull request

### Opening a pull request

A `dbt-greenplum` maintainer will be assigned to review each PR based on priority and capacity.
They may suggest code revisions for style and clarity or they may request additional tests.
These are good things! dbt Labs believes that contributing high-quality code is a collaborative effort.
The same process is followed whether the contributor is external or another `dbt-greenplum` maintainer.
Once all tests are passing and the PR has been approved by the appropriate code owners,
a `dbt-greenplum` maintainer will merge the changes into `main`.

And that's it! Happy developing :tada:
