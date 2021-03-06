import json
from plynx.graph.base_nodes import BaseBash


class Command(BaseBash):
    def __init__(self, node=None):
        super(Command, self).__init__(node)

    def run(self, preview=False):
        inputs = BaseBash._prepare_inputs(self.node.inputs, preview)
        parameters = BaseBash._prepare_parameters(self.node.parameters)
        outputs = BaseBash._prepare_outputs(self.node.outputs)
        logs = BaseBash._prepare_logs(self.node.logs)
        cmd_command = self.node.get_parameter_by_name('cmd').value
        cmd_array = [
            self._get_arguments_string('input', inputs),
            self._get_arguments_string('output', outputs),
            self._get_arguments_string('param', parameters),
            self._get_arguments_string('log', logs),
            cmd_command
        ]
        cmd_string = ';\n'.join(cmd_array)
        if preview:
            return cmd_string

        script_location = self._get_script_fname()
        with open(script_location, 'w') as script_file:
            script_file.write(cmd_string)

        res = self.exec_script(script_location, logs)

        self._postprocess_outputs(outputs)
        self._postprocess_logs(logs)

        return res

    def status(self):
        pass

    def kill(self):
        return self.kill_process()

    @staticmethod
    def get_base_name():
        return 'command'

    @staticmethod
    def _get_arguments_string(var_name, arguments):
        res = []
        res.append('declare -A {}'.format(var_name))
        for key, value in arguments.items():
            res.append('{}["{}"]={}'.format(var_name, key, Command._escape_bash(value)))
        return ';'.join(res)

    @staticmethod
    def _escape_bash(s):
        return json.dumps(s).replace("'", "\\'")
