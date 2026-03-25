def service_allowed(service, flight):

    airline = flight[:2]   # 

    # Indigo restriction
    if airline == "6E":
        if service in ["IE", "IEF"]:
            return True
        else:
            return False

    # All other airlines allowed
    return True