import pandas as pd
import argparse
import re
import sys

class Signal:
    def __init__(self, sig_name, bit_src='0', bit_dest='0', parameters={}):
        self.sig_name = sig_name
        self.bit_src = bit_src
        self.bit_dest = bit_dest
        self.parameters = parameters
        self.width = abs(self.getSigValue(bit_src)-self.getSigValue(bit_dest)) + 1
        
    def getSigValue(self, sig_side_string):
        if sig_side_string.isnumeric():
            return int(sig_side_string)
        pattern = r"([-+/*]|\w+)"
        tokens = re.findall(pattern, sig_side_string)
        tokens = [str(self.parameters[token]) if token in self.parameters else token for token in tokens]
        try:
            sig_string_result = eval(''.join(tokens))
        except Exception as e:
            print(f'Sigal define error in {sig_side_string}')
        return sig_string_result

    def getSigName(self):
        return self.sig_name
    
    def getSigWidth(self):
        return self.width

    def __str__(self):
        return self.sig_name if self.width == 1 else f'[{abs(self.getSigValue(self.bit_src)-self.getSigValue(self.bit_dest))-1}:{self.bit_dest}] {self.sig_name}' if self.bit_src.isnumeric() else f'[{self.bit_src}:{self.bit_dest}] {self.sig_name}'

    def __lt__(self, other):
        return self.sig_name < other.sig_name

class Module:
    def __init__(self, module_name, module_instance = None):
        self.module_name = module_name
        self.module_instance = module_instance if module_instance else f'{module_name}_0'

    def getInstanceName(self):
        return self.module_instance

    def __eq__(self, other):
        return self.module_name == other.module_name

    def __hash__(self):
        return hash(self.module_name)

    def __str__(self):
        return self.module_name
class VerilogCodeGenerator:
    def __init__(self, file_path):
        self.file_path = file_path
        self.module_xls = pd.ExcelFile(self.file_path)
        self.module_deploy = self.module_xls.sheet_names[1]
        self.upper_module = self.clean_module_name(self.module_deploy)
        self.module_deploy_data = self.read_sheet(sheet_name = self.module_deploy)
        self.module_io = self.generate_module_io()
        
    def read_sheet(self, sheet_name=None):
        return self.module_xls.parse(sheet_name=sheet_name, header=None).values.tolist()

    @staticmethod
    def clean_module_name(module_name):
        clean_module_pattern = r"([^:()]*)(?::([^()]*)\(?([^()]*\)))?"
        match = re.match(clean_module_pattern, module_name)
        if match:
            cleaned_name = "".join([char for char in match.group(1) if char.isupper() or char == '_' or char.isnumeric()])
            return Module(cleaned_name, match.group(2))
        else:
            print('Please check module naming.')
            sys.exit(1)
    
    @staticmethod
    def create_sig_info(sig, parameters):
        sig = sig.strip().replace(",", "")
        pattern = r"(\w*)\s*:?\s*(\w*)\s*\[?(\w*-?\w*)?:?(\w*-?\w*)\]?"
        match = re.match(pattern, sig)
        if match.group(3) and match.group(4):
            return Signal(match.group(1), match.group(3), match.group(4), parameters)
        elif match.group(2).isnumeric():
            return Signal(match.group(1), str(match.group(2)), '0', parameters)
        elif not match.group(2):
            return Signal(match.group(1))
        elif match.group(2):
            return Signal(match.group(1), match.group(2) + '-1', '0', parameters)
    @staticmethod
    def create_parameter_info(moduleParameterStrings):
        moduleParameters = {}
        moduleParameterStrings = re.split(r',|\n| ',moduleParameterStrings)
        for moduleParameter in moduleParameterStrings:
            if moduleParameter != '':
                moduleParameterName, moduleParameterValue = moduleParameter.split("=")
                moduleParameters[moduleParameterName] = moduleParameterValue
        return moduleParameters

    def generate_module_io(self):
        src_module_names = []
        dest_module_names = []
        original_module_names = []
        module_io = {}
        module_content_startwith = 0
        
        #Get each side module
        for i in range(0, len(self.module_deploy_data[0:])):
            if self.module_deploy_data[i][0] == 'MODULES':
                module_content_startwith = i + 1
                break
        header = self.module_deploy_data[module_content_startwith - 1]
        for i in range(1, len(header)):
            if pd.isnull(header[i]) or header[i].isspace():
                break
            cleaned_name = self.clean_module_name(header[i])
            src_module_names.append(cleaned_name)
        for row in self.module_deploy_data[module_content_startwith:]:
            if pd.isnull(row[0]) or row[0].isspace():
                break
            cleaned_name = self.clean_module_name(row[0])
            if cleaned_name in src_module_names:
                dest_module_names.append(cleaned_name)
            else: 
                print(f'Please check your spec table, maybe some module not match between src and dest.')
                sys.exit(1)
        original_module_names = src_module_names + dest_module_names
        original_module_names.append(self.upper_module)
        
        for cleaned_module_name in original_module_names:
            module_io[cleaned_module_name] = {"inputs": set(), "outputs": set(), "parameters": {}}

        for row in self.module_deploy_data[1:]:
            module_content = str(row[0])
            if module_content == "PRI_PARAMETER":
                for i in range(1, len(row)):
                    if pd.notnull(row[i]) and row[i] not in ["N/A", "NA", ""]:
                        module_io[self.upper_module]['parameters'].update(self.create_parameter_info(row[i]))
            elif module_content == "SEC_PARAMETER":
                for i in range(1, len(row)):
                    module_name = src_module_names[i - 1]
                    if pd.notnull(row[i]) and row[i] not in ["N/A", "NA", ""]:
                       module_io[module_name]['parameters'].update(self.create_parameter_info(row[i]))

        for row in self.module_deploy_data[1:]:
            module_content = str(row[0])
            if module_content in ("PRIMARY_INPUT", "PRIMARY_OUTPUT"):
                io_type = "inputs" if module_content == "PRIMARY_INPUT" else "outputs"
                for i in range(1, len(row)):
                    module_name = src_module_names[i - 1]
                    if pd.notnull(row[i]) and row[i] not in ["N/A", "NA", ""]:
                        sigs = [self.create_sig_info(sig, module_io[module_name]['parameters']) for sig in row[i].split("\n") if sig and sig!='' and not sig.isspace()]
                        module_io[module_name][io_type].update(sigs)
                        module_io[self.upper_module][io_type].update(sigs)
            elif module_content in ("USE_CMDLINE_CLOCK", "USE_CMDLINE_RESET"):
                sig = 'REFCLK' if self.clean_module_name(module_content) == "USE_CMDLINE_CLOCK" else 'RST_N'
                for i in range(1, len(row)):
                    module_name = src_module_names[i - 1]
                    if row[i] == 'Y':
                        module_io[module_name]["inputs"].add(self.create_sig_info(sig, module_io[module_name]['parameters']))
            elif module_content.startswith("ADD_MOD_PORT"):
                sig = module_content.removeprefix("ADD_MOD_PORT: ")
                for i in range(1, len(row)):
                    module_name = src_module_names[i - 1]
                    if row[i] == 'Y':
                        module_io[module_name]["inputs"].add(self.create_sig_info(sig, module_io[module_name]['parameters']))
            elif self.clean_module_name(module_content) in original_module_names:
                dest_module_name = self.clean_module_name(module_content)
                for i in range(1, len(row)):
                    src_module_name = src_module_names[i - 1]
                    if pd.notnull(row[i]) and row[i] not in ["N/A", "NA", ""] and dest_module_name:
                        sigs = [self.create_sig_info(sig, module_io[module_name]['parameters']) for sig in row[i].split("\n") if sig and sig!='' and not sig.isspace()]
                        module_io[src_module_name]["outputs"].update(sigs)
                        module_io[dest_module_name]["inputs"].update(sigs)
        return module_io
    
    def generate_verilog_code_upper_module(self, prefix_string = ""):
        verilog_code = ""
        verilog_code += f"module {str(self.upper_module)} "
        if self.module_io[self.upper_module]["parameters"]:
            verilog_code += f"#("
            module_line = verilog_code
            verilog_code += f"parameter " + f",\n{' ':>{len(module_line)}}parameter ".join(f'{moduleParameterName} = {moduleParameterValue}' for moduleParameterName, moduleParameterValue in self.module_io[self.upper_module]["parameters"].items())
            verilog_code += f")"
        verilog_code += f"\n("
        if self.module_io[self.upper_module]["inputs"]:
            verilog_code += "\n\tinput wire " + ",\n\tinput wire ".join(str(sig) for sig in sorted(self.module_io[self.upper_module]["inputs"]))
        if self.module_io[self.upper_module]["outputs"]:
            verilog_code += "\n\toutput wire " + ",\n\toutput wire ".join(str(sig) for sig in sorted(self.module_io[self.upper_module]["outputs"]))
        verilog_code += f"\n);\n"
        for module_name in self.module_io.keys():
            if module_name == self.upper_module:
                continue
            verilog_code += self.generate_instance_verilog_code(module_name, prefix_string)
        verilog_code += f"endmodule //{str(self.upper_module)}\n"
        return verilog_code

    def generate_verilog_code(self, module_name):
        module_name = self.clean_module_name(module_name)
        verilog_code = ""
        verilog_code += f"module {module_name} "
        if self.module_io[module_name]["parameters"]:
            verilog_code += f"#("
            module_line = verilog_code
            verilog_code += f"parameter " + f",\n{' ':>{len(module_line)}}parameter ".join(f'{moduleParameterName} = {moduleParameterValue}' for moduleParameterName, moduleParameterValue in self.module_io[module_name]["parameters"].items())
            verilog_code += f")"
        verilog_code += f"\n("
        if self.module_io[module_name]["inputs"]:
            verilog_code += "\n\tinput wire " + ",\n\tinput wire ".join(str(sig) for sig in sorted(self.module_io[module_name]["inputs"]))
        if self.module_io[module_name]["outputs"]:
            verilog_code += "\n\toutput wire " + ",\n\toutput wire ".join(str(sig) for sig in sorted(self.module_io[module_name]["outputs"]))
        verilog_code += f"\n);\n\nendmodule //{module_name}\n\n"
        return verilog_code
    
    def generate_dummy_io_verilog_code(self, module_name):
        module_name = self.clean_module_name(module_name)
        verilog_code = ""
        verilog_code += f"module {module_name} "
        if self.module_io[module_name]["parameters"]:
            verilog_code += f"#("
            module_line = verilog_code
            verilog_code += f"parameter " + f",\n{' ':>{len(module_line)}}parameter ".join(f'{moduleParameterName} = {moduleParameterValue}' for moduleParameterName, moduleParameterValue in self.module_io[module_name]["parameters"].items())
            verilog_code += f")"
        verilog_code += f"\n("
        if self.module_io[module_name]["inputs"]:
            verilog_code += "\n\tinput wire " + ",\n\tinput wire ".join(str(sig) for sig in sorted(self.module_io[module_name]["inputs"]))
        if self.module_io[module_name]["outputs"]:
            verilog_code += "\n\toutput wire " + ",\n\toutput wire ".join(str(sig) for sig in sorted(self.module_io[module_name]["outputs"]))
        verilog_code += f"\n);"
        if self.module_io[module_name]["inputs"]:
            verilog_code += "\nAssign " + "\nAssign ".join(sig.getSigName() + " = " + str(sig.getSigWidth()) + "'b" + '0'*sig.getSigWidth() + ';' for sig in sorted(self.module_io[module_name]["inputs"]))
        if self.module_io[module_name]["outputs"]:
            verilog_code += "\nAssign " + "\nAssign ".join(sig.getSigName() + " = " + str(sig.getSigWidth()) + "'b" + '0'*sig.getSigWidth() + ';' for sig in sorted(self.module_io[module_name]["outputs"]))
        verilog_code += f"\n\nendmodule //{module_name}"
        return verilog_code
    
    def generate_instance_verilog_code(self, module_name, prefix_string=""):
        module_name = self.clean_module_name(module_name)
        verilog_code = ""
        parameter_line_len = 0
        if self.module_io[module_name]["inputs"]:
            verilog_code += "wire " + ";\nwire ".join(str(sig) for sig in sorted(self.module_io[module_name]["inputs"]))
        if self.module_io[module_name]["outputs"]:
            verilog_code += "wire " + ";\nwire ".join(str(sig) for sig in sorted(self.module_io[module_name]["outputs"]))
        module_line = f"{module_name}"
        verilog_code += "\n" + module_line
        if self.module_io[module_name]["parameters"]:
            module_line = f"{module_name} #("
            verilog_code += f" #("
            verilog_code += f"" + f",\n{' ':>{len(module_line)}}".join(f'.{moduleParameterName}({moduleParameterValue})' for moduleParameterName, moduleParameterValue in self.module_io[module_name]["parameters"].items())
            verilog_code += f")"
            parameter_line_len = len(list(self.module_io[module_name]["parameters"].keys())[-1]) + len(self.module_io[module_name]["parameters"][list(self.module_io[module_name]["parameters"].keys())[-1]])
        verilog_code += f"{prefix_string}{module_name} (\n"
        parameter_line_len += len(f"{module_name} #( ){prefix_string}{module_name}(")
        if self.module_io[module_name]["inputs"]:
            verilog_code += f"{' ':>{parameter_line_len}}"
            verilog_code += f"{' ':>{parameter_line_len}}".join('.' + sig.getSigName() + ' (' + sig.getSigName() + ').\n' for sig in sorted(self.module_io[module_name]["inputs"]))
        if self.module_io[module_name]["outputs"]:
            verilog_code += f"{' ':>{parameter_line_len}}"
            verilog_code += f"{' ':>{parameter_line_len}}".join('.' + sig.getSigName() + ' (' + sig.getSigName() + ').\n' for sig in sorted(self.module_io[module_name]["outputs"]))
        verilog_code += f"{' ':>{parameter_line_len}});"
        return verilog_code

    def save_to_file(self, verilog_code, output_file):
        with open(output_file, 'w') as f:
            f.write(verilog_code)

    def output_verilog_code_upper_module(self, file_output_name, prefix_string=""):
        top_module_content = ""
        for module_name in self.module_io.keys():
            verilog_code = self.generate_verilog_code(module_name)
            top_module_content += verilog_code + '\n'
            output_file = f'{module_name}.v'
            self.save_to_file(verilog_code, output_file)
        top_module_content = self.generate_verilog_code_upper_module(prefix_string)
        output_file = f'{self.module_deploy}.v'
        self.save_to_file(top_module_content, file_output_name)

    def output_verilog_code(self, module_name=None):
        verilog_code = self.generate_verilog_code(module_name)
        output_file = f'{module_name}.v'
        self.save_to_file(verilog_code, output_file)

    def output_instance_verilog_code(self, module_name=None, prefix_string=""):
        if module_name is None:
            for module_name in self.module_io.keys():
                verilog_code = self.generate_instance_verilog_code(module_name, prefix_string)
                output_file = f'{module_name}.instance.v'
                self.save_to_file(verilog_code, output_file)
        else:
            verilog_code = self.generate_instance_verilog_code(module_name, prefix_string)
            output_file = f'{module_name}.instance.v'
            self.save_to_file(verilog_code, output_file)
    def output_dummy_io_verilog_code(self, module_name=None):
        if module_name is None:
            for module_name in self.module_io.keys():
                verilog_code = self.generate_dummy_io_verilog_code(module_name)
                output_file = f'{module_name}.dummy_io.v'
                self.save_to_file(verilog_code, output_file)
        else:
            verilog_code = self.generate_dummy_io_verilog_code(module_name)
            output_file = f'{module_name}.dummy_io.v'
            self.save_to_file(verilog_code, output_file)

def main():
    parser = argparse.ArgumentParser(description='Verilog Generator')
    parser.add_argument('-f', '--input-file', required=True, help='Input file path')
    parser.add_argument('-modi_prefix', '--prefix-string', help='Control the prefix string for user module’s instance name')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-m', '--module-name', help='Only generate specified module header and instance file. If not used, all modules will be generated.')
    group.add_argument('-o', '--upper-module-file-name', help='Specify the output file name of upper module; module name is the same as worksheet name in xxx.xls file.')

    args = parser.parse_args()
    generator = VerilogCodeGenerator(args.input_file)
    if args.upper_module_file_name:
        generator.output_verilog_code_upper_module(file_output_name=args.upper_module_file_name, prefix_string=args.prefix_string if args.prefix_string else "")
    elif args.module_name:
        generator.output_verilog_code(module_name=args.module_name if args.module_name else None)
        generator.output_instance_verilog_code(module_name=args.module_name if args.module_name else None, prefix_string=args.prefix_string if args.prefix_string else "")
        generator.output_dummy_io_verilog_code(module_name=args.module_name if args.module_name else None)
if __name__ == "__main__":
    main()
