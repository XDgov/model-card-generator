import cmd
import os
import markdown


class ModelCardGenerator(cmd.Cmd):
    intro = " Welcome to the model card generator developed by xD|Census!\n\n This tool can be used to create a model card: a way to share information about a model's intent, data, architecture, and performance.\n\n To generate a markdown (*.md) file version of a model card, type \"begin\", hit enter, and enter the model\'s information as prompted.\n\n To exit the script at any time without saving the file, type \"exit\" and hit enter."
    prompt = '> '
    file = None
    name = None
    owner = None
    agency = None
    model = None
    example_dict = {
                    'Anticipated Use': ["In which agencies will this model be used?", "Who are the intended users of the model?", "What are the intended use cases of the model?"],
                    'Model Information': ["What is the current model version?", "What is the version release date?", "What changes have been made since the last release?", "What is the license for use?"],
                    'Model Architecture': ["What type of algorithm is used?", "How is the input data formatted?", "How is the output data formatted?"],
                    'Datasets': ["Does the training dataset contain information related to individuals or human populations?", "What is the source(s) of the training data?", "How was this data collected or generated?", "What variables are contained in this dataset?", "How many entries are contained in your dataset?", "What percent of data is chosen as a validation set?"],
                    'Performance Metrics': ["What metrics are used to rate model performance?", "How are the metrics being reported?", "What is the confidence interval of these metrics?", "What decision threshold was used to compute the metric?", "What factors limit the model's performance?"],
                    'Bias': ["Within the workflow of this model, are there concerns related to privacy or surveillance?", "What steps are taken to mitigate privacy and surveillance risks in the model architecture or use cases?", "Within the workflow of this model, is there risk of discrimination against protected classes: age, gender, race, sexuality, color, religion/creed, nationality, disability, veteran status, genetic information, or citizenship?", "What strategies are being used to address possible sources of discrimination in your model architecture or use cases?", "Within the workflow of this model, is there risk of human judgement injecting bias?", "What methods are used to minimize bias from human judgement?", "What biases are potentially found in the dataset from collection methods, historical unfairness, sample size, etc.?", "Are there variables that are influenced by or connected to protected classes? How is this relationship evaluated as a potential source of bias? Example: Gender vs Hair length", "How and when are biases in the dataset addressed in the workflow of the model?", "What testing has been performed to look for bias related to discrimination of protected classes?", "What testing has been performed to maximize fairness in the model’s learned behavior?", "What percentage of development time has been dedicated to bias mitigation?"]
    }
    information_dict = {'Anticipated Use': "ant use info", 'Model Information': "mod info info", 'Model Architecture': "mod arch info", 'Datasets':"dataset info", 'Performance Metrics':"perf metrics info", 'Bias':"bias info"}
    questions_dict = {
                    'Anticipated Use': ["In which agencies will this model be used?", "Who are the intended users of the model?", "What are the intended use cases of the model?"],
                    'Model Information': ["What is the current model version?", "What is the version release date?", "What changes have been made since the last release?", "What is the license for use?"],
                    'Model Architecture': ["What type of algorithm is used?", "How is the input data formatted?", "How is the output data formatted?"],
                    'Datasets': ["Does the training dataset contain information related to individuals or human populations?", "What is the source(s) of the training data?", "How was this data collected or generated?", "What variables are contained in this dataset?", "How many entries are contained in your dataset?", "What percent of data is chosen as a validation set?"],
                    'Performance Metrics': ["What metrics are used to rate model performance?", "How are the metrics being reported?", "What is the confidence interval of these metrics?", "What decision threshold was used to compute the metric?", "What factors limit the model's performance?"],
                    'Bias': [["Within the workflow of this model, are there concerns related to privacy or surveillance?", "What steps are taken to mitigate privacy and surveillance risks in the model architecture or use cases?", "Within the workflow of this model, is there risk of discrimination against protected classes: age, gender, race, sexuality, color, religion/creed, nationality, disability, veteran status, genetic information, or citizenship?", "What strategies are being used to address possible sources of discrimination in your model architecture or use cases?", "Within the workflow of this model, is there risk of human judgement injecting bias?", "What methods are used to minimize bias from human judgement?", "What biases are potentially found in the dataset from collection methods, historical unfairness, sample size, etc.?", "Are there variables that are influenced by or connected to protected classes? How is this relationship evaluated as a potential source of bias? Example: Gender vs Hair length", "How and when are biases in the dataset addressed in the workflow of the model?", "What testing has been performed to look for bias related to discrimination of protected classes?", "What testing has been performed to maximize fairness in the model’s learned behavior?", "What percentage of development time has been dedicated to bias mitigation?"], ["Within the workflow of this model, is there risk of human judgement injecting bias?", "What methods are used to minimize bias from human judgement?", "What biases are potentially found in the training dataset from collection methods, sample size, representation, etc.?", "What evaluation tools have been used to evaluate bias in the training dataset?", "How and when are biases in the dataset addressed in the workflow of the model?", "What testing has been performed to look for bias in the model?", "What percentage of development time has been dedicated to bias mitigation?"]]
    }
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
        self.model = name
        self.init_file()

    def init_file(self):
        filename = self.model

        self.file = open(f"{filename}.md", 'w')
        self.file.write(f"# {self.model} Model Card\n")
        self.file.write("## Accountability\n")
        self.file.write("### Model Name\n")
        self.file.write(f"* {self.model}\n")

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

    # # basic commands #
    # def do_name(self, arg):
    #     'Names of collaborators in a "+" separated list: name Jane Doe, Ph.D. + John Smith + Joe Schmo'
    #     temp_list = arg.split("+")
    #     for n in range(0, len(temp_list)):
    #         temp_list[n] = temp_list[n].strip()
    #     self.name = temp_list

    # def do_model(self, arg):
    #     'Model name: model Test Model Name'
    #     self.model = arg

    # def do_owner(self, arg):
    #     'Internally-built, off-the-shelf, or bespoke aquisition?: owner bespoke'
    #     types = ["Internally built", "Off-the-shelf", "Bespoke"]
    #     self.owner = types[int(arg) - 1]

    # def do_agency(self, arg):
    #     'Affiliated agency ("+" seperated list for multiple agencies): agency Census Bureau + xD'
    #     temp_list = arg.split("+")
    #     for n in range(0, len(temp_list)):
    #         temp_list[n] = temp_list[n].strip()
    #     self.agency = temp_list

    # def printinfo(self, _arg):
    #     'Displays the current inputs'
    #     print("Collaborators: ", self.name)
    #     print("Aquisition: ", self.owner)
    #     print("Affiliated Agency: ", self.agency)

    # def do_input(self, _arg):
    #     'Read input file: input'
    #     self.readInputTXT()
    #     try:
    #         with open(f'{self.model} Model Card.md', 'r') as f:
    #             text = f.read()
    #             html = markdown.markdown(text, output_format='html')

    #         with open('ModelCard.html', 'w') as f:
    #             f.write(html)
    #         f.close()
    #     except Exception:
    #         print("Unable to create HTML file")

    # def do_begin(self, _arg):
    #     'Begin content entry:  begin'

    #     m = input("What is your model name?\n")
    #     self.do_model(m)

    #     n = input("\nEnter names of model owners in a \"+\" seperated list. Example: Jane Doe, Ph.D. + John Smith\n")
    #     self.do_name(n)

    #     a = input("\nEnter affiliated agencies in a + seperated list. Example: xD + Census\n")
    #     self.do_agency(a)

    #     aq_flag = True
    #     o = input("\nHow was the model aquired:\n1. internally-built - Developed and maintained by employees of the intended user\n2. off-the-shelf - Existing model aquired and modified for new use case\n3. bespoke - Outside agency developed model for this specific use case\n")
    #     while aq_flag is True:

    #         if o.isnumeric():
    #             if int(o) > 0 and int(o) < 4:
    #                 self.do_owner(o)
    #                 aq_flag = False
    #         else:
    #             print("Invalid input")
    #             o = input("\nHow was the model aquired:\n1. internally-built - Developed and maintained by employees of the intended user\n2. off-the-shelf - Existing model aquired and modified for new use case\n3. bespoke - Outside agency developed model for this specific use case\n")

    #     form = input("\nIn what format would you like to input further responses:\n1. Command line\n2. Text document\n")

    #     form_FL = True
    #     human_flag = 0
    #     while form_FL is True:
    #         form = int(form)
    #         if form == 2:
    #             included_questions = {}

    #             for key in self.questions_dict.keys():
    #                 questions = self.questions_dict[key]
    #                 while key == "Bias" and human_flag not in ["1", "2"]:
    #                     human_flag = input("Does the training dataset contain information related to individuals or human populations?\n" + "1. Yes\n" + "2. No\n")
    #                     if human_flag == "1":
    #                         questions = self.questions_dict[key][0]
    #                     elif human_flag == "2":
    #                         questions = self.questions_dict[key][1]
    #                 q = "\n" + key + "\n"
    #                 for question in questions:
    #                     q = q + "     " + question + "\n"

    #                 q = q + "Include section? (Y/N)\n"

    #                 fl = True

    #                 while (fl):
    #                     y = input(q)

    #                     if y == "Y" or y == "y":
    #                         included_questions[key] = questions
    #                         fl = False
    #                     elif y == "N" or y == "n":
    #                         fl = False
    #                     else:
    #                         print("Invalid input")

    #             print("Section selection complete. Your file will now be populated.")
    #             self.populateTXT(included_questions)
    #             form_FL = False

    #         elif form == 1:

    #             included_questions = {}
    #             for key in self.questions_dict.keys():
    #                 q = "\n" + key + "\n"
    #                 print(q)
    #                 temp = {}
    #                 questions = self.questions_dict[key]
    #                 while key == "Bias" and human_flag not in ["1", "2"]:
    #                     human_flag = input("Does the training dataset contain information related to individuals or human populations?\n" + "1. Yes\n" + "2. No\n")
    #                     if human_flag == "1":
    #                         questions = self.questions_dict[key][0]
    #                     elif human_flag == "2":
    #                         questions = self.questions_dict[key][1]

    #                 for que_index in range(0, len(questions)):
    #                     question = questions[que_index]
    #                     ans = input(question + "\n")
    #                     while ans.lower() == "help":
    #                         self.examples(self, key, que_index)
    #                         ans = input(question + "\n")

    #                     if len(ans) > 1:
    #                         temp[question] = ans
    #                 if len(temp.keys()) > 0:
    #                     included_questions[key] = temp
    #             print("Questions completed. Your output file will now be populated.")
    #             output_form = input("\nIn what format would you like to output your model card responses:\n1. Markdown (.md)\n2. JSON (.json)\n3. Word (.docx)\n")
    #             while output_form not in ["1", "2", "3"]:
    #                 output_form = input("\nIn what format would you like to output your model card responses:\n1. Markdown (.md)\n2. JSON (.json)\n3. Word (.docx)\n")

    #             output_FL = True
    #             while output_FL is True:
    #                 output_form = int(output_form)
    #                 if output_form == 1:
    #                     self.do_bye(included_questions, 1)
    #                     output_FL = False
    #                 elif output_form > 1 and output_form < 4:
    #                     self.do_bye(included_questions, output_form + 3)
    #                     output_FL = False
    #                 else:
    #                     print("Invalid output form selected.\n")
    #                     output_form = input("\nIn what format would you like to output your model card responses:\n1. Markdown (.md)\n2. JSON (.json)\n 3. Word (.docx)\n")

    #             form_FL = False

    #         else:
    #             print("Invalid form choice")
    #             form = input("\nIn what format would you like to input further responses:\n1. Command line\n2. Word document\n 3. Text document\n")

    #     self.do_bye(included_questions, form)

    # def do_bye(self, arg, form):
    #     'Stop recording, close the tool, and exit:  bye'

    #     if form == 1:

    #         self.populateMD(arg)

    #     try:
    #         with open('ModelCard.md', 'r') as f:
    #             text = f.read()
    #             html = markdown.markdown(text)

    #         with open('ModelCard.html', 'w') as f:
    #             f.write(html)
    #         f.close()
    #     except Exception:
    #         print("Unable to create HTML file")
    #     print('Thank you for using the Model Card Generator. \n Type \'exit\' to leave the shell')
    #     return True

    # def examples(self, questionsDict, section, questionIndex):
    #     print("*****************************")
    #     print("\n")

    #     print("More information:\n")
    #     print(self.information_dict[section])

    #     print("\n")
    #     print("Question: " + self.questions_dict[section][questionIndex])
    #     print("Example Answer:\n")
    #     print(self.example_dict[section][questionIndex])
    #     print("*****************************")

    # def populateTXT(self, arg):
    #     file = open("ModelCardInputs.txt", "w")
    #     names = ""
    #     agents = ""
    #     for name in self.name:
    #         if names != "":
    #             names = names + "+" + str(name)
    #         else:
    #             names = str(name)
    #     file.write(str(names))
    #     file.write("\n")
    #     file.write(str(self.owner))
    #     file.write("\n")
    #     for agent in self.agency:
    #         if agents != "":
    #             agents = agents + "+" + str(agent)
    #         else:
    #             agents = str(agent)
    #     file.write(str(agents))
    #     file.write("\n")
    #     file.write(str(self.model))
    #     file.write("\n")

    #     file.write("Welcome to the model card generator input document. You may answer your selected questions below. Answers should be written in the sections delineated by '################' only. When finished, run the generator once more and run the command 'input'.\n")

    #     for section in arg.keys():
    #         file.write("*" + section + "*\n")
    #         file.write(self.information_dict[section])

    #         for index in range(0, len(arg[section])):
    #             file.write("+" + arg[section][index] + "+\n")
    #             file.write("Example Answer:\n")
    #             file.write(self.example_dict[section][index])
    #             file.write("\nEnter your response between the pound signs (#):")
    #             file.write("\n#")
    #             file.write("\n")
    #             file.write("#\n")

    #         file.write("")
    #         file.write("")
    #     file.close()

    # def readInputTXT(self):
    #     if os.path.isfile("ModelCardInputs.txt"):
    #         file = open("ModelCardInputs.txt", "r")
    #         data = file.read()
    #         file.close()

    #         vars = data.split("\n")
    #         self.name = vars[0].split("+")
    #         self.owner = vars[1]
    #         self.agency = vars[2].split("+")
    #         self.model = vars[3]

    #         included_questions = {}
    #         temp = {}

    #         current_section = None
    #         current_question = None

    #         sections = data.split("*")
    #         for s in range(0, len(sections)):
    #             if s % 2 == 0 and s != 0:
    #                 questions = sections[s].split("+")
    #                 for q in range(0, len(questions)):
    #                     if q % 2 ==0 and q != 0:
    #                         answers = questions[q].split("#")
    #                         for a in range(0, len(answers)):
    #                             if a % 2 != 0 and a != 0 and current_question is not None:
    #                                 temp[current_question] = answers[a]
    #                     elif q == 0:
    #                         continue
    #                     else:
    #                         current_question = questions[q]
    #             else:
    #                 if s == 0:
    #                     continue
    #                 elif current_section is None:
    #                     included_questions[current_section] = temp
    #                     temp = {}
    #                     current_section = sections[s]
    #                 else:
    #                     current_section = sections[s]
    #         included_questions[current_section] = temp
    #         self.populateMD(included_questions)
    #         print("Markdown file created.")

    #     else:
    #         print("Unable to open ModelCardInputs.txt")

    # def populateMD(self, arg):
    #     try:
    #         f = open('ModelCard.md', "w")
    #     except Exception:
    #         print("Unable to create .md document")
    #     f.write("# " + self.model + " Model Card\n")
    #     if self.name is not None:
    #         f.write("##Collaborators:\n")
    #         for name in self.name:
    #             f.write('* {}\n'.format(name))
    #     f.write("\n")
    #     if self.agency is not None:
    #         f.write("##Agency:\n")
    #         for agency in self.agency:
    #             f.write('* {}\n'.format(agency))
    #     if self.owner is not None:
    #         f.write("##Ownership:\n")
    #         f.write('* {}\n'.format(self.owner))
    #     for section in arg.keys():
    #         f.write("##" + section + "\n")
    #         for question in arg[section]:
    #             f.write("###" + question + "\n")
    #             f.write("* " + arg[section][question] + "\n")
    #     f.close()

    #     print("Model card created. Open ModelCard.md in a text editor to populate with your responses to the included questions.")


if __name__ == '__main__':
    ModelCardGenerator().cmdloop()
