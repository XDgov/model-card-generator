import cmd


class ModelCardGenerator(cmd.Cmd):
    intro = " Welcome to the model card generator developed by xD|Census!\n\n This tool can be used to create a model card: a way to share information about a model's intent, data, architecture, and performance.\n\n To generate a markdown (*.md) file version of a model card, type \"begin\", hit enter, and enter the model\'s information as prompted.\n\n To exit the script at any time without saving the file, type \"exit\" and hit enter."
    prompt = '> '
    file = None
    model_name = None
    statements_dict = {
        'Accountability': ['Model name', 'Point of contact(s) and affiliations', 'Model acquisition/development method'],
        'Anticipated Use': ['Division(s) using the model', 'Intended application(s) and stakeholder(s) of the model'],
        'Model Information & Architecture': ['Current model version and release date', 'Changes made since the last release (if any)', 'License for use', 'Type of model (Classification, Regression, Object Detection etc.)', 'Type(s) of algorithm used'],
        'Dataset & Performance': ['Source(s) of the training data', 'Data collection/ generation method', 'Number of variables in this dataset', 'Number of entries in your dataset', 'Percent of data chosen as a training, testing and validation set', 'Metrics used to rate model performance', 'Factors that limit the model\'s performance. (Examples: Limited dataset, number of nulls/NAs) (if any)'],
        'Bias Identification & Mitigation': ['Inclusion of information related to individuals or human populations in the training/testing/validation dataset', 'Degree of risk of human judgement injecting bias within the workflow', 'Methods used to minimize bias from human judgement', 'Potential biases found in the training dataset from collection methods, sample size, representation, etc.', 'Testing/evaluation performed to look for bias in the workflow of the model', 'Degree of model explainability/transparency'],
        'Governance/Compliance': ['Model/dataset compliance with existing laws and regulations. (Including privacy protection regulations)']
    }

    def do_begin(self, arg):
        for key in self.statements_dict:
            # first section: initialize file
            if key == 'Accountability':
                self.accountability(arg)
            # last section: save file and exit
            elif key == 'Governance/Compliance':
                self.complete_file(arg)
            else:
                self.write_section(key)

    def write_section(self, section):
        self.file.write(f"## {section}\n")
        for segment in self.statements_dict[section]:
            input_val = input(f"{segment}\n")

            self.file.write(f"### {segment}\n")
            self.file.write(f"* {input_val}\n")

    def accountability(self, _arg):
        for section in self.statements_dict['Accountability']:
            if section == 'Model name':
                model_name = input(f"{section}\n")
                self.init_model_name(model_name)
            else:
                input_val = input(f"{section}\n")
                self.file.write(f"### {section}\n")
                self.file.write(f"* {input_val}\n")

    def init_model_name(self, name):
        self.model_name = name
        self.init_file()

    def init_file(self):
        filename = self.model_name

        self.file = open(f"{filename}.md", 'w')
        self.file.write(f"# {self.model_name} Model Card\n")
        self.file.write("## Accountability\n")
        self.file.write("### Model Name\n")
        self.file.write(f"* {self.model_name}\n")

    def complete_file(self, _arg):
        section = 'Governance/Compliance'
        self.file.write(f"## {section}\n")

        for segment in self.statements_dict[section]:
            input_val = input(f"{segment}\n")
            self.file.write(f"### {segment}\n")
            self.file.write(f"* {input_val}\n")

        self.close()
        exit()

    def do_exit(self, _arg):
        'Stop recording, close the tool, and exit'
        self.close()
        exit()

    def close(self):
        if self.file:
            self.file.close()
            self.file = None


if __name__ == '__main__':
    ModelCardGenerator().cmdloop()
