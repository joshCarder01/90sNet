# Table of Contents
- [Table of Contents](#table-of-contents)
- [Test Plan](#test-plan)
  - [Infrastructure Tests](#infrastructure-tests)
  - [API Server Tests](#api-server-tests)
- [Test Results](#test-results)
  - [Infrastructre Test Results](#infrastructre-test-results)
  - [API Server Tests](#api-server-tests-1)


# Test Plan

## Infrastructure Tests
<style>
    ol {
    list-style-type: none; /* Remove default numbering */
    }
    ol li {
    begin: inherit;
    counter-increment: my-counter;
    }
    ol li:before {
    content: attr(begin) counter(my-counter) " ";
    }
    ol ol {
    begin: inherit;
    counter-reset: sub-counter;
    }
    ol ol li {
    begin: inherit;
    counter-increment: sub-counter;
    }
    ol ol li:before {
    content: attr(begin) counter(my-counter) "." counter(sub-counter) " ";
    }
</style>
<ol begin="IS">
    <li begin="IS"><strong>Infrastructure Test</strong></br>
    <ol>
    <li begin="IS">Verify infrastructure can connect to docker network</li>
    <li begin="IS">Docker exec command will run and output will be checked to ensure infrastructure can reach contrainers and perform needed actions</li>
    <li begin="IS">Inputs: container name</li>
    <li begin="IS">Outputs: command executed pass/fail</li>
    <li begin="IS">Normal</li>
    <li begin="IS">blackbox</li>
    <li begin="IS">Functional</li>
    <li begin="IS">Unit</li></ol>
    </li>
    <li begin="IS">
        <strong>Infrastructure Test</strong>
            <ol>
            <li begin="IS">Verify directories are monitored</li>
            <li begin="IS">directory will be modified using docker exec command, and event stream will be monitored to ensure modification was seen</li>
            <li begin="IS">Inputs: path</li>
            <li begin="IS">Outputs: event seen pass/fail</li>
            <li begin="IS">Normal</li>
            <li begin="IS">blackbox</li>
            <li begin="IS">Functional</li>
            <li begin="IS">Unit</li>
            </ol>
    </li>
    <li begin="IS">
        <strong>Infrastructure Test</strong>
            <ol>
            <li begin="IS">Verify files are monitored</li>
            <li begin="IS">file will be modified using docker exec command, and event stream will be monitored to ensure modification was seen</li>
            <li begin="IS">Inputs: path</li>
            <li begin="IS">Outputs: event seen pass/fail</li>
            <li begin="IS">Normal</li>
            <li begin="IS">blackbox</li>
            <li begin="IS">Functional</li>
            <li begin="IS">Unit</li>
            </ol>
    </li>
    <li begin="IS">
        <strong>Infrastructure Test</strong>
            <ol>
            <li begin="IS">Verify manager responds to commands</li>
            <li begin="IS">Command will be sent to network manager and will wait until response if found</li>
            <li begin="IS">Inputs: command</li>
            <li begin="IS">Outputs: command fulfiilled pass/fail</li>
            <li begin="IS">Normal</li>
            <li begin="IS">blackbox</li>
            <li begin="IS">Functional</li>
            <li begin="IS">Unit</li>
            </ol>
    </li>
    <li begin="IS">
        <strong>Infrastructure Test</strong>
            <ol>
            <li begin="IS">Adversaries take action</li>
            <li begin="IS">Actions for a preprogrammed adversary trigger will be executed and will wait until expected response is detected directly</li>
            <li begin="IS">Inputs: actions</li>
            <li begin="IS">Outputs: response seen pass/fail</li>
            <li begin="IS">Normal</li>
            <li begin="IS">blackbox</li>
            <li begin="IS">Functional</li>
            <li begin="IS">Unit</li>
            </ol>
    </li>
</ol>

## API Server Tests
<ol>
	<li begin="AS">
	<strong>API Server Test</strong>
		<ol>
			<li begin="AS">Command API Transaction</li>
			<li begin="AS">Sending Commands and results to the server and getting the same should be in order and keep track of what is happening</li>
			<li begin="AS">Inputs: test commands and results</li>
			<li begin="AS">Outputs: response seen pass/fail</li>
			<li begin="AS">Normal</li>
			<li begin="AS">blackbox</li>
			<li begin="AS">Functional</li>
			<li begin="AS">Unit</li>
		</ol>
	</li>
	<li begin='AS'>
	<strong>API Server Test</strong>
		<ol>
			<li begin='AS'>Command API Blank</li>
			<li begin='AS'>Command Has Determined Response When No Data in Queue</li>
			<li begin='AS'>Inputs: empty command queue</li>
			<li begin='AS'>Outputs: response seen pass/fail</li>
			<li begin='AS'>Normal</li>
			<li begin='AS'>whitebox</li>
			<li begin='AS'>Functional</li>
			<li begin='AS'>Unit</li>
		</ol>
	</li>
	<li begin="AS">
	<strong>API Server Test</strong>
		<ol>
			<li begin='AS'>Get Events</li>
			<li begin='AS'>Get Seeded Event Data</li>
			<li begin='AS'>Inputs: test seed data</li>
			<li begin='AS'>Outputs: response seen pass/fail</li>
			<li begin='AS'>Normal</li>
			<li begin='AS'>whitebox</li>
			<li begin='AS'>Functional</li>
			<li begin='AS'>Unit</li>
		</ol>
	</li>
	<li begin="AS">
	<strong>API Server Test</strong>
		<ol>
			<li begin='AS'>Get Events Since</li>
			<li begin='AS'>Test Seeded Events After Certain Time</li>
			<li begin='AS'>Inputs: test seed data</li>
			<li begin='AS'>Outputs: response seen pass/fail</li>
			<li begin='AS'>Normal</li>
			<li begin='AS'>whitebox</li>
			<li begin='AS'>Functional</li>
			<li begin='AS'>Unit</li>
		</ol>
	</li>
	<li begin="AS">
	<strong>API Server Test</strong>
		<ol>
			<li begin='AS'>Post Event</li>
			<li begin='AS'>Ensure Posted Event is added to Database</li>
			<li begin='AS'>Inputs: test event</li>
			<li begin='AS'>Outputs: response seen pass/fail</li>
			<li begin='AS'>Normal</li>
			<li begin='AS'>whitebox</li>
			<li begin='AS'>Functional</li>
			<li begin='AS'>Unit</li>
		</ol>
	</li>
	<li begin='AS'>
	<strong>API Server Test</strong>
		<ol>
			<li begin='AS'>Get All Machines</li>
			<li begin='AS'>Ensure API Get All Machines</li>
			<li begin='AS'>Inputs: seeded machines test data</li>
			<li begin='AS'>Outputs: response seen pass/fail</li>
			<li begin='AS'>Normal</li>
			<li begin='AS'>whitebox</li>
			<li begin='AS'>Functional</li>
			<li begin='AS'>Unit</li>
		</ol>
	</li>
	<li begin='AS'>
	<strong>API Server Test</strong>
		<ol>
			<li begin='AS'>Post Machine</li>
			<li begin='AS'>Ensure API Post Machine</li>
			<li begin='AS'>Inputs: test machine data</li>
			<li begin='AS'>Outputs: response seen pass/fail</li>
			<li begin='AS'>Normal</li>
			<li begin='AS'>whitebox</li>
			<li begin='AS'>Functional</li>
			<li begin='AS'>Unit</li>
		</ol>
	</li>
	<li begin='AS'>
	<strong>API Server Test</strong>
		<ol>
			<li begin='AS'>Get All Users</li>
			<li begin='AS'>Get All Seeded User Data</li>
			<li begin='AS'>Inputs: seeded user data</li>
			<li begin='AS'>Outputs: response seen pass/fail</li>
			<li begin='AS'>Normal</li>
			<li begin='AS'>whitebox</li>
			<li begin='AS'>Functional</li>
			<li begin='AS'>Unit</li>
		</ol>
	</li>
	<li begin='AS'>
	<strong>API Server Test</strong>
		<ol>
			<li begin='AS'>Post User</li>
			<li begin='AS'>Post User Data To Server Ensure It Shows Up On DB</li>
			<li begin='AS'>Inputs: test user data</li>
			<li begin='AS'>Outputs: response seen pass/fail</li>
			<li begin='AS'>Normal</li>
			<li begin='AS'>whitebox</li>
			<li begin='AS'>Functional</li>
			<li begin='AS'>Unit</li>
		</ol>
	</li>
</ol>
</div>

# Test Results
## Infrastructre Test Results
```sh
UnitTesting $ python test.py
IS0: connect_docker             [PASS]
IS1: monitor_dir                [PASS]
IS2: monitor_file               [PASS]
IS3: manager_reply              [PASS]
IS4: adversary_action           [PASS]
```
## API Server Tests
```sh
$ docker compose exec -t flask_app python -m pytest -v
=============================== test session starts ================================
platform linux -- Python 3.11.8, pytest-8.0.0, pluggy-1.4.0 -- /usr/local/bin/python
cachedir: .pytest_cache
rootdir: /app
plugins: mock-3.14.0
collected 9 items                                                                  

tests/functional/test_commands.py::test_AS1_command_blank PASSED             [ 11%]
tests/functional/test_commands.py::test_AS2_command_transaction PASSED       [ 22%]
tests/functional/test_events.py::test_AS3_events_get_all PASSED              [ 33%]
tests/functional/test_events.py::test_AS4_events_get_since PASSED            [ 44%]
tests/functional/test_events.py::test_AS5_events_post PASSED                 [ 55%]
tests/functional/test_machine.py::test_AS6_machines_get_all PASSED           [ 66%]
tests/functional/test_machine.py::test_AS7_machines_post PASSED              [ 77%]
tests/functional/test_users.py::test_AS8_users_get_all PASSED                [ 88%]
tests/functional/test_users.py::test_AS9_users_post PASSED                   [100%]

================================ 9 passed in 0.20s =================================

```
