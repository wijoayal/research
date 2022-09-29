#! /usr/bin/env python
import lxml.etree as et
from argparse import ArgumentParser
from ncclient import manager
from ncclient.operations import RPCError

payload = [
'''
<get xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <filter>
    <rib xmlns="http://cisco.com/ns/yang/Cisco-IOS-XR-ip-rib-ipv4-oper">
      <vrfs>
        <vrf>
          <afs>
            <af>
              <safs>
                <saf>
                  <ip-rib-route-table-names>
                    <ip-rib-route-table-name>
                      <protocol>
                        <bgp>
                          <as>
                            <information/>
                          </as>
                        </bgp>
                      </protocol>
                    </ip-rib-route-table-name>
                  </ip-rib-route-table-names>
                </saf>
              </safs>
            </af>
          </afs>
        </vrf>
      </vrfs>
    </rib>
  </filter>
</get>
''',
]

if __name__ == '__main__':

    parser = ArgumentParser(description='Usage:')

    # script arguments
    parser.add_argument('-a', '--host', type=str, required=True,
                        help="Device IP address or Hostname")
    parser.add_argument('-u', '--username', type=str, required=True,
                        help="Device Username (netconf agent username)")
    parser.add_argument('-p', '--password', type=str, required=True,
                        help="Device Password (netconf agent password)")
    parser.add_argument('--port', type=int, default=830,
                        help="Netconf agent port")
    args = parser.parse_args()

    # connect to netconf agent
    with manager.connect(host=args.host,
                         port=args.port,
                         username=args.username,
                         password=args.password,
                         timeout=90,
                         hostkey_verify=False,
                         device_params={'name': 'csr'}) as m:

        # execute netconf operation
        for rpc in payload:
            try:
                response = m.dispatch(et.fromstring(rpc))
                data = response
            except RPCError as e:
                data = e._raw

            # beautify output
            print(data)