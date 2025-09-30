import os
import requests
from langchain_core.tools import tool

def nso_call(endpoint: str, method: str = "GET", data: dict = None):
    """
    Generic helper for NSO RESTCONF API calls.
    """
    nso_user = os.getenv("NSO_USER")
    nso_pwd = os.getenv("NSO_PWD")
    nso_url = os.getenv("NSO_URL", "http://localhost:8080/restconf/data")
    url = f"{nso_url}{endpoint}"

    auth=(nso_user, nso_pwd)
    headers = {"Content-Type": "application/yang-data+json"}
    try:
        if method == "GET":
            resp = requests.get(url, auth=auth, headers=headers)
        else:
            resp = requests.post(url, json=data, auth=auth, headers=headers)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        return {"error": str(e)}

@tool
def get_service_parameters(service_id: str) -> dict:
    """Queries the NSO to get the l3vpn service attributes based on the service id."""
    return nso_call(endpoint=f"/tailf-ncs:services/l3vpn:l3vpn={service_id}", method="GET")

@tool
def execute_ping(device_name: str, vrf_name: str, ipv4_address: str) -> dict:
    """Queries the NSO to execute a ping for a particular ipv4 address inside a VRF on a PE device."""
    return nso_call(
        endpoint=f"/tailf-ncs:devices/device={device_name}/live-status/tailf-ned-cisco-ios-xr-stats:exec/any", 
        method="POST",
        data={"input": {"args": f"ping vrf {vrf_name} {ipv4_address}"}})

@tool
def check_if_status(device_name: str, interface_name: str) -> dict:
    """Queries the NSO to check the status of a particular link/interface on a PE device."""
    return nso_call(
        endpoint=f"/tailf-ncs:devices/device={device_name}/live-status/tailf-ned-cisco-ios-xr-stats:exec/any",
        method="POST",
        data={"input": {"args": f"show interface {interface_name}"}})

@tool
def check_mp_bgp_session_status(device_name: str) -> dict:
    """Queries the NSO to check the status of the MP-BGP session on a PE device."""
    return nso_call(
        endpoint=f"/tailf-ncs:devices/device={device_name}/live-status/tailf-ned-cisco-ios-xr-stats:exec/any",
        method="POST",
        data={"input": {"args": f"show bgp vpnv4 unicast summary"}})

@tool
def check_rt_configuration(device_name: str, vrf_name: str) -> dict:
    """Queries the NSO to check the status of the RT configuration on a PE device."""
    return nso_call(
        endpoint=f"/tailf-ncs:devices/device={device_name}/live-status/tailf-ned-cisco-ios-xr-stats:exec/any",
        method="POST",
        data={"input": {"args": f"show vrf {vrf_name} detail"}})

@tool
def check_route_availability(device_name: str, vrf_name: str) -> dict:
    """Queries the NSO to check the bgp database routing information for a particular VRF on a PE device."""
    return nso_call(
        endpoint=f"/tailf-ncs:devices/device={device_name}/live-status/tailf-ned-cisco-ios-xr-stats:exec/any",
        method="POST",
        data={"input": {"args": f"show bgp vpnv4 unicast vrf {vrf_name}"}})


