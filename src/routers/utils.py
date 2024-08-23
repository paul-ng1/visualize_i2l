def filter_urls(messages):
    result = []
    for (message, verified) in messages:
        dicret = message.__dict__
        del dicret['_sa_instance_state']
        del dicret['metadata_']
        dicret['created_at'] = int(dicret['created_at'].timestamp())
        dicret['notified_at'] = int(dicret['notified_at'].timestamp())
        dicret['verified'] = verified
        result.append(dicret)

    return result