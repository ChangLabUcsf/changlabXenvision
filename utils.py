# -*- coding: utf-8 -*-
"""
Helper functions for analysis, plotting, and video display. Credit cited in
function documentation, otherwise written by JRL.

:Author: Jessie R. Liu (unless otherwise noted)
:Copyright: Copyright (c) 2021, Jessie R. Liu, All rights reserved.
"""
import pickle
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
import IPython.display as ipd
from base64 import b64encode
import seaborn as sns


def plot_trial_averages(sentence_num=1, participant_num=1):
    """
    This function plots the average brain activity for each electrode as
    well as the wavform of the sentence the participant was listening to.

    Parameters
    ----------
    sentence_num : int
        The sentence that the participant was listening to. Defaults to `1`,
        can be `1` or `2`.
    participant_num : int
        Which participant's brain activity to plot. Defaults to `1`, can be
        `1` or `2`.

    Returns
    -------
    Nothing, just displays the plot.
    """

    # Define the colors for each electrode.
    colors = sns.color_palette('husl')
    elec_colors = [colors[0], colors[1]]

    # Load the data.
    with open(f'data/P{participant_num}_data.pkl', 'rb') as f:
        data = pickle.load(f)[f'sentence{sentence_num}']

    # Setup the figure and set the title.
    fig, axs = plt.subplots(2, 1, figsize=(10, 5), sharex=True)
    axs[0].axes.set(title=data['text'])

    # Draw vertical and horizontal lines for each plot.
    for ax in axs.ravel():
        ax.axhline(y=0, linestyle=':', color='k')
        ax.axvline(x=0, linestyle=':', color='k')

    # Define the x-values for plotting the wavform.
    wavform_time = (np.arange(len(data['sound'])) / data['sound_sr']) - 0.5

    # Plot the wavform on the first subplot and add axes labels.
    axs[0].plot(wavform_time, data['sound'], color='k', linewidth=1, alpha=0.8)
    axs[0].axes.set(ylabel='Amplitude', title='Waveform')

    # Define the x-values for plotting the brain activity and compute the
    # trial averaged brain activity.
    ecog_time = (np.arange(data['ecog'].shape[1]) / data['ecog_sr']) - 0.5
    ecog_avg = data['ecog'].mean(0)

    # Plot the trial averaged brain activity for each electrode on the
    # second subplot.
    for cur_elec, elec in enumerate(data['electrodes']):
        axs[1].plot(ecog_time, ecog_avg[:, cur_elec], label=f'e{elec}',
                    color=elec_colors[cur_elec])

    # Add labels and format the legend.
    axs[1].axes.set(xlabel='Time from start of sentence (s)',
                    ylabel='Average electrical activity')
    axs[1].legend(frameon=False)
    fig.tight_layout();
    pass


def plot_multiple_trial_data(sentence_num=1, electrode_num=0,
                             participant_num=1):
    """
    Plots the first 5 individual trials for a given electrode, sentence,
    and participant.

    Parameters
    ----------
    sentence_num : int
        The sentence that the participant was listening to. Defaults to `1`,
        can be `1` or `2`.
    electrode_num : int
        Which electrode's activity to plot. Defaults to `0`, but can be `0`
        or `1`.
    participant_num : int
        Which participant's brain activity to plot. Defaults to `1`, can be
        `1` or `2`.

    Returns
    -------
    Nothing, just displays the plot.
    """

    # Define the colors for each electrode.
    colors = sns.color_palette('husl')
    elec_colors = [colors[0], colors[1]]

    # Load the data.
    with open(f'data/P{participant_num}_data.pkl', 'rb') as f:
        data = pickle.load(f)[f'sentence{sentence_num}']

    # Setup the figure and set the title.
    fig, axs = plt.subplots(5, 1, figsize=(6, 8), sharex=True, sharey=True)
    axs[0].axes.set(title=data['text'])

    # Draw vertical and horizontal lines for each plot.
    for ax in axs.ravel():
        ax.axhline(y=0, linestyle=':', color='k')
        ax.axvline(x=0, linestyle=':', color='k')

    # Define the x-values for plotting the brain activity.
    ecog_time = (np.arange(data['ecog'].shape[1]) / data['ecog_sr']) - 0.5

    # Plot each trial in it's own subplot.
    for cur_trial in range(5):
        # Get the brain activity for one trial and the specified electrode.
        ecog_trial = data['ecog'][cur_trial, :, electrode_num]

        # Plot the single trial and add a title to the subplot with the
        # trial number.
        axs[cur_trial].plot(ecog_time, ecog_trial,
                            color=elec_colors[electrode_num])
        axs[cur_trial].set_title(f'Trial # {cur_trial + 1}')

    # Add x and y labels.
    axs[0].set_ylabel('Electrical Response')
    axs[0].set_xlabel('Time from start of sentence (s)')
    fig.tight_layout();
    pass


def plot_single_trial_data(sentence_num=1, trial_num=0, participant_num=1):
    """
    Plot a single trial of each electrode's activity while a participant is
    listening to the specified sentence number.

    Parameters
    ----------
    sentence_num : int
        The sentence that the participant was listening to. Defaults to `1`,
        can be `1` or `2`.
    trial_num : int
        The trial number to plot. Defaults to `0` but can be any value
        between 0 and 10.
    participant_num : int
        Which participant's brain activity to plot. Defaults to `1`, can be
        `1` or `2`.

    Returns
    -------
    Nothing, just displays the plot.
    """

    # Define the colors for each electrode.
    colors = sns.color_palette('husl')
    elec_colors = [colors[0], colors[1]]

    # Load the data.
    with open(f'data/P{participant_num}_data.pkl', 'rb') as f:
        data = pickle.load(f)[f'sentence{sentence_num}']

    # Setup the figure and set the title.
    fig, axs = plt.subplots(1, 2, figsize=(13, 3), sharex=True)
    axs[0].axes.set(title=data['text'])

    # Draw vertical and horizontal lines for each plot.
    for ax in axs.ravel():
        ax.axhline(y=0, linestyle=':', color='k')
        ax.axvline(x=0, linestyle=':', color='k')
        ax.axes.set(ylabel='Strength of Electrical Activity',
                    xlabel='Time from start of sentence (s)')

    # Define the x-values for plotting the brain activity and select the
    # trial of brain activity.
    ecog_time = (np.arange(data['ecog'].shape[1]) / data['ecog_sr']) - 0.5
    ecog_trial = data['ecog'][trial_num, :]

    # Plot the activity for each electrode in separate subplots.
    for cur_elec, elec in enumerate(data['electrodes']):
        axs[cur_elec].plot(ecog_time, ecog_trial[:, cur_elec],
                           color=elec_colors[cur_elec])

    fig.tight_layout();
    pass


def get_sentence_text(sent_num):
    """
    Get the text for the specified sentence.

    Parameters
    ----------
    sent_num : int
        The sentence that the participant was listening to. Defaults to `1`,
        can be `1` or `2`.

    Returns
    -------
    The text of the sentence as a string.
    """
    with open('data/P1_data.pkl', 'rb') as f:
        data = pickle.load(f)
    return data[f'sentence{sent_num}']['text'].replace("`", "'")


def plot_wavform_and_spectrogram(sound, sr, title):
    """
    Plots the wavform and Short-time Fourier transform spectrogram of a
    given sound.

    Parameters
    ----------
    sound : 1d array
        The data corresponding to the wavform amplitude.
    sr : float or int
        The sampling rate of the sound.
    title : str
        The title of the plot, should be the text or label of the sound
        being plotted.

    Returns
    -------
    Nothing, just displays the plot.
    """

    # Trim the silence portion of the wavform.
    cutoff = np.where(sound != 0)[0][0]
    sound_cut = sound[cutoff:-cutoff]

    # Create the x-values for each timestamp of the sound data.
    sound_time = np.arange(len(sound_cut)) / sr

    # Set up the figure.
    fig, axs = plt.subplots(2, 1, figsize=(10, 8), constrained_layout=True,
                            sharex=True)

    # Plot the wavform in the first subplot.
    axs[0].plot(sound_time, sound_cut, 'black')
    axs[0].axes.set(ylabel='Amplitude', title=title)

    # Compute the spectrogram using the Short-time Fourier Transform.
    frequencies, times, spectrogram = signal.stft(sound_cut, fs=sr,
                                                  window='hann', nperseg=256,
                                                  noverlap=64)

    # Plot the spectrogram in the second subplot.
    im = axs[1].pcolormesh(times, frequencies, np.abs(spectrogram),
                           shading='auto', vmin=0, vmax=0.1, cmap='Spectral_r')
    axs[1].axes.set(xlabel='Time (s)', ylabel='Frequency (Hz)')
    cbar = fig.colorbar(im, ax=axs[1]);
    cbar.set_label('Loudness')
    pass


def play_brain_movie(sentence_number=1, speed='normal'):
    """
    Load pre-made .mp4 videos and play them in a Jupyter notebook. Should
    also work when using Google Colab.

    Parameters
    ----------
    sentence_number : int
        The sentence that the participant was listening to. Defaults to `1`,
        can be `1` or `2`.
    speed : str
        The playback speed of the video, either "normal" or "slow".

    Returns
    -------
    Nothing, just displays the movie.
    """

    # Raises an error if the sentence_number is incorrectly set.
    if sentence_number not in [1, 2]:
        raise ValueError(f'Sentence number can only be `1` or `2`, '
                         f'not {sentence_number}.')

    # Translates the speed into degree of speed reduction.
    if speed == 'normal':
        speed_int = 1
    elif speed == 'slow':
        speed_int = 4
    else:
        raise ValueError(f'Speed can only be "normal" or "slow", not {speed}.')

    # Define the path to the file.
    movie_path = f'media/brain_movie_sentence{sentence_number}_with_sound_' \
                 f'{speed_int}x.mp4'

    # Reads the file and displays in the notebook.
    mp4 = open(movie_path, 'rb').read()
    data_url = "data:video/mp4;base64," + b64encode(mp4).decode()
    ipd.display(ipd.HTML("""
    <video width=400 controls>
          <source src="{}" type="video/mp4">
    </video>
    """.format(data_url)))
    pass
