# Copyright 2024 CNRS and University of Strasbourg
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""MS/MS spectrum test class."""

from nucleosid import ms_ms_spectrum


def test_set_title():
    """Test the set_title function."""
    spectrum = ms_ms_spectrum.MSMSSpectrum()
    spectrum.set_title('Test spectrum')
    assert spectrum.title == 'Test spectrum'


def test_set_rtinseconds():
    """Test the set_rtinseconds function."""
    spectrum = ms_ms_spectrum.MSMSSpectrum()
    spectrum.set_rtinseconds(10)
    assert spectrum.rtinseconds == 10


def test_set_pepmass():
    """Test the set_pepmass function."""
    spectrum = ms_ms_spectrum.MSMSSpectrum()
    spectrum.set_pepmass(100)
    assert spectrum.pepmass == 100


def test_set_charge():
    """Test the set_charge function."""
    spectrum = ms_ms_spectrum.MSMSSpectrum()
    spectrum.set_charge(3)
    assert spectrum.charge == 3


def test_append_peak():
    """Test the set_append_peak function."""
    spectrum = ms_ms_spectrum.MSMSSpectrum()
    spectrum.append_peak("A")
    spectrum.append_peak("B")
    assert len(spectrum.peaks) == 2


def test_get_exact_mass():
    """Test the get_exact_mass function."""
    spectrum = ms_ms_spectrum.MSMSSpectrum()
    spectrum.pepmass = 3.14
    exact_mass = spectrum.get_exact_mass()
    assert isinstance(exact_mass, float)
    assert exact_mass == 3.14

def test_get_rtinseconds():
    """Test the get_rtinseconds function."""
    spectrum = ms_ms_spectrum.MSMSSpectrum()
    spectrum.rtinseconds = 6.18
    rtinseconds = spectrum.get_rtinseconds()
    assert isinstance(rtinseconds, float)
    assert rtinseconds == 6.18


def test_get_peaks():
    """Test the get_peak function."""
    spectrum = ms_ms_spectrum.MSMSSpectrum()
    spectrum.peaks = ['A', 'B']
    peak_list = spectrum.get_peaks()
    assert isinstance(peak_list, list)
    assert peak_list == ['A', 'B']
