from pacu.core.io.trajectory import session

def index(req, id):
    couples = session.get_trial_index(id)
    return [
        dict(index=index, name=name)
        for index, name in couples
    ]
