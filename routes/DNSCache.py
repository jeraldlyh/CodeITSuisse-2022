import logging
from asyncio.log import logger

from flask import jsonify, request
from utils.firestore import Firestore

from routes import app


@app.route("/instantiateDNSLookup", methods=["POST"])
async def instantiateDNSLookup():
    input_data = request.get_json()
    logging.info(input_data)

    lookup_table = input_data["lookupTable"]

    db = Firestore()
    await db.create_lookup_table(lookup_table)
    return jsonify({"success": True})


@app.route("/simulateQuery", methods=["POST"])
async def simulateQuery():
    input_data = request.get_json()
    logger.info(input_data)
    cache_size = input_data["cacheSize"]
    logs = input_data["log"]
    cache = {}

    db = Firestore()
    lookup_table = await db.get_lookup_table()
    output = []

    for log in logs:
        ip_address = retrieve_ip_address(log, lookup_table)
        is_null_ip_address = ip_address is None
        if log not in cache:
            payload = {
                "status": "cache miss" if not is_null_ip_address else "invalid",
                "ipAddress": ip_address,
            }

            if not is_null_ip_address:
                if len(cache) == cache_size:
                    cache.pop(next(iter(cache)))
                cache[log] = {"ip_address": ip_address}
            output.append(payload)
        else:
            payload = {"status": "cache hit", "ipAddress": ip_address}
            output.append(payload)

    return jsonify({"JSON": output})


def retrieve_ip_address(domain, lookup_table):
    if domain not in lookup_table:
        return None
    return lookup_table[domain]
