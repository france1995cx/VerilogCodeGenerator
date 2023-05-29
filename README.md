# Verilog Generator
This Python script allows you to automatically generate Verilog code from a given input file. This input file must be in a specific Excel format which includes details about various parameters and signals related to the modules. The script will parse this file and generate corresponding Verilog code for each module.

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Example](#example)
- [Support](#support)


## Features
Generation of Verilog code for each module in the input file.
Output Verilog code to .v files for each module.
Output instance Verilog code to .instance.v files for each module.
Output dummy IO Verilog code to .dummy_io.v files for each module.
The script can output Verilog code for all modules or a specified module based on the input arguments.

## Installation
How to Use
To use this script, clone this repository and then navigate to the directory where the Python script is located.

Make sure you have the necessary Python libraries installed. You can install them with:
pip install pandas argparse re sys os

## Usage
The script takes in the following command-line arguments:

-f or --input-file : This is a required argument where you must specify the path to your input Excel file.
-modi_prefix or --prefix-string : A prefix string for module instance generation.
-m or --module-name : The name of a specific module you want the Verilog code to be generated for.
-o or --upper-module-file-name : Specify the output file name of upper module; module name is the same as worksheet name in xxx.xls file.

## Example
To generate Verilog code for a specific module, you can use the following command:
python VerilogGenerator.py -f <path_to_your_input_file> -om <module_name>

To generate Verilog code for all modules, use:
python VerilogGenerator.py -f <path_to_your_input_file> -o <output_file_name>

Example xlsx file attached in Example folder

## Support
If you have any questions or run into any issues, please create an issue on this GitHub repository.
