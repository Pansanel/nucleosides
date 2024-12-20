#!/usr/bin/env python

# Copyright 2022 CNRS and University of Strasbourg
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


"""Module to manage the application."""

import tkinter as tk
from tkinter import filedialog
from tkinter import ttk

import pkg_resources

from nucleosid import analysis_writer
from nucleosid import info_dialog
from nucleosid import mgf_data_analyzer
from nucleosid import mgf_parser
from nucleosid import modification_database_parser as db_parser

NAME = "Nucleos'ID"
DESCRIPTION = "Identifies RNA post-transcriptionnal modifications at " + \
              "nucleosides level."
VERSION = '1.0.0'
DEFAULT_THRESHOLD_INTENSITY = 0
DEFAULT_MS_TOLERANCE = 0.02
DEFAULT_MS_MS_TOLERANCE = 0.5
DEFAULT_MS_MS_SCORE_THRESHOLD = 20
DEFAULT_EXCLUSION_TIME = 60


class NucleosidApplication:
    """This class permits to manage the NucleosID Tk Interface."""

    def __init__(self):
        """Initialize the application."""
        self.database_list = [
            "Archaea", "Eukaryota", "Eubacteria", "Archaea_Eubacteria",
            "Archaea_Eukaryota", "Eubacteria_Eukaryota",
            "Archaea_Eubacteria_Eukaryota"
        ]
        self.ms_tolerance_types = ["Da", "ppm"]
        self.ms_ms_tolerance_types = ["Da", "ppm"]
        self.root = tk.Tk()
        icon_file = pkg_resources.resource_filename(
            'nucleosid', 'images/nucleosid-icon.png'
        )
        self.root.iconphoto(True, tk.PhotoImage(file=icon_file))
        self.root.title(NAME)
        self.root.grid()
        self.create_widgets()

    def run(self):
        """Run the application."""
        self.root.mainloop()

    def select_input_file(self):
        """Select the input file and update the innput_file entry."""
        input_file_path = filedialog.askopenfilename(
            title="Select the input file",
            filetypes=[('mgf files', '.mgf'), ('txt files', '.txt')]
        )
        self.input_file.delete(0, 'end')
        self.input_file.insert(0, input_file_path)

    def select_output_file(self):
        """Select the output file and update the output_file entry."""
        output_file_path = filedialog.asksaveasfilename(
            title="Select the output file",
            filetypes=[
                ('csv files', '.csv'), ('xlsx file', '.xlsx')
            ]
        )
        if output_file_path[-4:] in ['.csv', 'xlsx']:
            self.output_file.delete(0, 'end')
            self.output_file.insert(0, output_file_path)

    def show_about(self):
        """Open a simple dialog window and give some information."""
        title = "About Nucleos'ID"
        message = (
            f"Nucleos'ID - version {VERSION}\n\n"
            "Nucleos'ID is a software for untargeted identification of RNA\n"
            "post-transcriptional modifications from MS/MS acquisitions.\n\n"
            "Further details about this software can be obtained on:\n"
            "https://github.com/MSARN/NucleosID"
        )
        info_dialog.InfoDialog(
            self.root,
            title=title,
            text=message,
        )

    def analyze(self):
        """Analyze the input file and write the output file."""
        analysis_parameters = {
            'ms_tolerance': float(self.ms_tolerance.get()),
            'ms_tolerance_type': str(self.ms_tolerance_type.get()),
            'ms_ms_tolerance': float(self.ms_ms_tolerance.get()),
            'ms_ms_tolerance_type': str(self.ms_ms_tolerance_type.get()),
            'ms_ms_score_threshold': float(self.ms_ms_score_threshold.get()),
            'exclusion_time': float(self.exclusion_time.get())
        }
        mgf_data_parser = mgf_parser.MgfParser(self.input_file.get())
        database_file = pkg_resources.resource_filename(
            'nucleosid', 'databases/' + self.database.get() + '.csv'
        )
        modification_db_parser = db_parser.ModificationDatabaseParser(
            database_file
        )
        data_analyzer = mgf_data_analyzer.MGFDataAnalyzer(
            mgf_data_parser.get_ms_ms_spectra(),
            modification_db_parser.get_modification_database(),
            analysis_parameters
        )
        data_analyzer.find_arn_modifications()
        results = data_analyzer.get_analysis()
        if not results.empty:
            # Write output only if hits have been found
            output = analysis_writer.AnalysisWriter(results)
            if self.output_file.get()[-5:] == '.xlsx':
                output.write_analysis(self.output_file.get(), 'xlsx')
            else:
                # Save as CSV file by default
                output.write_analysis(self.output_file.get())
            message = (
                "The analysis is successful. The output has been saved to:\n"
                f"{self.output_file.get()}\n\n"
                f"{len(results)} matching RNA modifications have been found\n"
                f"{data_analyzer.filtered_number} hits have been filtered"
                " out using the given filters\n"
            )
        else:
            message = (
                "No ARN modifications could be found using the given\n"
                "parameters."
            )
        title = "Analysis Results"
        info_dialog.InfoDialog(
            self.root,
            title=title,
            text=message
        )

    def create_widgets(self):
        """Create the widgets."""
        # Create the left panel
        self.left_frame = tk.Frame(
            self.root, bg="white", relief='ridge', borderwidth=2
        )
        self.canvas = tk.Canvas(
            self.left_frame, bg="white",
            width=128, highlightthickness=0
        )
        self.canvas.grid()
        logo_path = pkg_resources.resource_filename(
            'nucleosid', 'images/nucleosid-logo.png'
        )
        self.logo = tk.PhotoImage(file=logo_path)
        self.canvas.create_image(0, 0, image=self.logo, anchor="nw")
        self.left_frame.pack(side='left', fill='y', padx=5, pady=5)

        # Create the header
        self.right_frame = tk.Frame(self.root)
        self.right_frame.pack()
        self.title = tk.Label(
            self.right_frame, text=NAME, font=("Arial 24 bold")
        )
        self.title.pack(padx=8, pady=8)
        self.description = tk.Label(
            self.right_frame, text=DESCRIPTION, font=("Arial 12 italic")
        )
        self.description.pack(padx=5, pady=5)

        # Create the input box
        self.lf1 = tk.LabelFrame(self.right_frame, text="Input")
        self.lf1.pack(fill='x', padx=5, pady=5)
        self.input_file_label = tk.Label(self.lf1, text="Input file:")
        self.input_file_label.grid(row=0, column=0, sticky='w')
        self.input_file = tk.Entry(self.lf1, width=32, bg="white")
        self.input_file.grid(row=0, column=1, sticky='w', padx=2, pady=2)
        self.input_file_selection = tk.Button(
            self.lf1, text="Browse file", command=self.select_input_file
        )
        self.input_file_selection.grid(row=0, column=2, padx=2, pady=2)

        # Create the output box
        self.lf2 = tk.LabelFrame(self.right_frame, text="Output")
        self.lf2.pack(fill='x', padx=5, pady=5)
        self.output_file_label = tk.Label(self.lf2, text="Output file:")
        self.output_file_label.grid(row=0, column=0, sticky='w')
        self.output_file = tk.Entry(self.lf2, width=32, bg="white")
        self.output_file.grid(row=0, column=1, sticky='w', padx=2, pady=2)
        self.output_file_selection = tk.Button(
            self.lf2, text="Browse file", command=self.select_output_file
        )
        self.output_file_selection.grid(row=0, column=2, padx=2, pady=2)

        # Create the settings box
        self.lf3 = tk.LabelFrame(self.right_frame, text="Settings")
        self.lf3.pack(fill='x', padx=5, pady=5)
        self.database_location_label = tk.Label(
            self.lf3, text="Database:"
        )
        self.database_location_label.grid(row=0, column=0, sticky='w')
        self.database = ttk.Combobox(
            self.lf3, values=self.database_list, state='readonly', width=27
        )
        self.database.current(6)
        self.database.grid(row=0, column=1, sticky='w', padx=2, pady=2)
        # MS Tolerance
        self.ms_tolerance_label = tk.Label(self.lf3, text="MS mass tolerance:")
        self.ms_tolerance_label.grid(
            row=1, column=0, sticky='w', padx=2, pady=2
        )
        self.ms_tolerance_frame = tk.Frame(self.lf3)
        self.ms_tolerance_frame.grid(
            row=1, column=1, sticky='w', padx=2, pady=2
        )
        self.ms_tolerance = tk.Entry(
            self.ms_tolerance_frame, width="6", bg="white", justify="right"
        )
        self.ms_tolerance.insert(0, DEFAULT_MS_TOLERANCE)
        self.ms_tolerance.pack(side='left')
        self.ms_tolerance_type = ttk.Combobox(
            self.ms_tolerance_frame, values=self.ms_tolerance_types,
            state='readonly', width="4"
        )
        self.ms_tolerance_type.current(0)
        self.ms_tolerance_type.pack(side='right', padx=2)

        # MS MS Tolerance
        self.ms_ms_tolerance_label = tk.Label(
            self.lf3, text="MS/MS mass tolerance:"
        )
        self.ms_ms_tolerance_label.grid(
            row=2, column=0, sticky='w', padx=2, pady=2
        )
        self.ms_ms_tolerance_frame = tk.Frame(self.lf3)
        self.ms_ms_tolerance_frame.grid(
            row=2, column=1, sticky='w', padx=2, pady=2
        )
        self.ms_ms_tolerance = tk.Entry(
            self.ms_ms_tolerance_frame, width="6", bg="white", justify="right"
        )
        self.ms_ms_tolerance.insert(0, DEFAULT_MS_MS_TOLERANCE)
        self.ms_ms_tolerance.pack(side='left')
        self.ms_ms_tolerance_type = ttk.Combobox(
            self.ms_ms_tolerance_frame, values=self.ms_ms_tolerance_types,
            state='readonly', width="4"
        )
        self.ms_ms_tolerance_type.current(0)
        self.ms_ms_tolerance_type.pack(side='right', padx=2)

        # Create the filter box
        self.lf4 = tk.LabelFrame(self.right_frame, text="Filters")
        self.lf4.pack(fill='x', padx=5, pady=5)
        # Intensity threshold
        self.ms_ms_intensity_threshold_label = tk.Label(
            self.lf4, text="MS/MS intensity threshold:"
        )
        self.ms_ms_intensity_threshold_label.grid(row=0, column=0, sticky='w')
        self.ms_ms_intensity_threshold = tk.Entry(
            self.lf4, width=6, bg="white", justify="right"
        )
        self.ms_ms_intensity_threshold.insert(0, DEFAULT_THRESHOLD_INTENSITY)
        self.ms_ms_intensity_threshold.grid(row=0, column=1, padx=2, pady=2)
        self.ms_ms_intensity_threshold_unit = tk.Label(self.lf4, text="AU")
        self.ms_ms_intensity_threshold_unit.grid(
            row=0, column=2, sticky='w', padx=2, pady=2
        )
        # MS MS score threshold
        self.ms_ms_score_threshold_label = tk.Label(
            self.lf4, text="MS/MS score threshold:"
        )
        self.ms_ms_score_threshold_label.grid(
            row=1, column=0, sticky='w', padx=2, pady=2
        )
        self.ms_ms_score_threshold = tk.Entry(
            self.lf4, width=6, bg="white", justify="right"
        )
        self.ms_ms_score_threshold.insert(0, DEFAULT_MS_MS_SCORE_THRESHOLD)
        self.ms_ms_score_threshold.grid(row=1, column=1, padx=2, pady=2)
        self.ms_ms_score_threshold_unit = tk.Label(self.lf4, text="%")
        self.ms_ms_score_threshold_unit.grid(
            row=1, column=2, sticky='w', padx=2, pady=2
        )
        # Exclusion time
        self.exclusion_time_label = tk.Label(
            self.lf4, text="Exclusion time:"
        )
        self.exclusion_time_label.grid(
            row=2, column=0, sticky='w', padx=2, pady=2
        )
        self.exclusion_time = tk.Entry(
            self.lf4, width=6, bg="white", justify="right"
        )
        self.exclusion_time.insert(0, DEFAULT_EXCLUSION_TIME)
        self.exclusion_time.grid(row=2, column=1, padx=2, pady=2)
        self.exclusion_time_unit = tk.Label(self.lf4, text="s")
        self.exclusion_time_unit.grid(
            row=2, column=2, sticky='w', padx=2, pady=2
        )

        # Create the buttons
        self.lf5 = tk.Frame(self.right_frame)
        self.lf5.pack(expand=True, padx=5, pady=5)
        self.run_button = tk.Button(
            self.lf5, text='Analyze',
            command=self.analyze
        )
        self.run_button.pack(side='left', padx=5, pady=2)
        self.help_button = tk.Button(
            self.lf5, text='About',
            command=self.show_about
        )
        self.help_button.pack(side='left', padx=5, pady=2)
        self.quit_button = tk.Button(
            self.lf5, text='Quit',
            command=self.right_frame.quit
        )
        self.quit_button.pack(side='left', padx=5, pady=2)


def main():
    """Analzyzes Main function for the Nucleos'ID application. Handles command.

    line arguments and loads configuration before launching the
    application window.
    """
    app = NucleosidApplication()
    app.run()


if __name__ == '__main__':
    main()
