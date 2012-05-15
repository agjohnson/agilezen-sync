'''

    AgileZen - Models

'''

import json
import requests
import slumber

class Story():
    '''Represents an AgileZen story'''
    
    def __init__(self, text, story_id=None, priority=None, color=None,
            tags=None):
        '''Build a story object'''
        self.text = text
        self.story_id = story_id
        self.priority = priority
        self.color = color
        self.tags = tags

    def ticket(self, ticket=None):
        '''Return linked ticket'''
        if ticket:
            self.ticket = ticket
        return self.ticket

    def __repr__(self):
        return '<agilezensync.model.Story id={o.story_id}>'.format(o=self)

class StoryRelationship():
    '''Represent an AgileZen story relationship to a ticket'''

    def __init__(self, story, ticket):
        '''Build relationship'''
        self.story = story
        self.ticket = ticket
        self.story.ticket(ticket)
        self.ticket.story(story)

class Ticket():
    '''Represents an exported ticket'''

    def __init__(self, resource, ticket_id, text, priority=None, tags=None):
        '''Build ticket'''
        self.resource = resource
        self.ticket_id = ticket_id
        self.text = text
        self.priority = priority
        self.tags = tags

    def story(self, story=None):
        '''Return linked story'''
        if story:
            self.story = story
        return self.story
    
    def story_dict(self):
        '''Convert ticket to usable dict'''

        def get_color(priority):
            colors = {
                "Low": "grey",
                "Normal": "blue",
                "High": "green",
                "Urgent": "yellow",
                "Immediate": "red"
            }
            return colors[priority] if priority in colors else None
        
        # TODO more properties
        story = {
            'text': self.text,
            'priority': self.priority,
            'tags': self.tags             
        }
        if hasattr(self, 'priority') and self.priority is not None:
            story['priority'] = self.priority
            story['color'] = get_color(story['priority'])
        return story

    def __repr__(self):
        return '<agilezensync.model.Ticket resource={o.resource.name} id={o.ticket_id}>'.format(o=self)

