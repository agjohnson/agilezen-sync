'''

    AgileZen - Storage

    Stores ticket information locally

'''

from agilezensync.resources import Storage, Chili, Github

def sync():
    store = Storage()
    store.open()
    
    if store.conf['chili']:
        chili = Chili(
            url=store.conf['chili']['url'],
            api=store.conf['chili']['api']
        )
        for ticket in chili.tickets(store.conf['chili']['uid']):
            store.update_relationship(ticket)

    if store.conf['github']:
        github = Github(auth=(
            store.conf['github']['username'],
            store.conf['github']['password']
        ))
        for ticket in github.tickets(
                store.conf['github']['username'],
                store.conf['github']['repo']):
            store.update_relationship(ticket)

