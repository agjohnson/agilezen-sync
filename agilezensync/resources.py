'''

    AgileZen - Resources

'''

import json
import requests
import slumber
import ConfigParser
import os.path

from agilezensync.model import Story, Ticket

class AgileZen(slumber.API):
    '''AgileZen API with Slumber'''

    def __init__(self, api):
        '''Return slumber object'''
        slumber.API.__init__(
            self,
            base_url='https://agilezen.com/api/v1',
            session=requests.session(
                headers={'X-Zen-ApiKey': api}
            )
        )

    def stories(self, project):
        '''Generator function for returning project stories'''
        data = self.projects(project).stories.get()
        if not 'items' in data:
            yield []
        for story in data['items']:
            yield Story(
                story_id=story['id'],
                text=story['text'],
                priority=story['priority'] if 'priority' in story else None,
                color=story['color'] if 'color' in story else None,
                tags=story['tags'] if 'tags' in story else None
            )

class Chili(slumber.API):
    '''Chili project API with Slumber'''

    def __init__(self, url, api):
        '''Return slumber object authenticating at url with api key'''
        slumber.API.__init__(
            self,
            base_url=url,
            append_slash=False,
            append_format=True,
            auth=(api, "foobar")
        )
        self.name = 'chili'
    
    def tickets(self, uid):
        '''Generator function for list of tickets as stories'''
        data = self.issues.get(assigned_to_id=uid)
        if 'issues' in data:
            for ticket in data['issues']:
                yield Ticket(
                    resource=self,
                    ticket_id=ticket['id'],
                    text='[#{id}]({url}/issues/{id}) {subject}'.format(
                        url=self._store.get('base_url'),
                        **ticket
                    ),
                    priority=ticket['priority']['name'],
                )

class Github(slumber.API):
    '''Github issue API with slumber'''

    def __init__(self, auth):
        '''Return slumber object'''
        slumber.API.__init__(
            self,
            base_url='https://api.github.com',
            append_slash=False,
            auth=auth
        )
        self.name = 'github'
    
    def tickets(self, username, repo):
        '''Generator function for tickets'''
        tickets = self.repos(username)(repo).issues.get()
        for ticket in tickets:
            # TODO add tags
            yield Ticket(
                resource=self,
                ticket_id=ticket['number'],
                text='[#{number}]({url}) {title}'.format(**ticket),
            )


class Storage():
    '''AgileZen relationship cache'''

    data = dict()
    config = dict()
    conf = dict()

    def __init__(self, cfg_file='agilezensync.cfg', cache='cache.json'):
        self.storage = {}

        config = ConfigParser.RawConfigParser()
        config.read(cfg_file)
        for sect in ['agilezen', 'chili', 'github']:
            if config.has_section(sect):
                self.conf[sect] = dict(config.items(sect))

        self.open()

    def open(self):
        '''Open storage cache'''
        if not os.path.exists('cache.json'):
            self.data = dict()
        h = open('cache.json', 'r')
        self.data = json.load(h)
        h.close()

    def save(self):
        '''Save to cache file'''
        h = open('cache.json', 'w')
        json.dump(self.data, h)
        h.close()
    
    def agilezen(self, project=True):
        '''Return agilezen'''
        if not hasattr(self, '_agilezen') or self._agilezen is None:
            self._agilezen = AgileZen(
                self.conf['agilezen']['api']
            )
        if project:
            return self._agilezen.projects(self.conf['agilezen']['project'])
        else:
            return self._agilezen

    def update_relationship(self, ticket):
        '''Update storage with relationship'''
        ticket_key = '{ticket.resource.name}-{ticket.ticket_id}'.format(ticket=ticket)
        print 'Searching for relationship for {key}'.format(key=ticket_key)
        if ticket_key in self.data:
            story_id = self.data[ticket_key]['story']
            print "Updating story {story_id}".format(story_id=story_id)
            
            story = self.agilezen().stories(story_id)
            if story:
                story.put(ticket.story_dict())
        else:
            print "Adding ticket {ticket.ticket_id}".format(ticket=ticket)
            story_json = self.agilezen().stories.post(
                ticket.story_dict()
            )
            story = json.loads(story_json)
            self.data.update({
                '{t.resource.name}-{t.ticket_id}'.format(t=ticket): {
                    'story': story['id']
                }
            })

        self.save()         

