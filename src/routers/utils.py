def filter_generate_output(generate_output):
    dicret = generate_output.__dict__
    del dicret['_sa_instance_state']
    dicret['created_at'] = int(dicret['created_at'].timestamp())

    return dicret


def filter_generate_outputs(generate_outputs):
    result = []
    for generate_output in generate_outputs:
        result.append(filter_generate_output(generate_output))

    return result
