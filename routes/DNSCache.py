from datetime import datetime

from flask import jsonify, request
from utils.firestore import Firestore

from routes import app


@app.route("/instantiateDNSLookup", methods=["POST"])
async def instantiateDNSLookup():
    input_data = request.get_json()

    lookup_table = input_data["lookupTable"]

    db = Firestore()
    await db.create_lookup_table(lookup_table)
    return jsonify({"success": True})


@app.route("/simulateQuery", methods=["POST"])
async def simulateQuery():
    input_data = request.get_json()
    cache_size = input_data["cacheSize"]
    logs = input_data["log"]
    cache = {}

    db = Firestore()
    lookup_table = await db.get_lookup_table()
    output = []

    for log in logs:
        ip_address = retrieve_ip_address(log, lookup_table)
        is_null_ip_address = ip_address is None
        payload = None

        if log not in cache:
            payload = {
                "status": "cache miss" if not is_null_ip_address else "invalid",
                "ipAddress": ip_address,
            }

            if not is_null_ip_address:
                if len(cache) == cache_size:
                    least_recently_used = datetime.max
                    least_used_domain = None
                    for key, value in cache.items():
                        if value["datetime"] < least_recently_used:
                            least_recently_used = value["datetime"]
                            least_used_domain = key
                    cache.pop(least_used_domain)
                cache[log] = {"ip_address": ip_address, "datetime": datetime.now()}
        else:
            payload = {"status": "cache hit", "ipAddress": ip_address}
            cache[log]["datetime"] = datetime.now()
        output.append(payload)

    return jsonify({"JSON": output, "status": 200})


def retrieve_ip_address(domain, lookup_table):
    if domain not in lookup_table:
        return None
    return lookup_table[domain]
