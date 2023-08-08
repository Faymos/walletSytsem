

def serializeDict(args) -> dict:
    return {
        **{i: str(args[i]) for i in args if i=='_id'}, **{i: args[i] for i in args if i!= '_id'}}
   


def serializeList(entity) -> list:
    return [serializeDict(args) for args in entity]
    