from pprint import pprint

import argparse
import logging
import sys

from wekapyutils.wekalogging import configure_logging, register_module
#from wekapyutils.wekassh import RemoteServer, parallel

import wekarestapi
from wekarestapi.rest import ApiException

# get root logger
log = logging.getLogger()

def main():
    # parse arguments
    progname = sys.argv[0]
    parser = argparse.ArgumentParser(description='This is a stub for programs that would use the Weka REST api')

    # example of how to to add a list-type command line argument
    #parser.add_argument('server_ips', metavar='serverips', type=str, nargs='+',
    #                    help='Server DATAPLANE IPs to test')

    # example of how to add a switch-line argument
    #parser.add_argument("-j", "--json", dest='json_flag', action='store_true', help="enable json output mode")

    # these next args are passed to the script and parsed in etc/preamble - this is more for syntax checking
    parser.add_argument("-v", "--verbose", dest='verbosity', action='store_true', help="enable verbose mode")

    args = parser.parse_args()

    # set up logging in a standard way...
    configure_logging(log, args.verbosity)

    # local modules - override a module's logging level
    register_module("my_module", logging.ERROR)

    # make API calls
    config = wekarestapi.Configuration(hostname="vweka01")

    # create an instance of the API class
    api_client = wekarestapi.ApiClient(config)

    try:
        # login to weka system
        api_response = wekarestapi.LoginApi(api_client).login(
            wekarestapi.LoginBody(username="admin", password="Weka.io123", org="root"))
        #    pprint(api_response)
        config.auth_tokens = api_response.data
    except ApiException as e:
        print("Exception when calling LoginApi->login: %s\n" % e)

    try:
        # get alerts
        api_response = wekarestapi.AlertsApi(api_client).get_alerts()
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling AlertsApi->get_alerts: %s\n" % e)

if __name__ == '__main__':
    main()
