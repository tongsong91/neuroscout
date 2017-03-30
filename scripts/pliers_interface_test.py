from nipype.pipeline.engine import Node, Workflow
import nipype.interfaces.pliers as pliers

from nipype.interfaces.utility import Function

import os

bids_dir = os.path.abspath('/home/zorro/datasets/ds009')
task = 'emotionalregulation'
run = ['run-01']
subject = '01'
json_spec = '/home/zorro/repos/neuroscout/scripts/test_spec.json'

"""
Set up workflow
"""
wf = Workflow(name='first_level')

"""
Get event files
"""

def _get_events(bids_dir, subject_id, runs, task):
    """ Get a subject's event files """
    from bids.grabbids import BIDSLayout
    layout = BIDSLayout(bids_dir)
    events = [layout.get(
        type='events', return_type='file', subject=subject_id, run=r, task=task)[0] for r in runs]
    return events

events_getter = Node(name='events', interface=Function(
    input_names=['bids_dir', 'subject_id', 'runs', 'task'],
    output_names=['events'], function=_get_events))
events_getter.inputs.runs = run
events_getter.inputs.bids_dir = bids_dir
events_getter.inputs.task = task
events_getter.inputs.subject_id = subject


"""
Extract features, for a given set of subjects, etc and write out a
set of new event files.
"""

pliers_extract = Node(interface=pliers.PliersInterface(), name='pliers')
pliers_extract.inputs.graph_spec = json_spec
pliers_extract.inputs.bids_directory = bids_dir
wf.connect(events_getter, 'events', pliers_extract, 'event_files')
wf.run()