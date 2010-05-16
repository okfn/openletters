import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to

import genshi

from openletters.lib.base import BaseController, render
from openletters import model
from openletters.transform import transform_json

log = logging.getLogger(__name__)

class TimelineController(BaseController):

    def index(self):
        # Return a rendered template
        #return render('/timeline.mako')
        # or, return a response
        timeline = "<p>This page will contain a timeline for the letters of Charles Dickens<p>"
        c.letterhtml = genshi.HTML(timeline)
        if c.letterhtml is None:
            abort(404)
        else:
            return render('timeline.html')
