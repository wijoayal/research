import logging
from datetime import datetime
from fastapi import FastAPI
from fastapi_utils.tasks import repeat_every
import time
from app.db import mongodb
import subprocess
from app.core.logging_instance import init_logging

init_logging()
logger = logging.getLogger(__name__)
app = FastAPI()

router_id_1 ='1.1.1.1'
router_id_2 ='1.1.1.2'
router_id_3 ='1.1.1.3'
router_id_4 ='1.1.1.4'
router_name_2 = 'T-GYE'
router_name_1 = 'T-UIO'
router_name_4 = 'T-CUE'
router_name_3 = 'T-ESM'

@app.on_event("startup")
@repeat_every(seconds=5, logger=logger) 
async def get_all_data1():
    router_id = router_id_1
    router_name = router_name_1

    try:
        content = subprocess.run([
            'python3',
            '/app/core/sc2_rib.py',
            '-a',
            router_id,
            '-u',
            'cisco',
            '-p',
            'cisco'
        ], capture_output=True, timeout=5)
        content = str(content.stdout)
    except Exception as e:
        print(e)
        content = ''
    finally:
        answer = content
        if '</active-routes-count>' in answer:

            active_routes_count = answer.split('</active-routes-count>')[0].split('<active-routes-count>')[1]
            backup_routes_count = answer.split('</backup-routes-count>')[0].split('<backup-routes-count>')[1]
            deleted_routes_count = answer.split('</deleted-routes-count>')[0].split('<deleted-routes-count>')[1]
            paths_count = answer.split('</paths-count>')[0].split('<paths-count>')[1]
            protocol_route_memory = answer.split('</protocol-route-memory>')[0].split('<protocol-route-memory>')[1]
            af_name = answer.split('</af-name>')[0].split('<af-name>')[1]
            as_number = answer.split('</as>')[0].split('<as>')[1]
            route_table_name = answer.split('</route-table-name>')[0].split('<route-table-name>')[1]
            routes_counts = answer.split('</routes-counts>')[0].split('<routes-counts>')[1]

            mongodb.collection_routers.update_one(
                {'router_id':router_id},
                {'$set': {
                    'rib':{
                        'active_routes_count' : active_routes_count,
                        'backup_routes_count' : backup_routes_count,
                        'deleted_routes_count' : deleted_routes_count,
                        'paths_count' : paths_count,
                        'protocol_route_memory' : protocol_route_memory,
                        'af_name' : af_name,
                        'as_number' : as_number,
                        'route_table_name' : route_table_name,
                        'routes_counts' : routes_counts
                    },
                    'date_modified' : datetime.now()
                }}, upsert = True
            )
        else:
            mongodb.collection_routers.update_one(
                {'router_id':router_id},
                {'$set': {
                    'rib':{
                        'active_routes_count' : 0,
                        'backup_routes_count' : 0,
                        'deleted_routes_count' : 0,
                        'paths_count' : 0,
                        'protocol_route_memory' : 0,
                        'af_name' : None,
                        'as_number' : None,
                        'route_table_name' : None,
                        'routes_counts' : 0
                    },
                    'date_modified' : datetime.now()
                }}, upsert = True
            )
 
    try:
        content = subprocess.run([
            'python3',
            '/app/core/sc4_fib.py',
            '-a',
            router_id,
            '-u',
            'cisco',
            '-p',
            'cisco'
        ], capture_output=True, timeout=5)
        content = str(content.stdout)
    except Exception as e:
        print(e)
        content = ''
    finally:
        answer = content
    # print(answer, type(answer))
        if '</node-name>' in answer:
            node_name = answer.split('</node-name>')[0].split('<node-name>')[1]
            punt_unreachable_packets = answer.split('</punt-unreachable-packets>')[0].split('<punt-unreachable-packets>')[1]
            df_unreachable_packets = answer.split('</df-unreachable-packets>')[0].split('<df-unreachable-packets>')[1]
            encapsulation_failure_packets = answer.split('</encapsulation-failure-packets>')[0].split('<encapsulation-failure-packets>')[1]
            incomplete_adjacency_packets = answer.split('</incomplete-adjacency-packets>')[0].split('<incomplete-adjacency-packets>')[1]
            unresolved_prefix_packets = answer.split('</unresolved-prefix-packets>')[0].split('<unresolved-prefix-packets>')[1]
            unsupported_feature_packets = answer.split('</unsupported-feature-packets>')[0].split('<unsupported-feature-packets>')[1]
            discard_packets = answer.split('</discard-packets>')[0].split('<discard-packets>')[1]
            checksum_error_packets = answer.split('</checksum-error-packets>')[0].split('<checksum-error-packets>')[1]
            fragmenation_consumed_packets = answer.split('</fragmenation-consumed-packets>')[0].split('<fragmenation-consumed-packets>')[1]
            null_packets = answer.split('</null-packets>')[0].split('<null-packets>')[1]
            rpf_check_failure_packets = answer.split('</rpf-check-failure-packets>')[0].split('<rpf-check-failure-packets>')[1]
            rp_destination_drop_packets = answer.split('</rp-destination-drop-packets>')[0].split('<rp-destination-drop-packets>')[1]
            total_number_of_drop_packets = answer.split('</total-number-of-drop-packets>')[0].split('<total-number-of-drop-packets>')[1]
            total_number_of_drop_packets = answer.split('</total-number-of-drop-packets>')[0].split('<total-number-of-drop-packets>')[1]
            mpls_disabled_interface = answer.split('</mpls-disabled-interface>')[0].split('<mpls-disabled-interface>')[1]
            gre_lookup_failed_drop = answer.split('</gre-lookup-failed-drop>')[0].split('<gre-lookup-failed-drop>')[1]
            gre_error_drop = answer.split('</gre-error-drop>')[0].split('<gre-error-drop>')[1]
            lisp_punt_drops = answer.split('</lisp-punt-drops>')[0].split('<lisp-punt-drops>')[1]
            lisp_encap_error_drops = answer.split('</lisp-encap-error-drops>')[0].split('<lisp-encap-error-drops>')[1]
            lisp_decap_error_drops = answer.split('</lisp-decap-error-drops>')[0].split('<lisp-decap-error-drops>')[1]
            multi_label_drops = answer.split('</multi-label-drops>')[0].split('<multi-label-drops>')[1]
            no_route_packets = answer.split('</no-route-packets>')[0].split('<no-route-packets>')[1]

            mongodb.collection_routers.update_one(
                {'router_id':router_id},
                {'$set': {
                    'fib':{
                        'node_name' : node_name,
                        'punt_unreachable_packets' : punt_unreachable_packets,
                        'df_unreachable_packets' : df_unreachable_packets,
                        'encapsulation_failure_packets' : encapsulation_failure_packets,
                        'incomplete_adjacency_packets' : incomplete_adjacency_packets,
                        'unresolved_prefix_packets' : unresolved_prefix_packets,
                        'unsupported_feature_packets' : unsupported_feature_packets,
                        'discard_packets' : discard_packets,
                        'checksum_error_packets' : checksum_error_packets,
                        'fragmenation_consumed_packets' : fragmenation_consumed_packets,
                        'null_packets' : null_packets,
                        'rpf_check_failure_packets' : rpf_check_failure_packets,
                        'rp_destination_drop_packets' : rp_destination_drop_packets,
                        'total_number_of_drop_packets' : total_number_of_drop_packets,
                        'total_number_of_drop_packets' : total_number_of_drop_packets,
                        'mpls_disabled_interface' : mpls_disabled_interface,
                        'gre_lookup_failed_drop' : gre_lookup_failed_drop,
                        'gre_error_drop' : gre_error_drop,
                        'lisp_punt_drops' : lisp_punt_drops,
                        'lisp_encap_error_drops' : lisp_encap_error_drops,
                        'lisp_decap_error_drops' : lisp_decap_error_drops,
                        'multi_label_drops' : multi_label_drops,
                        'no_route_packets' : no_route_packets
                    },
                    'date_modified' : datetime.now()
                }}, upsert = True
            )
        else:
            mongodb.collection_routers.update_one(
                {'router_id':router_id},
                {'$set': {
                    'fib':{
                        'node_name' : None,
                        'punt_unreachable_packets' : 0,
                        'df_unreachable_packets' : 0,
                        'encapsulation_failure_packets' : 0,
                        'incomplete_adjacency_packets' : 0,
                        'unresolved_prefix_packets' : 0,
                        'unsupported_feature_packets' : 0,
                        'discard_packets' : 0,
                        'checksum_error_packets' : 0,
                        'fragmenation_consumed_packets' : 0,
                        'null_packets' : 0,
                        'rpf_check_failure_packets' : 0,
                        'rp_destination_drop_packets' : 0,
                        'total_number_of_drop_packets' : 0,
                        'total_number_of_drop_packets' : 0,
                        'mpls_disabled_interface' : 0,
                        'gre_lookup_failed_drop' : 0,
                        'gre_error_drop' : 0,
                        'lisp_punt_drops' : 0,
                        'lisp_encap_error_drops' : 0,
                        'lisp_decap_error_drops' : 0,
                        'multi_label_drops' : 0,
                        'no_route_packets' : 0
                    },
                    'date_modified' : datetime.now()
                }}, upsert = True
            )
    try:
        content = subprocess.run([
            'python3',
            '/app/core/sc1_open.py',
            '-a',
            router_id,
            '-u',
            'cisco',
            '-p',
            'cisco'
        ], capture_output=True, timeout=5)
        content = str(content.stdout)
    except Exception as e:
        print(e)
        content = ''
    finally:
        answer = content
        if '</as>' in answer:
            as_number = answer.split('</as>')[0].split('<as>')[1]
            total_paths = answer.split('</total-paths>')[0].split('<total-paths>')[1]
            total_prefixes = answer.split('</total-prefixes>')[0].split('<total-prefixes>')[1]
            mongodb.collection_routers.update_one(
                {'router_id':router_id},
                {'$set': {
                    'router_name': router_name,
                    'as_number' : as_number,
                    'total_prefixes' : total_prefixes,
                    'total_paths' : total_paths,
                    'date_modified' : datetime.now()
                }}, upsert = True
            )
        else:
            mongodb.collection_routers.update_one(
                {'router_id':router_id},
                {'$set': {
                    'router_name': router_name,
                    'as_number' : None,
                    'total_prefixes' : None,
                    'total_paths' : None,
                    'date_modified' : datetime.now()
                }}, upsert = True
            )    

@app.on_event("startup")
@repeat_every(seconds=5, logger=logger) 
async def get_all_data2():
    router_id = router_id_2
    router_name = router_name_2
    try:
        content = subprocess.run([
            'python3',
            '/app/core/sc2_rib.py',
            '-a',
            router_id,
            '-u',
            'cisco',
            '-p',
            'cisco'
        ], capture_output=True, timeout=5)
        content = str(content.stdout)
    except Exception as e:
        print(e)
        content = ''
    finally:
        answer = content
        if '</active-routes-count>' in answer:

            active_routes_count = answer.split('</active-routes-count>')[0].split('<active-routes-count>')[1]
            backup_routes_count = answer.split('</backup-routes-count>')[0].split('<backup-routes-count>')[1]
            deleted_routes_count = answer.split('</deleted-routes-count>')[0].split('<deleted-routes-count>')[1]
            paths_count = answer.split('</paths-count>')[0].split('<paths-count>')[1]
            protocol_route_memory = answer.split('</protocol-route-memory>')[0].split('<protocol-route-memory>')[1]
            af_name = answer.split('</af-name>')[0].split('<af-name>')[1]
            as_number = answer.split('</as>')[0].split('<as>')[1]
            route_table_name = answer.split('</route-table-name>')[0].split('<route-table-name>')[1]
            routes_counts = answer.split('</routes-counts>')[0].split('<routes-counts>')[1]

            mongodb.collection_routers.update_one(
                {'router_id':router_id},
                {'$set': {
                    'rib':{
                        'active_routes_count' : active_routes_count,
                        'backup_routes_count' : backup_routes_count,
                        'deleted_routes_count' : deleted_routes_count,
                        'paths_count' : paths_count,
                        'protocol_route_memory' : protocol_route_memory,
                        'af_name' : af_name,
                        'as_number' : as_number,
                        'route_table_name' : route_table_name,
                        'routes_counts' : routes_counts
                    },
                    'date_modified' : datetime.now()
                }}, upsert = True
            )
        else:
            mongodb.collection_routers.update_one(
                {'router_id':router_id},
                {'$set': {
                    'rib':{
                        'active_routes_count' : 0,
                        'backup_routes_count' : 0,
                        'deleted_routes_count' : 0,
                        'paths_count' : 0,
                        'protocol_route_memory' : 0,
                        'af_name' : None,
                        'as_number' : None,
                        'route_table_name' : None,
                        'routes_counts' : 0
                    },
                    'date_modified' : datetime.now()
                }}, upsert = True
            )
 
    try:
        content = subprocess.run([
            'python3',
            '/app/core/sc4_fib.py',
            '-a',
            router_id,
            '-u',
            'cisco',
            '-p',
            'cisco'
        ], capture_output=True, timeout=5)
        content = str(content.stdout)
    except Exception as e:
        print(e)
        content = ''
    finally:
        answer = content
    # print(answer, type(answer))
        if '</node-name>' in answer:
            node_name = answer.split('</node-name>')[0].split('<node-name>')[1]
            punt_unreachable_packets = answer.split('</punt-unreachable-packets>')[0].split('<punt-unreachable-packets>')[1]
            df_unreachable_packets = answer.split('</df-unreachable-packets>')[0].split('<df-unreachable-packets>')[1]
            encapsulation_failure_packets = answer.split('</encapsulation-failure-packets>')[0].split('<encapsulation-failure-packets>')[1]
            incomplete_adjacency_packets = answer.split('</incomplete-adjacency-packets>')[0].split('<incomplete-adjacency-packets>')[1]
            unresolved_prefix_packets = answer.split('</unresolved-prefix-packets>')[0].split('<unresolved-prefix-packets>')[1]
            unsupported_feature_packets = answer.split('</unsupported-feature-packets>')[0].split('<unsupported-feature-packets>')[1]
            discard_packets = answer.split('</discard-packets>')[0].split('<discard-packets>')[1]
            checksum_error_packets = answer.split('</checksum-error-packets>')[0].split('<checksum-error-packets>')[1]
            fragmenation_consumed_packets = answer.split('</fragmenation-consumed-packets>')[0].split('<fragmenation-consumed-packets>')[1]
            null_packets = answer.split('</null-packets>')[0].split('<null-packets>')[1]
            rpf_check_failure_packets = answer.split('</rpf-check-failure-packets>')[0].split('<rpf-check-failure-packets>')[1]
            rp_destination_drop_packets = answer.split('</rp-destination-drop-packets>')[0].split('<rp-destination-drop-packets>')[1]
            total_number_of_drop_packets = answer.split('</total-number-of-drop-packets>')[0].split('<total-number-of-drop-packets>')[1]
            total_number_of_drop_packets = answer.split('</total-number-of-drop-packets>')[0].split('<total-number-of-drop-packets>')[1]
            mpls_disabled_interface = answer.split('</mpls-disabled-interface>')[0].split('<mpls-disabled-interface>')[1]
            gre_lookup_failed_drop = answer.split('</gre-lookup-failed-drop>')[0].split('<gre-lookup-failed-drop>')[1]
            gre_error_drop = answer.split('</gre-error-drop>')[0].split('<gre-error-drop>')[1]
            lisp_punt_drops = answer.split('</lisp-punt-drops>')[0].split('<lisp-punt-drops>')[1]
            lisp_encap_error_drops = answer.split('</lisp-encap-error-drops>')[0].split('<lisp-encap-error-drops>')[1]
            lisp_decap_error_drops = answer.split('</lisp-decap-error-drops>')[0].split('<lisp-decap-error-drops>')[1]
            multi_label_drops = answer.split('</multi-label-drops>')[0].split('<multi-label-drops>')[1]
            no_route_packets = answer.split('</no-route-packets>')[0].split('<no-route-packets>')[1]

            mongodb.collection_routers.update_one(
                {'router_id':router_id},
                {'$set': {
                    'fib':{
                        'node_name' : node_name,
                        'punt_unreachable_packets' : punt_unreachable_packets,
                        'df_unreachable_packets' : df_unreachable_packets,
                        'encapsulation_failure_packets' : encapsulation_failure_packets,
                        'incomplete_adjacency_packets' : incomplete_adjacency_packets,
                        'unresolved_prefix_packets' : unresolved_prefix_packets,
                        'unsupported_feature_packets' : unsupported_feature_packets,
                        'discard_packets' : discard_packets,
                        'checksum_error_packets' : checksum_error_packets,
                        'fragmenation_consumed_packets' : fragmenation_consumed_packets,
                        'null_packets' : null_packets,
                        'rpf_check_failure_packets' : rpf_check_failure_packets,
                        'rp_destination_drop_packets' : rp_destination_drop_packets,
                        'total_number_of_drop_packets' : total_number_of_drop_packets,
                        'total_number_of_drop_packets' : total_number_of_drop_packets,
                        'mpls_disabled_interface' : mpls_disabled_interface,
                        'gre_lookup_failed_drop' : gre_lookup_failed_drop,
                        'gre_error_drop' : gre_error_drop,
                        'lisp_punt_drops' : lisp_punt_drops,
                        'lisp_encap_error_drops' : lisp_encap_error_drops,
                        'lisp_decap_error_drops' : lisp_decap_error_drops,
                        'multi_label_drops' : multi_label_drops,
                        'no_route_packets' : no_route_packets
                    },
                    'date_modified' : datetime.now()
                }}, upsert = True
            )
        else:
            mongodb.collection_routers.update_one(
                {'router_id':router_id},
                {'$set': {
                    'fib':{
                        'node_name' : None,
                        'punt_unreachable_packets' : 0,
                        'df_unreachable_packets' : 0,
                        'encapsulation_failure_packets' : 0,
                        'incomplete_adjacency_packets' : 0,
                        'unresolved_prefix_packets' : 0,
                        'unsupported_feature_packets' : 0,
                        'discard_packets' : 0,
                        'checksum_error_packets' : 0,
                        'fragmenation_consumed_packets' : 0,
                        'null_packets' : 0,
                        'rpf_check_failure_packets' : 0,
                        'rp_destination_drop_packets' : 0,
                        'total_number_of_drop_packets' : 0,
                        'total_number_of_drop_packets' : 0,
                        'mpls_disabled_interface' : 0,
                        'gre_lookup_failed_drop' : 0,
                        'gre_error_drop' : 0,
                        'lisp_punt_drops' : 0,
                        'lisp_encap_error_drops' : 0,
                        'lisp_decap_error_drops' : 0,
                        'multi_label_drops' : 0,
                        'no_route_packets' : 0
                    },
                    'date_modified' : datetime.now()
                }}, upsert = True
            )
    try:
        content = subprocess.run([
            'python3',
            '/app/core/sc1_open.py',
            '-a',
            router_id,
            '-u',
            'cisco',
            '-p',
            'cisco'
        ], capture_output=True, timeout=5)
        content = str(content.stdout)
    except Exception as e:
        print(e)
        content = ''
    finally:
        answer = content
        if '</as>' in answer:
            as_number = answer.split('</as>')[0].split('<as>')[1]
            total_paths = answer.split('</total-paths>')[0].split('<total-paths>')[1]
            total_prefixes = answer.split('</total-prefixes>')[0].split('<total-prefixes>')[1]
            mongodb.collection_routers.update_one(
                {'router_id':router_id},
                {'$set': {
                    'router_name': router_name,
                    'as_number' : as_number,
                    'total_prefixes' : total_prefixes,
                    'total_paths' : total_paths,
                    'date_modified' : datetime.now()
                }}, upsert = True
            )
        else:
            mongodb.collection_routers.update_one(
                {'router_id':router_id},
                {'$set': {
                    'router_name': router_name,
                    'as_number' : None,
                    'total_prefixes' : None,
                    'total_paths' : None,
                    'date_modified' : datetime.now()
                }}, upsert = True
            ) 

@app.on_event("startup")
@repeat_every(seconds=5, logger=logger) 
async def get_all_data3():
    router_id = router_id_3
    router_name = router_name_3
    try:
        content = subprocess.run([
            'python3',
            '/app/core/sc2_rib.py',
            '-a',
            router_id,
            '-u',
            'cisco',
            '-p',
            'cisco'
        ], capture_output=True, timeout=5)
        content = str(content.stdout)
    except Exception as e:
        print(e)
        content = ''
    finally:
        answer = content
        if '</active-routes-count>' in answer:

            active_routes_count = answer.split('</active-routes-count>')[0].split('<active-routes-count>')[1]
            backup_routes_count = answer.split('</backup-routes-count>')[0].split('<backup-routes-count>')[1]
            deleted_routes_count = answer.split('</deleted-routes-count>')[0].split('<deleted-routes-count>')[1]
            paths_count = answer.split('</paths-count>')[0].split('<paths-count>')[1]
            protocol_route_memory = answer.split('</protocol-route-memory>')[0].split('<protocol-route-memory>')[1]
            af_name = answer.split('</af-name>')[0].split('<af-name>')[1]
            as_number = answer.split('</as>')[0].split('<as>')[1]
            route_table_name = answer.split('</route-table-name>')[0].split('<route-table-name>')[1]
            routes_counts = answer.split('</routes-counts>')[0].split('<routes-counts>')[1]

            mongodb.collection_routers.update_one(
                {'router_id':router_id},
                {'$set': {
                    'rib':{
                        'active_routes_count' : active_routes_count,
                        'backup_routes_count' : backup_routes_count,
                        'deleted_routes_count' : deleted_routes_count,
                        'paths_count' : paths_count,
                        'protocol_route_memory' : protocol_route_memory,
                        'af_name' : af_name,
                        'as_number' : as_number,
                        'route_table_name' : route_table_name,
                        'routes_counts' : routes_counts
                    },
                    'date_modified' : datetime.now()
                }}, upsert = True
            )
        else:
            mongodb.collection_routers.update_one(
                {'router_id':router_id},
                {'$set': {
                    'rib':{
                        'active_routes_count' : 0,
                        'backup_routes_count' : 0,
                        'deleted_routes_count' : 0,
                        'paths_count' : 0,
                        'protocol_route_memory' : 0,
                        'af_name' : None,
                        'as_number' : None,
                        'route_table_name' : None,
                        'routes_counts' : 0
                    },
                    'date_modified' : datetime.now()
                }}, upsert = True
            )
 
    try:
        content = subprocess.run([
            'python3',
            '/app/core/sc4_fib.py',
            '-a',
            router_id,
            '-u',
            'cisco',
            '-p',
            'cisco'
        ], capture_output=True, timeout=5)
        content = str(content.stdout)
    except Exception as e:
        print(e)
        content = ''
    finally:
        answer = content
    # print(answer, type(answer))
        if '</node-name>' in answer:
            node_name = answer.split('</node-name>')[0].split('<node-name>')[1]
            punt_unreachable_packets = answer.split('</punt-unreachable-packets>')[0].split('<punt-unreachable-packets>')[1]
            df_unreachable_packets = answer.split('</df-unreachable-packets>')[0].split('<df-unreachable-packets>')[1]
            encapsulation_failure_packets = answer.split('</encapsulation-failure-packets>')[0].split('<encapsulation-failure-packets>')[1]
            incomplete_adjacency_packets = answer.split('</incomplete-adjacency-packets>')[0].split('<incomplete-adjacency-packets>')[1]
            unresolved_prefix_packets = answer.split('</unresolved-prefix-packets>')[0].split('<unresolved-prefix-packets>')[1]
            unsupported_feature_packets = answer.split('</unsupported-feature-packets>')[0].split('<unsupported-feature-packets>')[1]
            discard_packets = answer.split('</discard-packets>')[0].split('<discard-packets>')[1]
            checksum_error_packets = answer.split('</checksum-error-packets>')[0].split('<checksum-error-packets>')[1]
            fragmenation_consumed_packets = answer.split('</fragmenation-consumed-packets>')[0].split('<fragmenation-consumed-packets>')[1]
            null_packets = answer.split('</null-packets>')[0].split('<null-packets>')[1]
            rpf_check_failure_packets = answer.split('</rpf-check-failure-packets>')[0].split('<rpf-check-failure-packets>')[1]
            rp_destination_drop_packets = answer.split('</rp-destination-drop-packets>')[0].split('<rp-destination-drop-packets>')[1]
            total_number_of_drop_packets = answer.split('</total-number-of-drop-packets>')[0].split('<total-number-of-drop-packets>')[1]
            total_number_of_drop_packets = answer.split('</total-number-of-drop-packets>')[0].split('<total-number-of-drop-packets>')[1]
            mpls_disabled_interface = answer.split('</mpls-disabled-interface>')[0].split('<mpls-disabled-interface>')[1]
            gre_lookup_failed_drop = answer.split('</gre-lookup-failed-drop>')[0].split('<gre-lookup-failed-drop>')[1]
            gre_error_drop = answer.split('</gre-error-drop>')[0].split('<gre-error-drop>')[1]
            lisp_punt_drops = answer.split('</lisp-punt-drops>')[0].split('<lisp-punt-drops>')[1]
            lisp_encap_error_drops = answer.split('</lisp-encap-error-drops>')[0].split('<lisp-encap-error-drops>')[1]
            lisp_decap_error_drops = answer.split('</lisp-decap-error-drops>')[0].split('<lisp-decap-error-drops>')[1]
            multi_label_drops = answer.split('</multi-label-drops>')[0].split('<multi-label-drops>')[1]
            no_route_packets = answer.split('</no-route-packets>')[0].split('<no-route-packets>')[1]

            mongodb.collection_routers.update_one(
                {'router_id':router_id},
                {'$set': {
                    'fib':{
                        'node_name' : node_name,
                        'punt_unreachable_packets' : punt_unreachable_packets,
                        'df_unreachable_packets' : df_unreachable_packets,
                        'encapsulation_failure_packets' : encapsulation_failure_packets,
                        'incomplete_adjacency_packets' : incomplete_adjacency_packets,
                        'unresolved_prefix_packets' : unresolved_prefix_packets,
                        'unsupported_feature_packets' : unsupported_feature_packets,
                        'discard_packets' : discard_packets,
                        'checksum_error_packets' : checksum_error_packets,
                        'fragmenation_consumed_packets' : fragmenation_consumed_packets,
                        'null_packets' : null_packets,
                        'rpf_check_failure_packets' : rpf_check_failure_packets,
                        'rp_destination_drop_packets' : rp_destination_drop_packets,
                        'total_number_of_drop_packets' : total_number_of_drop_packets,
                        'total_number_of_drop_packets' : total_number_of_drop_packets,
                        'mpls_disabled_interface' : mpls_disabled_interface,
                        'gre_lookup_failed_drop' : gre_lookup_failed_drop,
                        'gre_error_drop' : gre_error_drop,
                        'lisp_punt_drops' : lisp_punt_drops,
                        'lisp_encap_error_drops' : lisp_encap_error_drops,
                        'lisp_decap_error_drops' : lisp_decap_error_drops,
                        'multi_label_drops' : multi_label_drops,
                        'no_route_packets' : no_route_packets
                    },
                    'date_modified' : datetime.now()
                }}, upsert = True
            )
        else:
            mongodb.collection_routers.update_one(
                {'router_id':router_id},
                {'$set': {
                    'fib':{
                        'node_name' : None,
                        'punt_unreachable_packets' : 0,
                        'df_unreachable_packets' : 0,
                        'encapsulation_failure_packets' : 0,
                        'incomplete_adjacency_packets' : 0,
                        'unresolved_prefix_packets' : 0,
                        'unsupported_feature_packets' : 0,
                        'discard_packets' : 0,
                        'checksum_error_packets' : 0,
                        'fragmenation_consumed_packets' : 0,
                        'null_packets' : 0,
                        'rpf_check_failure_packets' : 0,
                        'rp_destination_drop_packets' : 0,
                        'total_number_of_drop_packets' : 0,
                        'total_number_of_drop_packets' : 0,
                        'mpls_disabled_interface' : 0,
                        'gre_lookup_failed_drop' : 0,
                        'gre_error_drop' : 0,
                        'lisp_punt_drops' : 0,
                        'lisp_encap_error_drops' : 0,
                        'lisp_decap_error_drops' : 0,
                        'multi_label_drops' : 0,
                        'no_route_packets' : 0
                    },
                    'date_modified' : datetime.now()
                }}, upsert = True
            )
    try:
        content = subprocess.run([
            'python3',
            '/app/core/sc1_open.py',
            '-a',
            router_id,
            '-u',
            'cisco',
            '-p',
            'cisco'
        ], capture_output=True, timeout=5)
        content = str(content.stdout)
    except Exception as e:
        print(e)
        content = ''
    finally:
        answer = content
        if '</as>' in answer:
            as_number = answer.split('</as>')[0].split('<as>')[1]
            total_paths = answer.split('</total-paths>')[0].split('<total-paths>')[1]
            total_prefixes = answer.split('</total-prefixes>')[0].split('<total-prefixes>')[1]
            mongodb.collection_routers.update_one(
                {'router_id':router_id},
                {'$set': {
                    'router_name': router_name,
                    'as_number' : as_number,
                    'total_prefixes' : total_prefixes,
                    'total_paths' : total_paths,
                    'date_modified' : datetime.now()
                }}, upsert = True
            )
        else:
            mongodb.collection_routers.update_one(
                {'router_id':router_id},
                {'$set': {
                    'router_name': router_name,
                    'as_number' : None,
                    'total_prefixes' : None,
                    'total_paths' : None,
                    'date_modified' : datetime.now()
                }}, upsert = True
            ) 

@app.on_event("startup")
@repeat_every(seconds=5, logger=logger) 
async def get_all_data4():
    router_id = router_id_4
    router_name = router_name_4
    try:
        content = subprocess.run([
            'python3',
            '/app/core/sc2_rib.py',
            '-a',
            router_id,
            '-u',
            'cisco',
            '-p',
            'cisco'
        ], capture_output=True, timeout=5)
        content = str(content.stdout)
    except Exception as e:
        print(e)
        content = ''
    finally:
        answer = content
        if '</active-routes-count>' in answer:

            active_routes_count = answer.split('</active-routes-count>')[0].split('<active-routes-count>')[1]
            backup_routes_count = answer.split('</backup-routes-count>')[0].split('<backup-routes-count>')[1]
            deleted_routes_count = answer.split('</deleted-routes-count>')[0].split('<deleted-routes-count>')[1]
            paths_count = answer.split('</paths-count>')[0].split('<paths-count>')[1]
            protocol_route_memory = answer.split('</protocol-route-memory>')[0].split('<protocol-route-memory>')[1]
            af_name = answer.split('</af-name>')[0].split('<af-name>')[1]
            as_number = answer.split('</as>')[0].split('<as>')[1]
            route_table_name = answer.split('</route-table-name>')[0].split('<route-table-name>')[1]
            routes_counts = answer.split('</routes-counts>')[0].split('<routes-counts>')[1]

            mongodb.collection_routers.update_one(
                {'router_id':router_id},
                {'$set': {
                    'rib':{
                        'active_routes_count' : active_routes_count,
                        'backup_routes_count' : backup_routes_count,
                        'deleted_routes_count' : deleted_routes_count,
                        'paths_count' : paths_count,
                        'protocol_route_memory' : protocol_route_memory,
                        'af_name' : af_name,
                        'as_number' : as_number,
                        'route_table_name' : route_table_name,
                        'routes_counts' : routes_counts
                    },
                    'date_modified' : datetime.now()
                }}, upsert = True
            )
        else:
            mongodb.collection_routers.update_one(
                {'router_id':router_id},
                {'$set': {
                    'rib':{
                        'active_routes_count' : 0,
                        'backup_routes_count' : 0,
                        'deleted_routes_count' : 0,
                        'paths_count' : 0,
                        'protocol_route_memory' : 0,
                        'af_name' : None,
                        'as_number' : None,
                        'route_table_name' : None,
                        'routes_counts' : 0
                    },
                    'date_modified' : datetime.now()
                }}, upsert = True
            )
 
    try:
        content = subprocess.run([
            'python3',
            '/app/core/sc4_fib.py',
            '-a',
            router_id,
            '-u',
            'cisco',
            '-p',
            'cisco'
        ], capture_output=True, timeout=5)
        content = str(content.stdout)
    except Exception as e:
        print(e)
        content = ''
    finally:
        answer = content
    # print(answer, type(answer))
        if '</node-name>' in answer:
            node_name = answer.split('</node-name>')[0].split('<node-name>')[1]
            punt_unreachable_packets = answer.split('</punt-unreachable-packets>')[0].split('<punt-unreachable-packets>')[1]
            df_unreachable_packets = answer.split('</df-unreachable-packets>')[0].split('<df-unreachable-packets>')[1]
            encapsulation_failure_packets = answer.split('</encapsulation-failure-packets>')[0].split('<encapsulation-failure-packets>')[1]
            incomplete_adjacency_packets = answer.split('</incomplete-adjacency-packets>')[0].split('<incomplete-adjacency-packets>')[1]
            unresolved_prefix_packets = answer.split('</unresolved-prefix-packets>')[0].split('<unresolved-prefix-packets>')[1]
            unsupported_feature_packets = answer.split('</unsupported-feature-packets>')[0].split('<unsupported-feature-packets>')[1]
            discard_packets = answer.split('</discard-packets>')[0].split('<discard-packets>')[1]
            checksum_error_packets = answer.split('</checksum-error-packets>')[0].split('<checksum-error-packets>')[1]
            fragmenation_consumed_packets = answer.split('</fragmenation-consumed-packets>')[0].split('<fragmenation-consumed-packets>')[1]
            null_packets = answer.split('</null-packets>')[0].split('<null-packets>')[1]
            rpf_check_failure_packets = answer.split('</rpf-check-failure-packets>')[0].split('<rpf-check-failure-packets>')[1]
            rp_destination_drop_packets = answer.split('</rp-destination-drop-packets>')[0].split('<rp-destination-drop-packets>')[1]
            total_number_of_drop_packets = answer.split('</total-number-of-drop-packets>')[0].split('<total-number-of-drop-packets>')[1]
            total_number_of_drop_packets = answer.split('</total-number-of-drop-packets>')[0].split('<total-number-of-drop-packets>')[1]
            mpls_disabled_interface = answer.split('</mpls-disabled-interface>')[0].split('<mpls-disabled-interface>')[1]
            gre_lookup_failed_drop = answer.split('</gre-lookup-failed-drop>')[0].split('<gre-lookup-failed-drop>')[1]
            gre_error_drop = answer.split('</gre-error-drop>')[0].split('<gre-error-drop>')[1]
            lisp_punt_drops = answer.split('</lisp-punt-drops>')[0].split('<lisp-punt-drops>')[1]
            lisp_encap_error_drops = answer.split('</lisp-encap-error-drops>')[0].split('<lisp-encap-error-drops>')[1]
            lisp_decap_error_drops = answer.split('</lisp-decap-error-drops>')[0].split('<lisp-decap-error-drops>')[1]
            multi_label_drops = answer.split('</multi-label-drops>')[0].split('<multi-label-drops>')[1]
            no_route_packets = answer.split('</no-route-packets>')[0].split('<no-route-packets>')[1]

            mongodb.collection_routers.update_one(
                {'router_id':router_id},
                {'$set': {
                    'fib':{
                        'node_name' : node_name,
                        'punt_unreachable_packets' : punt_unreachable_packets,
                        'df_unreachable_packets' : df_unreachable_packets,
                        'encapsulation_failure_packets' : encapsulation_failure_packets,
                        'incomplete_adjacency_packets' : incomplete_adjacency_packets,
                        'unresolved_prefix_packets' : unresolved_prefix_packets,
                        'unsupported_feature_packets' : unsupported_feature_packets,
                        'discard_packets' : discard_packets,
                        'checksum_error_packets' : checksum_error_packets,
                        'fragmenation_consumed_packets' : fragmenation_consumed_packets,
                        'null_packets' : null_packets,
                        'rpf_check_failure_packets' : rpf_check_failure_packets,
                        'rp_destination_drop_packets' : rp_destination_drop_packets,
                        'total_number_of_drop_packets' : total_number_of_drop_packets,
                        'total_number_of_drop_packets' : total_number_of_drop_packets,
                        'mpls_disabled_interface' : mpls_disabled_interface,
                        'gre_lookup_failed_drop' : gre_lookup_failed_drop,
                        'gre_error_drop' : gre_error_drop,
                        'lisp_punt_drops' : lisp_punt_drops,
                        'lisp_encap_error_drops' : lisp_encap_error_drops,
                        'lisp_decap_error_drops' : lisp_decap_error_drops,
                        'multi_label_drops' : multi_label_drops,
                        'no_route_packets' : no_route_packets
                    },
                    'date_modified' : datetime.now()
                }}, upsert = True
            )
        else:
            mongodb.collection_routers.update_one(
                {'router_id':router_id},
                {'$set': {
                    'fib':{
                        'node_name' : None,
                        'punt_unreachable_packets' : 0,
                        'df_unreachable_packets' : 0,
                        'encapsulation_failure_packets' : 0,
                        'incomplete_adjacency_packets' : 0,
                        'unresolved_prefix_packets' : 0,
                        'unsupported_feature_packets' : 0,
                        'discard_packets' : 0,
                        'checksum_error_packets' : 0,
                        'fragmenation_consumed_packets' : 0,
                        'null_packets' : 0,
                        'rpf_check_failure_packets' : 0,
                        'rp_destination_drop_packets' : 0,
                        'total_number_of_drop_packets' : 0,
                        'total_number_of_drop_packets' : 0,
                        'mpls_disabled_interface' : 0,
                        'gre_lookup_failed_drop' : 0,
                        'gre_error_drop' : 0,
                        'lisp_punt_drops' : 0,
                        'lisp_encap_error_drops' : 0,
                        'lisp_decap_error_drops' : 0,
                        'multi_label_drops' : 0,
                        'no_route_packets' : 0
                    },
                    'date_modified' : datetime.now()
                }}, upsert = True
            )
    try:
        content = subprocess.run([
            'python3',
            '/app/core/sc1_open.py',
            '-a',
            router_id,
            '-u',
            'cisco',
            '-p',
            'cisco'
        ], capture_output=True, timeout=5)
        content = str(content.stdout)
    except Exception as e:
        print(e)
        content = ''
    finally:
        answer = content
        if '</as>' in answer:
            as_number = answer.split('</as>')[0].split('<as>')[1]
            total_paths = answer.split('</total-paths>')[0].split('<total-paths>')[1]
            total_prefixes = answer.split('</total-prefixes>')[0].split('<total-prefixes>')[1]
            mongodb.collection_routers.update_one(
                {'router_id':router_id},
                {'$set': {
                    'router_name': router_name,
                    'as_number' : as_number,
                    'total_prefixes' : total_prefixes,
                    'total_paths' : total_paths,
                    'date_modified' : datetime.now()
                }}, upsert = True
            )
        else:
            mongodb.collection_routers.update_one(
                {'router_id':router_id},
                {'$set': {
                    'router_name': router_name,
                    'as_number' : None,
                    'total_prefixes' : None,
                    'total_paths' : None,
                    'date_modified' : datetime.now()
                }}, upsert = True
            ) 

@app.on_event("startup")
@repeat_every(seconds=5, logger=logger) 
async def get_sc3_data1():
    router_id = router_id_1
    try:
        content = subprocess.run([
            'python3',
            '/app/core/sc3_infra.py',
            '-a',
            router_id,
            '-u',
            'cisco',
            '-p',
            'cisco'
        ], capture_output=True, timeout=5)
        content = str(content.stdout)
    except Exception as e:
        print(e)
        content = ''
    finally:
        answer = content
        if '</interface-name>' in answer:        
            interfaces = []
            for data in answer.split('<interface-name>'):

                if '</interface-name>' in data and int(data.split('</packets-sent>')[0].split('<packets-sent>')[1])>0:
                    interface_name = data.split('</interface-name>')[0]
                    bandwidth = data.split('</bandwidth>')[0].split('<bandwidth>')[1]
                    packets_received = data.split('</packets-received>')[0].split('<packets-received>')[1]
                    packets_sent = data.split('</packets-sent>')[0].split('<packets-sent>')[1]
                    bytes_received = data.split('</bytes-received>')[0].split('<bytes-received>')[1]
                    bytes_sent = data.split('</bytes-sent>')[0].split('<bytes-sent>')[1]
                    multicast_packets_received = data.split('</multicast-packets-received>')[0].split('<multicast-packets-received>')[1]
                    carrier_transitions = data.split('</carrier-transitions>')[0].split('<carrier-transitions>')[1]
                    last_data_time = data.split('</last-data-time>')[0].split('<last-data-time>')[1]
                    crc_errors = data.split('</crc-errors>')[0].split('<crc-errors>')[1]
                    input_data_rate = data.split('</input-data-rate>')[0].split('<input-data-rate>')[1]
                    input_drops = data.split('</input-drops>')[0].split('<input-drops>')[1]
                    input_errors = data.split('</input-errors>')[0].split('<input-errors>')[1]
                    input_ignored_packets = data.split('</input-ignored-packets>')[0].split('<input-ignored-packets>')[1]
                    input_load = data.split('</input-load>')[0].split('<input-load>')[1]
                    input_packet_rate = data.split('</input-packet-rate>')[0].split('<input-packet-rate>')[1]
                    input_queue_drops = data.split('</input-queue-drops>')[0].split('<input-queue-drops>')[1]
                    load_interval = data.split('</load-interval>')[0].split('<load-interval>')[1]
                    output_buffer_failures = data.split('</output-buffer-failures>')[0].split('<output-buffer-failures>')[1]
                    output_data_rate = data.split('</output-data-rate>')[0].split('<output-data-rate>')[1]
                    output_drops = data.split('</output-drops>')[0].split('<output-drops>')[1]
                    output_errors = data.split('</output-errors>')[0].split('<output-errors>')[1]
                    output_load = data.split('</output-load>')[0].split('<output-load>')[1]
                    output_packet_rate = data.split('</output-packet-rate>')[0].split('<output-packet-rate>')[1]
                    output_queue_drops = data.split('</output-queue-drops>')[0].split('<output-queue-drops>')[1]
                    peak_input_data_rate = data.split('</peak-input-data-rate>')[0].split('<peak-input-data-rate>')[1]
                    peak_input_packet_rate = data.split('</peak-input-packet-rate>')[0].split('<peak-input-packet-rate>')[1]
                    peak_output_data_rate = data.split('</peak-output-data-rate>')[0].split('<peak-output-data-rate>')[1]
                    peak_output_packet_rate = data.split('</peak-output-packet-rate>')[0].split('<peak-output-packet-rate>')[1]
                    reliability = data.split('</reliability>')[0].split('<reliability>')[1]

                    interface = {
                        'interface_name': interface_name,
                        'bandwidth': bandwidth,
                        'packets_received': packets_received,
                        'packets_sent': packets_sent,
                        'bytes_received': bytes_received,
                        'bytes_sent': bytes_sent,
                        'multicast_packets_received': multicast_packets_received,
                        'carrier_transitions': carrier_transitions,
                        'last_data_time': last_data_time,
                        'crc_errors': crc_errors,
                        'input_data_rate': input_data_rate,
                        'input_drops': input_drops,
                        'input_errors': input_errors,
                        'input_ignored_packets': input_ignored_packets,
                        'input_load': input_load,
                        'input_packet_rate': input_packet_rate,
                        'input_queue_drops': input_queue_drops,
                        'load_interval': load_interval,
                        'output_buffer_failures': output_buffer_failures,
                        'output_data_rate': output_data_rate,
                        'output_drops': output_drops,
                        'output_errors': output_errors,
                        'output_load': output_load,
                        'output_packet_rate': output_packet_rate,
                        'output_queue_drops': output_queue_drops,
                        'peak_input_data_rate': peak_input_data_rate,
                        'peak_input_packet_rate': peak_input_packet_rate,
                        'peak_output_data_rate': peak_output_data_rate,
                        'peak_output_packet_rate': peak_output_packet_rate,
                        'reliability': reliability,
                    }

                    interfaces.append(interface)

            mongodb.collection_routers_state.update_one(
                {'router_id':router_id},
                {'$set': {
                    'interfaces_state':interfaces,
                    'date_modified' : datetime.now()
                }}, upsert = True
            )
        else:
            interface = {
                        'interface_name': None,
                        'bandwidth': 0,
                        'packets_received': 0,
                        'packets_sent': 0,
                        'bytes_received': 0,
                        'bytes_sent': 0,
                        'multicast_packets_received': 0,
                        'carrier_transitions': 0,
                        'last_data_time': 0,
                        'crc_errors': 0,
                        'input_data_rate': 0,
                        'input_drops': 0,
                        'input_errors': 0,
                        'input_ignored_packets': 0,
                        'input_load': 0,
                        'input_packet_rate': 0,
                        'input_queue_drops': 0,
                        'load_interval': 0,
                        'output_buffer_failures': 0,
                        'output_data_rate': 0,
                        'output_drops': 0,
                        'output_errors': 0,
                        'output_load': 0,
                        'output_packet_rate': 0,
                        'output_queue_drops': 0,
                        'peak_input_data_rate': 0,
                        'peak_input_packet_rate': 0,
                        'peak_output_data_rate': 0,
                        'peak_output_packet_rate': 0,
                        'reliability': 0,
                    }
            mongodb.collection_routers_state.update_one(
                {'router_id':router_id},
                {'$set': {
                    'interfaces_state':interface,
                    'date_modified' : datetime.now()
                }}, upsert = True
            )

@app.on_event("startup")
@repeat_every(seconds=7, logger=logger) 
async def get_sc3_data2():
    router_id = router_id_2
    try:
        content = subprocess.run([
            'python3',
            '/app/core/sc3_infra.py',
            '-a',
            router_id,
            '-u',
            'cisco',
            '-p',
            'cisco'
        ], capture_output=True, timeout=5)
        content = str(content.stdout)
    except Exception as e:
        print(e)
        content = ''
    finally:
        answer = content
        if '</interface-name>' in answer:        
            interfaces = []
            for data in answer.split('<interface-name>'):

                if '</interface-name>' in data and int(data.split('</packets-sent>')[0].split('<packets-sent>')[1])>0:
                    interface_name = data.split('</interface-name>')[0]
                    bandwidth = data.split('</bandwidth>')[0].split('<bandwidth>')[1]
                    packets_received = data.split('</packets-received>')[0].split('<packets-received>')[1]
                    packets_sent = data.split('</packets-sent>')[0].split('<packets-sent>')[1]
                    bytes_received = data.split('</bytes-received>')[0].split('<bytes-received>')[1]
                    bytes_sent = data.split('</bytes-sent>')[0].split('<bytes-sent>')[1]
                    multicast_packets_received = data.split('</multicast-packets-received>')[0].split('<multicast-packets-received>')[1]
                    carrier_transitions = data.split('</carrier-transitions>')[0].split('<carrier-transitions>')[1]
                    last_data_time = data.split('</last-data-time>')[0].split('<last-data-time>')[1]
                    crc_errors = data.split('</crc-errors>')[0].split('<crc-errors>')[1]
                    input_data_rate = data.split('</input-data-rate>')[0].split('<input-data-rate>')[1]
                    input_drops = data.split('</input-drops>')[0].split('<input-drops>')[1]
                    input_errors = data.split('</input-errors>')[0].split('<input-errors>')[1]
                    input_ignored_packets = data.split('</input-ignored-packets>')[0].split('<input-ignored-packets>')[1]
                    input_load = data.split('</input-load>')[0].split('<input-load>')[1]
                    input_packet_rate = data.split('</input-packet-rate>')[0].split('<input-packet-rate>')[1]
                    input_queue_drops = data.split('</input-queue-drops>')[0].split('<input-queue-drops>')[1]
                    load_interval = data.split('</load-interval>')[0].split('<load-interval>')[1]
                    output_buffer_failures = data.split('</output-buffer-failures>')[0].split('<output-buffer-failures>')[1]
                    output_data_rate = data.split('</output-data-rate>')[0].split('<output-data-rate>')[1]
                    output_drops = data.split('</output-drops>')[0].split('<output-drops>')[1]
                    output_errors = data.split('</output-errors>')[0].split('<output-errors>')[1]
                    output_load = data.split('</output-load>')[0].split('<output-load>')[1]
                    output_packet_rate = data.split('</output-packet-rate>')[0].split('<output-packet-rate>')[1]
                    output_queue_drops = data.split('</output-queue-drops>')[0].split('<output-queue-drops>')[1]
                    peak_input_data_rate = data.split('</peak-input-data-rate>')[0].split('<peak-input-data-rate>')[1]
                    peak_input_packet_rate = data.split('</peak-input-packet-rate>')[0].split('<peak-input-packet-rate>')[1]
                    peak_output_data_rate = data.split('</peak-output-data-rate>')[0].split('<peak-output-data-rate>')[1]
                    peak_output_packet_rate = data.split('</peak-output-packet-rate>')[0].split('<peak-output-packet-rate>')[1]
                    reliability = data.split('</reliability>')[0].split('<reliability>')[1]

                    interface = {
                        'interface_name': interface_name,
                        'bandwidth': bandwidth,
                        'packets_received': packets_received,
                        'packets_sent': packets_sent,
                        'bytes_received': bytes_received,
                        'bytes_sent': bytes_sent,
                        'multicast_packets_received': multicast_packets_received,
                        'carrier_transitions': carrier_transitions,
                        'last_data_time': last_data_time,
                        'crc_errors': crc_errors,
                        'input_data_rate': input_data_rate,
                        'input_drops': input_drops,
                        'input_errors': input_errors,
                        'input_ignored_packets': input_ignored_packets,
                        'input_load': input_load,
                        'input_packet_rate': input_packet_rate,
                        'input_queue_drops': input_queue_drops,
                        'load_interval': load_interval,
                        'output_buffer_failures': output_buffer_failures,
                        'output_data_rate': output_data_rate,
                        'output_drops': output_drops,
                        'output_errors': output_errors,
                        'output_load': output_load,
                        'output_packet_rate': output_packet_rate,
                        'output_queue_drops': output_queue_drops,
                        'peak_input_data_rate': peak_input_data_rate,
                        'peak_input_packet_rate': peak_input_packet_rate,
                        'peak_output_data_rate': peak_output_data_rate,
                        'peak_output_packet_rate': peak_output_packet_rate,
                        'reliability': reliability,
                    }

                    interfaces.append(interface)

            mongodb.collection_routers_state.update_one(
                {'router_id':router_id},
                {'$set': {
                    'interfaces_state':interfaces,
                    'date_modified' : datetime.now()
                }}, upsert = True
            )
        else:
            interface = {
                        'interface_name': None,
                        'bandwidth': 0,
                        'packets_received': 0,
                        'packets_sent': 0,
                        'bytes_received': 0,
                        'bytes_sent': 0,
                        'multicast_packets_received': 0,
                        'carrier_transitions': 0,
                        'last_data_time': 0,
                        'crc_errors': 0,
                        'input_data_rate': 0,
                        'input_drops': 0,
                        'input_errors': 0,
                        'input_ignored_packets': 0,
                        'input_load': 0,
                        'input_packet_rate': 0,
                        'input_queue_drops': 0,
                        'load_interval': 0,
                        'output_buffer_failures': 0,
                        'output_data_rate': 0,
                        'output_drops': 0,
                        'output_errors': 0,
                        'output_load': 0,
                        'output_packet_rate': 0,
                        'output_queue_drops': 0,
                        'peak_input_data_rate': 0,
                        'peak_input_packet_rate': 0,
                        'peak_output_data_rate': 0,
                        'peak_output_packet_rate': 0,
                        'reliability': 0,
                    }
            mongodb.collection_routers_state.update_one(
                {'router_id':router_id},
                {'$set': {
                    'interfaces_state':interface,
                    'date_modified' : datetime.now()
                }}, upsert = True
            )

@app.on_event("startup")
@repeat_every(seconds=5, logger=logger) 
async def get_sc3_data3():
    router_id = router_id_3
    try:
        content = subprocess.run([
            'python3',
            '/app/core/sc3_infra.py',
            '-a',
            router_id,
            '-u',
            'cisco',
            '-p',
            'cisco'
        ], capture_output=True, timeout=5)
        content = str(content.stdout)
    except Exception as e:
        print(e)
        content = ''
    finally:
        answer = content
        if '</interface-name>' in answer:        
            interfaces = []
            for data in answer.split('<interface-name>'):

                if '</interface-name>' in data and int(data.split('</packets-sent>')[0].split('<packets-sent>')[1])>0:
                    interface_name = data.split('</interface-name>')[0]
                    bandwidth = data.split('</bandwidth>')[0].split('<bandwidth>')[1]
                    packets_received = data.split('</packets-received>')[0].split('<packets-received>')[1]
                    packets_sent = data.split('</packets-sent>')[0].split('<packets-sent>')[1]
                    bytes_received = data.split('</bytes-received>')[0].split('<bytes-received>')[1]
                    bytes_sent = data.split('</bytes-sent>')[0].split('<bytes-sent>')[1]
                    multicast_packets_received = data.split('</multicast-packets-received>')[0].split('<multicast-packets-received>')[1]
                    carrier_transitions = data.split('</carrier-transitions>')[0].split('<carrier-transitions>')[1]
                    last_data_time = data.split('</last-data-time>')[0].split('<last-data-time>')[1]
                    crc_errors = data.split('</crc-errors>')[0].split('<crc-errors>')[1]
                    input_data_rate = data.split('</input-data-rate>')[0].split('<input-data-rate>')[1]
                    input_drops = data.split('</input-drops>')[0].split('<input-drops>')[1]
                    input_errors = data.split('</input-errors>')[0].split('<input-errors>')[1]
                    input_ignored_packets = data.split('</input-ignored-packets>')[0].split('<input-ignored-packets>')[1]
                    input_load = data.split('</input-load>')[0].split('<input-load>')[1]
                    input_packet_rate = data.split('</input-packet-rate>')[0].split('<input-packet-rate>')[1]
                    input_queue_drops = data.split('</input-queue-drops>')[0].split('<input-queue-drops>')[1]
                    load_interval = data.split('</load-interval>')[0].split('<load-interval>')[1]
                    output_buffer_failures = data.split('</output-buffer-failures>')[0].split('<output-buffer-failures>')[1]
                    output_data_rate = data.split('</output-data-rate>')[0].split('<output-data-rate>')[1]
                    output_drops = data.split('</output-drops>')[0].split('<output-drops>')[1]
                    output_errors = data.split('</output-errors>')[0].split('<output-errors>')[1]
                    output_load = data.split('</output-load>')[0].split('<output-load>')[1]
                    output_packet_rate = data.split('</output-packet-rate>')[0].split('<output-packet-rate>')[1]
                    output_queue_drops = data.split('</output-queue-drops>')[0].split('<output-queue-drops>')[1]
                    peak_input_data_rate = data.split('</peak-input-data-rate>')[0].split('<peak-input-data-rate>')[1]
                    peak_input_packet_rate = data.split('</peak-input-packet-rate>')[0].split('<peak-input-packet-rate>')[1]
                    peak_output_data_rate = data.split('</peak-output-data-rate>')[0].split('<peak-output-data-rate>')[1]
                    peak_output_packet_rate = data.split('</peak-output-packet-rate>')[0].split('<peak-output-packet-rate>')[1]
                    reliability = data.split('</reliability>')[0].split('<reliability>')[1]

                    interface = {
                        'interface_name': interface_name,
                        'bandwidth': bandwidth,
                        'packets_received': packets_received,
                        'packets_sent': packets_sent,
                        'bytes_received': bytes_received,
                        'bytes_sent': bytes_sent,
                        'multicast_packets_received': multicast_packets_received,
                        'carrier_transitions': carrier_transitions,
                        'last_data_time': last_data_time,
                        'crc_errors': crc_errors,
                        'input_data_rate': input_data_rate,
                        'input_drops': input_drops,
                        'input_errors': input_errors,
                        'input_ignored_packets': input_ignored_packets,
                        'input_load': input_load,
                        'input_packet_rate': input_packet_rate,
                        'input_queue_drops': input_queue_drops,
                        'load_interval': load_interval,
                        'output_buffer_failures': output_buffer_failures,
                        'output_data_rate': output_data_rate,
                        'output_drops': output_drops,
                        'output_errors': output_errors,
                        'output_load': output_load,
                        'output_packet_rate': output_packet_rate,
                        'output_queue_drops': output_queue_drops,
                        'peak_input_data_rate': peak_input_data_rate,
                        'peak_input_packet_rate': peak_input_packet_rate,
                        'peak_output_data_rate': peak_output_data_rate,
                        'peak_output_packet_rate': peak_output_packet_rate,
                        'reliability': reliability,
                    }

                    interfaces.append(interface)

            mongodb.collection_routers_state.update_one(
                {'router_id':router_id},
                {'$set': {
                    'interfaces_state':interfaces,
                    'date_modified' : datetime.now()
                }}, upsert = True
            )
        else:
            interface = {
                        'interface_name': None,
                        'bandwidth': 0,
                        'packets_received': 0,
                        'packets_sent': 0,
                        'bytes_received': 0,
                        'bytes_sent': 0,
                        'multicast_packets_received': 0,
                        'carrier_transitions': 0,
                        'last_data_time': 0,
                        'crc_errors': 0,
                        'input_data_rate': 0,
                        'input_drops': 0,
                        'input_errors': 0,
                        'input_ignored_packets': 0,
                        'input_load': 0,
                        'input_packet_rate': 0,
                        'input_queue_drops': 0,
                        'load_interval': 0,
                        'output_buffer_failures': 0,
                        'output_data_rate': 0,
                        'output_drops': 0,
                        'output_errors': 0,
                        'output_load': 0,
                        'output_packet_rate': 0,
                        'output_queue_drops': 0,
                        'peak_input_data_rate': 0,
                        'peak_input_packet_rate': 0,
                        'peak_output_data_rate': 0,
                        'peak_output_packet_rate': 0,
                        'reliability': 0,
                    }
            mongodb.collection_routers_state.update_one(
                {'router_id':router_id},
                {'$set': {
                    'interfaces_state':interface,
                    'date_modified' : datetime.now()
                }}, upsert = True
            )

@app.on_event("startup")
@repeat_every(seconds=5, logger=logger) 
async def get_sc3_data4():
    router_id = router_id_4
    try:
        content = subprocess.run([
            'python3',
            '/app/core/sc3_infra.py',
            '-a',
            router_id,
            '-u',
            'cisco',
            '-p',
            'cisco'
        ], capture_output=True, timeout=5)
        content = str(content.stdout)
    except Exception as e:
        print(e)
        content = ''
    finally:
        answer = content
        if '</interface-name>' in answer:        
            interfaces = []
            for data in answer.split('<interface-name>'):

                if '</interface-name>' in data and int(data.split('</packets-sent>')[0].split('<packets-sent>')[1])>0:
                    interface_name = data.split('</interface-name>')[0]
                    bandwidth = data.split('</bandwidth>')[0].split('<bandwidth>')[1]
                    packets_received = data.split('</packets-received>')[0].split('<packets-received>')[1]
                    packets_sent = data.split('</packets-sent>')[0].split('<packets-sent>')[1]
                    bytes_received = data.split('</bytes-received>')[0].split('<bytes-received>')[1]
                    bytes_sent = data.split('</bytes-sent>')[0].split('<bytes-sent>')[1]
                    multicast_packets_received = data.split('</multicast-packets-received>')[0].split('<multicast-packets-received>')[1]
                    carrier_transitions = data.split('</carrier-transitions>')[0].split('<carrier-transitions>')[1]
                    last_data_time = data.split('</last-data-time>')[0].split('<last-data-time>')[1]
                    crc_errors = data.split('</crc-errors>')[0].split('<crc-errors>')[1]
                    input_data_rate = data.split('</input-data-rate>')[0].split('<input-data-rate>')[1]
                    input_drops = data.split('</input-drops>')[0].split('<input-drops>')[1]
                    input_errors = data.split('</input-errors>')[0].split('<input-errors>')[1]
                    input_ignored_packets = data.split('</input-ignored-packets>')[0].split('<input-ignored-packets>')[1]
                    input_load = data.split('</input-load>')[0].split('<input-load>')[1]
                    input_packet_rate = data.split('</input-packet-rate>')[0].split('<input-packet-rate>')[1]
                    input_queue_drops = data.split('</input-queue-drops>')[0].split('<input-queue-drops>')[1]
                    load_interval = data.split('</load-interval>')[0].split('<load-interval>')[1]
                    output_buffer_failures = data.split('</output-buffer-failures>')[0].split('<output-buffer-failures>')[1]
                    output_data_rate = data.split('</output-data-rate>')[0].split('<output-data-rate>')[1]
                    output_drops = data.split('</output-drops>')[0].split('<output-drops>')[1]
                    output_errors = data.split('</output-errors>')[0].split('<output-errors>')[1]
                    output_load = data.split('</output-load>')[0].split('<output-load>')[1]
                    output_packet_rate = data.split('</output-packet-rate>')[0].split('<output-packet-rate>')[1]
                    output_queue_drops = data.split('</output-queue-drops>')[0].split('<output-queue-drops>')[1]
                    peak_input_data_rate = data.split('</peak-input-data-rate>')[0].split('<peak-input-data-rate>')[1]
                    peak_input_packet_rate = data.split('</peak-input-packet-rate>')[0].split('<peak-input-packet-rate>')[1]
                    peak_output_data_rate = data.split('</peak-output-data-rate>')[0].split('<peak-output-data-rate>')[1]
                    peak_output_packet_rate = data.split('</peak-output-packet-rate>')[0].split('<peak-output-packet-rate>')[1]
                    reliability = data.split('</reliability>')[0].split('<reliability>')[1]

                    interface = {
                        'interface_name': interface_name,
                        'bandwidth': bandwidth,
                        'packets_received': packets_received,
                        'packets_sent': packets_sent,
                        'bytes_received': bytes_received,
                        'bytes_sent': bytes_sent,
                        'multicast_packets_received': multicast_packets_received,
                        'carrier_transitions': carrier_transitions,
                        'last_data_time': last_data_time,
                        'crc_errors': crc_errors,
                        'input_data_rate': input_data_rate,
                        'input_drops': input_drops,
                        'input_errors': input_errors,
                        'input_ignored_packets': input_ignored_packets,
                        'input_load': input_load,
                        'input_packet_rate': input_packet_rate,
                        'input_queue_drops': input_queue_drops,
                        'load_interval': load_interval,
                        'output_buffer_failures': output_buffer_failures,
                        'output_data_rate': output_data_rate,
                        'output_drops': output_drops,
                        'output_errors': output_errors,
                        'output_load': output_load,
                        'output_packet_rate': output_packet_rate,
                        'output_queue_drops': output_queue_drops,
                        'peak_input_data_rate': peak_input_data_rate,
                        'peak_input_packet_rate': peak_input_packet_rate,
                        'peak_output_data_rate': peak_output_data_rate,
                        'peak_output_packet_rate': peak_output_packet_rate,
                        'reliability': reliability,
                    }

                    interfaces.append(interface)

            mongodb.collection_routers_state.update_one(
                {'router_id':router_id},
                {'$set': {
                    'interfaces_state':interfaces,
                    'date_modified' : datetime.now()
                }}, upsert = True
            )
        else:
            interface = {
                        'interface_name': None,
                        'bandwidth': 0,
                        'packets_received': 0,
                        'packets_sent': 0,
                        'bytes_received': 0,
                        'bytes_sent': 0,
                        'multicast_packets_received': 0,
                        'carrier_transitions': 0,
                        'last_data_time': 0,
                        'crc_errors': 0,
                        'input_data_rate': 0,
                        'input_drops': 0,
                        'input_errors': 0,
                        'input_ignored_packets': 0,
                        'input_load': 0,
                        'input_packet_rate': 0,
                        'input_queue_drops': 0,
                        'load_interval': 0,
                        'output_buffer_failures': 0,
                        'output_data_rate': 0,
                        'output_drops': 0,
                        'output_errors': 0,
                        'output_load': 0,
                        'output_packet_rate': 0,
                        'output_queue_drops': 0,
                        'peak_input_data_rate': 0,
                        'peak_input_packet_rate': 0,
                        'peak_output_data_rate': 0,
                        'peak_output_packet_rate': 0,
                        'reliability': 0,
                    }
            mongodb.collection_routers_state.update_one(
                {'router_id':router_id},
                {'$set': {
                    'interfaces_state':interface,
                    'date_modified' : datetime.now()
                }}, upsert = True
            )

