#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Resilient Systems, Inc. ("Resilient") is willing to license software
# or access to software to the company or entity that will be using or
# accessing the software and documentation and that you represent as
# an employee or authorized agent ("you" or "your") only on the condition
# that you accept all of the terms of this license agreement.
#
# The software and documentation within Resilient's Development Kit are
# copyrighted by and contain confidential information of Resilient. By
# accessing and/or using this software and documentation, you agree that
# while you may make derivative works of them, you:
#
# 1)  will not use the software and documentation or any derivative
#     works for anything but your internal business purposes in
#     conjunction your licensed used of Resilient's software, nor
# 2)  provide or disclose the software and documentation or any
#     derivative works to any third party.
#
# THIS SOFTWARE AND DOCUMENTATION IS PROVIDED "AS IS" AND ANY EXPRESS
# OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL RESILIENT BE LIABLE FOR ANY DIRECT,
# INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
# HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,
# STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED
# OF THE POSSIBILITY OF SUCH DAMAGE.

"""Action Module circuits example to define new incident types in the entry wizard"""

from __future__ import print_function
import logging
from circuits.core.handlers import handler
import co3
from resilient_circuits.actions_component import ResilientComponent

LOG = logging.getLogger(__name__)

CONFIG_DATA_SECTION = "auto_add_new_inc_type"

class NewIncComponent(ResilientComponent):
    """Circuits framework to add a new incident type via the entry wizard"""

    def __init__(self, opts):
        super(NewIncComponent, self).__init__(opts)

        self.options = opts.get(CONFIG_DATA_SECTION, {})
        LOG.debug(self.options)

        #The queue name, "add_new_object", is specified in the app.config.fragment file
        self.channel = "actions." + self.options.get("queue", add_new_object)

    @handler("add_new_incident_type")
    def _add_new_inc_type(self, event, source=None, headers=None, message=None):
        """Function to automatically add new incident types to Incident Types and the Incident via the entry wizard"""
        incident = event.message["incident"]
        inc_id = incident["id"]
        results = []

        # Saves the name of the new incident type
        new_inc_type = incident["properties"]["enter_new_incident_type"]

        # New incident type skeleton
        obj = {"system": False, "parent_id": None, "create_date": None, "name": "Example", "hidden": False, "enabled": True, "id": None, "description": None}
        
        # Adds all the entered incident types to Resilient
        LOG.info('Updated incident types with %s type', new_inc_type)
        obj["name"] = new_inc_type
        results.append(self.rest_client().post("/incident_types", obj))

        # Function to add an incident type to an incident
        def update_inc(incident):
            LOG.info('Updated incident with %s type', new_inc_type)
            incident["incident_type_ids"].append(new_inc_type)
        return incident
	
        # Updates the incident types with the types defined in the new entry wiz
        self.rest_client().get_put("/incidents/{}".format(inc_id), update_inc, co3_context_token=event.context)

