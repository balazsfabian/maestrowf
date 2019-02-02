###############################################################################
# Copyright (c) 2017, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory
# Written by Francesco Di Natale, dinatale3@llnl.gov.
#
# LLNL-CODE-734340
# All rights reserved.
# This file is part of MaestroWF, Version: 1.0.0.
#
# For details, see https://github.com/LLNL/maestrowf.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
###############################################################################

"""Abstract interfaces for interacting with schedulers."""
from abc import ABCMeta, abstractmethod
import logging
import six

LOGGER = logging.getLogger(__name__)


@six.add_metaclass(ABCMeta)
class BatchInterface(object):
    """
    An interface for general interactions with a batch scheduler.

    This interface provides a general class interface for submitting to HPC
    scheduler systems. The general responsibilities are as follows:
        - Submission of a script
        - Header generation for scripts when requested
        - Job cancellation
        - Job status collection
    """

    @abstractmethod
    def get_header(self, batch_info, resources):
        """
        Generate the header present at the top of execution scripts.

        :param batch_info: A dictionary containing general batch information.
        :param resoruces: A collection of requested resources.
        :returns: A string of the header based on internal batch parameters and
        the parameter step.
        """
        pass

    @abstractmethod
    def check_jobs(self, joblist):
        """
        For the given job list, query execution status.

        :param joblist: A list of job identifiers to be queried.
        :returns: The return code of the status query, and a dictionary of job
        identifiers to their status.
        """
        pass

    @abstractmethod
    def cancel_jobs(self, joblist):
        """
        For the given job list, cancel each job.

        :param joblist: A list of job identifiers to be cancelled.
        :returns: The return code to indicate if jobs were cancelled.
        """
        pass

    @abstractmethod
    def _state(self, job_state):
        """
        Map a scheduler specific job state to a Study.State enum.

        :param job_state: String representation of scheduler job status.
        :returns: A Study.State enum corresponding to parameter job_state.
        """
        pass

    @abstractmethod
    def submit(self, step, path, cwd, job_map=None, env=None):
        """
        Submit a script to the scheduler.

        If cwd is specified, the submit method will operate outside of the path
        specified by the 'cwd' parameter.
        If env is specified, the submit method will set the environment
        variables for submission to the specified values. The 'env' parameter
        should be a dictionary of environment variables.

        :param step: An instance of a StudyStep.
        :param path: Path to the script to be executed.
        :param cwd: Path to the current working directory.
        :param job_map: A map of workflow step names to their job identifiers.
        :param env: A dict containing a modified environment for execution.
        :returns: The return code of the submission command and job identiifer.
        """
        pass
