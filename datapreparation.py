from __future__ import division
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import pretty_midi
import os
import pypianoroll as pproll
import sys



def piano_roll_to_pretty_midi(piano_roll, fs=100, program=2):
    '''Convert a Piano Roll array into a PrettyMidi object
     with a single instrument.

    Parameters
    ----------
    piano_roll : np.ndarray, shape=(128,frames), dtype=int
        Piano roll of one instrument
    fs : int
        Sampling frequency of the columns, i.e. each column is spaced apart
        by ``1./fs`` seconds.
    program : int
        The program number of the instrument.

    Returns
    -------
    midi_object : pretty_midi.PrettyMIDI
        A pretty_midi.PrettyMIDI class instance describing
        the piano roll.

    '''
    notes, frames = piano_roll.shape
    pm = pretty_midi.PrettyMIDI()
    instrument = pretty_midi.Instrument(program=program)

    # pad 1 column of zeros so we can acknowledge inital and ending events
    piano_roll = np.pad(piano_roll, [(0, 0), (1, 1)], 'constant')

    # use changes in velocities to find note on / note off events
    velocity_changes = np.nonzero(np.diff(piano_roll).T)

    # keep track on velocities and note on times
    prev_velocities = np.zeros(notes, dtype=int)
    note_on_time = np.zeros(notes)

    for time, note in zip(*velocity_changes):
        # use time + 1 because of padding above
        velocity = piano_roll[note, time + 1]
        time = time / fs
        if velocity > 0:
            if prev_velocities[note] == 0:
                note_on_time[note] = time
                prev_velocities[note] = velocity
        else:
            pm_note = pretty_midi.Note(
                velocity=prev_velocities[note],
                pitch=note,
                start=note_on_time[note],
                end=time)
            instrument.notes.append(pm_note)
            prev_velocities[note] = 0
    pm.instruments.append(instrument)
    return pm


def piano_roll_to_mid_file(pianoroll_matrix,fname,fs=5):
    """ input: piano roll matrix with shape (number of notes, time steps)
        output: string with path to mid file
    """
    piano_roll_to_pretty_midi(pianoroll_matrix,fs).write(fname)
    return os.path.join(os.getcwd(),fname)
    
def midfile_to_piano_roll(filepath,instrument_n=0,fs=5):
    """ convert mid file to piano_roll dataframe, but selecting a specific instrument in the mid file
        input: path to mid file, intrument to select in midfile
        output: piano_roll as dataframe
    """
    pm = pretty_midi.PrettyMIDI(filepath)
    roll = pm.instruments[instrument_n].get_piano_roll(fs)
    return roll

def visualize_piano_roll(pianoroll_matrix,fName=None,fs=5):
    """ input: piano roll matrix with shape (number of notes, time steps)
        effect: generates a nice graph with the piano roll visualization
    """
    if(pianoroll_matrix.shape[0]==128):
        pianoroll_matrix=pianoroll_matrix.T.astype(float)
    track = pproll.Track(pianoroll=pianoroll_matrix, program=0, is_drum=False, name='piano roll')   
    # Plot the piano-roll
    fig, ax = track.plot(beat_resolution=fs)
    if fName:
        plt.savefig(fName)
        plt.close()
    else:
        plt.show()
