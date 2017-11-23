import sys
import os
sys.path.append(os.getcwd())
from tempest.api.workloadmgr import base
from tempest import config
from tempest import test
from oslo_log import log as logging
from tempest import tvaultconf
from tempest import reporting
import time
from tempest import command_argument_string
from tempest.util import cli_parser
from tempest.util import query_data

LOG = logging.getLogger(__name__)
CONF = config.CONF

class WorkloadTest(base.BaseWorkloadmgrTest):

    credentials = ['primary']

    @classmethod
    def setup_clients(cls):
        super(WorkloadTest, cls).setup_clients()
        cls.client = cls.os.wlm_client

    @test.pre_req({'type':'config_backup'})
    @test.attr(type='smoke')
    @test.idempotent_id('72fe87ca-541a-42b0-b83a-1e07a5420603')
    def test_1_config_workload_configure(self):
        reporting.add_test_script(str(__name__) + "_configure")
        try:
            # prerequisite handles config_user creation and config_backup_pvk(private key) creation
            
            # for config backup configuration, yaml_file creation
            self.create_config_backup_yaml()
	    
	    config_workload_id = None

            # config backup configuration with CLI command
            config_workload_command = command_argument_string.config_workload_configure + " --config-file yaml_file.yaml --authorized-key config_backup_pvk "
    
            LOG.debug("config workload configure cli command: " + str(config_workload_command))
    
            rc = cli_parser.cli_returncode(config_workload_command)
            if rc != 0:
                reporting.add_test_step("Triggering config_workload_configure command via CLI", tvaultconf.FAIL)
                raise Exception("Command did not execute correctly")
            else:
                reporting.add_test_step("Triggering config_workload_configure command via CLI", tvaultconf.PASS)
                LOG.debug("Command executed correctly")

	    config_workload_id = query_data.get_config_workload_id()
            LOG.debug("Config workload id: " + str(config_workload_id))

	    if(config_workload_id != None):
                reporting.add_test_step("Config Workload Configure", tvaultconf.PASS)
            else:
                reporting.add_test_step("Config Worklaod Configure", tvaultconf.FAIL)
                reporting.set_test_script_status(tvaultconf.FAIL) 

            reporting.test_case_to_write()

        except Exception as e:
            LOG.error("Exception: " + str(e))
            reporting.set_test_script_status(tvaultconf.FAIL)
            reporting.test_case_to_write()


    @test.attr(type='smoke')
    @test.idempotent_id('ae78e629-1499-451b-b82e-6165b269863d')
    def test_2_config_workload_show(self):
        reporting.add_test_script(str(__name__) + "_show")
        try:
	    # test config_workload_show cli
            config_workload_show_command = command_argument_string.config_workload_show 

            LOG.debug("config workload show cli command: " + str(config_workload_show_command))

            rc = cli_parser.cli_returncode(config_workload_show_command)
            if rc != 0:
                reporting.add_test_step("Triggering config_workload_show_command via CLI", tvaultconf.FAIL)
                raise Exception("Command did not execute correctly")
            else:
                reporting.add_test_step("Triggering config_workload_show_command via CLI", tvaultconf.PASS)
                LOG.debug("Command executed correctly") 

	    config_workload_output = self.get_config_workload()
	    LOG.debug("config_workload_show_command output: " + str(output))

	    config_workload_status = config_workload_output['status']

            if config_workload_status == "available":
                LOG.debug("config_workload status is available, config_workload_id: " + config_workload_output['id'])
                reporting.add_test_step("config_workload status: available", tvaultconf.PASS)
            else:
                LOG.debug("config_workload status is not available, Error msg: " + config_workload_output['error_msg'])
                reporting.add_test_step("config_workload status: " + config_workload_output['status'], tvaultconf.FAIL)
		raise Exception ("Config Workload Configure Failed.")

            reporting.test_case_to_write()

        except Exception as e:
            LOG.error("Exception: " + str(e))
            reporting.set_test_script_status(tvaultconf.FAIL)
            reporting.test_case_to_write()

    test.pre_req({'type':'config_backup'})
    @test.attr(type='smoke')
    @test.idempotent_id('52d14575-e2dd-46bf-b1f2-7c317121fc6e')
    def test_3_config_workload_added_dir(self):
        reporting.add_test_script(str(__name__) + "_additional_dir")
        try: 
	    # prerequisite handles config_user creation and config_backup_pvk(private key) creation

            # for config backup configuration, yaml_file creation
	    added_dir = {'tvault-contego':{'config_dir':['/etc/tvault-contego/']}} 
            self.create_config_backup_yaml(added_dir=added_dir)

            # config backup configuration with CLI command
            config_workload_command = command_argument_string.config_workload_configure + " --config-file yaml_file.yaml --authorized-key config_backup_pvk "

            LOG.debug("config workload configure cli command: " + str(config_workload_command))

            rc = cli_parser.cli_returncode(config_workload_command)
            if rc != 0:
                reporting.add_test_step("Triggering config_workload_configure command via CLI", tvaultconf.FAIL)
                raise Exception("Command did not execute correctly")
            else:
                reporting.add_test_step("Triggering config_workload_configure command via CLI", tvaultconf.PASS)
                LOG.debug("Command executed correctly")
	    
	    config_workload_show_command = command_argument_string.config_workload_show

	    config_workload_output = cli_parser.cli_output(config_workload_show_command)

            LOG.debug("config_workload_show_command output from cli: " + str(config_workload_output))

            if added_dir.keys()[0] in str(config_workload_output):
                LOG.debug("config_workload output with added dir: " + added_dir.keys()[0] + " : "  + str(config_workload_output))
                reporting.add_test_step("config_workload completed with added dir ", tvaultconf.PASS)
            else:
		LOG.debug("config_workload output without added dir: " + added_dir.keys()[0] + " : "  + str(config_workload_output))
		reporting.add_test_step("config_workload completed with added dir ", tvaultconf.FAIL)

            reporting.test_case_to_write()

        except Exception as e:
            LOG.error("Exception: " + str(e))
            reporting.set_test_script_status(tvaultconf.FAIL)
            reporting.test_case_to_write()

