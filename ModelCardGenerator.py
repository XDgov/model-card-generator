import cmd, sys
import os
import argparse
import markdown

class ModelCardGenerator(cmd.Cmd):
	intro = 'Welcome to the model card generator! \n Model cards and data sheets are a framework to systematically document AI/ML model and training data qualities that can be sources of bias. This information will enable data and model users to pinpoint potential sources of bias. This tool will walk you through the process.\n\n To begin, type "begin". \n (Need help? type help or ? for commands) \n\n\n Required packages: markdown'
	prompt = '[mcg]'
	file = open("input.cmd", 'w')
	name = None
	owner = None
	agency = None
	model = None
	exampleDict = {'Anticipated Use':["In which agencies will this model be used?", "Who are the intended users of the model?", "What are the intended use cases of the model?"],
			'Model Information':["What is the current model version?", "What is the version release date?", "What changes have been made since the last release?", "What is the license for use?"],
			'Model Architecture':["What type of algorithm is used?", "How is the input data formatted?", "How is the output data formatted?"],
			'Datasets':["Does the training dataset contain information related to individuals or human populations?", "What is the source(s) of the training data?", "How was this data collected or generated?", "What variables are contained in this dataset?", "How many entries are contained in your dataset?", "What percent of data is chosen as a validation set?"],
			'Performance Metrics':["What metrics are used to rate model performance?", "How are the metrics being reported?", "What is the confidence interval of these metrics?", "What decision threshold was used to compute the metric?", "What factors limit the model's performance?"],
			'Bias':["Within the workflow of this model, are there concerns related to privacy or surveillance?", "What steps are taken to mitigate privacy and surveillance risks in the model architecture or use cases?", "Within the workflow of this model, is there risk of discrimination against protected classes: age, gender, race, sexuality, color, religion/creed, nationality, disability, veteran status, genetic information, or citizenship?", "What strategies are being used to address possible sources of discrimination in your model architecture or use cases?", "Within the workflow of this model, is there risk of human judgement injecting bias?", "What methods are used to minimize bias from human judgement?", "What biases are potentially found in the dataset from collection methods, historical unfairness, sample size, etc.?", "Are there variables that are influenced by or connected to protected classes? How is this relationship evaluated as a potential source of bias? Example: Gender vs Hair length", "How and when are biases in the dataset addressed in the workflow of the model?", "What testing has been performed to look for bias related to discrimination of protected classes?", "What testing has been performed to maximize fairness in the model’s learned behavior?", "What percentage of development time has been dedicated to bias mitigation?"]}

	informationDict = {'Anticipated Use': "ant use info", 'Model Information': "mod info info", 'Model Architecture': "mod arch info", 'Datasets':"dataset info", 'Performance Metrics':"perf metrics info", 'Bias':"bias info"}
	questionsDict = {'Anticipated Use':["In which agencies will this model be used?", "Who are the intended users of the model?", "What are the intended use cases of the model?"],
			'Model Information':["What is the current model version?", "What is the version release date?", "What changes have been made since the last release?", "What is the license for use?"],
			'Model Architecture':["What type of algorithm is used?", "How is the input data formatted?", "How is the output data formatted?"],
			'Datasets':["Does the training dataset contain information related to individuals or human populations?", "What is the source(s) of the training data?", "How was this data collected or generated?", "What variables are contained in this dataset?", "How many entries are contained in your dataset?", "What percent of data is chosen as a validation set?"],
			'Performance Metrics':["What metrics are used to rate model performance?", "How are the metrics being reported?", "What is the confidence interval of these metrics?", "What decision threshold was used to compute the metric?", "What factors limit the model's performance?"],
			'Bias':[["Within the workflow of this model, are there concerns related to privacy or surveillance?", "What steps are taken to mitigate privacy and surveillance risks in the model architecture or use cases?", "Within the workflow of this model, is there risk of discrimination against protected classes: age, gender, race, sexuality, color, religion/creed, nationality, disability, veteran status, genetic information, or citizenship?", "What strategies are being used to address possible sources of discrimination in your model architecture or use cases?", "Within the workflow of this model, is there risk of human judgement injecting bias?", "What methods are used to minimize bias from human judgement?", "What biases are potentially found in the dataset from collection methods, historical unfairness, sample size, etc.?", "Are there variables that are influenced by or connected to protected classes? How is this relationship evaluated as a potential source of bias? Example: Gender vs Hair length", "How and when are biases in the dataset addressed in the workflow of the model?", "What testing has been performed to look for bias related to discrimination of protected classes?", "What testing has been performed to maximize fairness in the model’s learned behavior?", "What percentage of development time has been dedicated to bias mitigation?"], ["Within the workflow of this model, is there risk of human judgement injecting bias?", "What methods are used to minimize bias from human judgement?", "What biases are potentially found in the training dataset from collection methods, sample size, representation, etc.?", "What evaluation tools have been used to evaluate bias in the training dataset?", "How and when are biases in the dataset addressed in the workflow of the model?", "What testing has been performed to look for bias in the model?", "What percentage of development time has been dedicated to bias mitigation?"]]}

	# basic commands #
	def do_name(self, arg):
		'Names of collaborators in a "+" separated list: name Jane Doe, Ph.D. + John Smith + Joe Schmo'
		temp_list = arg.split("+")
		for n in range(0,len(temp_list)):
			temp_list[n] = temp_list[n].strip()
		self.name = temp_list

	def do_model(self, arg):
		'Model name: model Test Model Name'
		self.model = arg

	def do_owner(self, arg):
		'Internally-built, off-the-shelf, or bespoke aquisition?: owner bespoke'
		
		types = ["Internally built", "Off-the-shelf", "Bespoke"]
		self.owner = types[int(arg) - 1]

	def do_agency(self, arg):
		'Affiliated agency ("+" seperated list for multiple agencies): agency Census Bureau + xD'
		temp_list = arg.split("+")
		for n in range(0,len(temp_list)):
			temp_list[n] = temp_list[n].strip()
		self.agency = temp_list

	def printinfo(self, arg):
		'Displays the current inputs'
		print("Collaborators: ", self.name)
		print("Aquisition: ", self.owner)
		print("Affiliated Agency: ", self.agency)

	def do_input(self, arg):
		'Read input file: input'
		
		#try:
		self.readInputTXT()
		try:
			with open('ModelCard.md', 'r') as f:
				text = f.read()
				html = markdown.markdown(text)

			with open('ModelCard.html', 'w') as f:
				f.write(html)
			f.close()
		except:
			print("Unable to create HTML file")

		#except:
			#print("Unable to read input file. Please check the file has been created and populated, then, try again.")	

	def do_begin(self, arg):
		'Begin content entry:  begin'	
		

		m = input("What is your model name?\n")
		self.do_model(m)

		n = input("\nEnter names of model owners in a \"+\" seperated list. Example: Jane Doe, Ph.D. + John Smith\n")		
		self.do_name(n)
		
		a = input("\nEnter affiliated agencies in a + seperated list. Example: xD + Census\n")
		self.do_agency(a)

		aqFlag = True
		o = input("\nHow was the model aquired:\n1. internally-built - Developed and maintained by employees of the intended user\n2. off-the-shelf - Existing model aquired and modified for new use case\n3. bespoke - Outside agency developed model for this specific use case\n") 
		while aqFlag == True:
			
			if o.isnumeric():	
				if int(o) > 0 and int(o) < 4:
					self.do_owner(o)
					aqFlag = False
			else:
				print("Invalid input")
				o = input("\nHow was the model aquired:\n1. internally-built - Developed and maintained by employees of the intended user\n2. off-the-shelf - Existing model aquired and modified for new use case\n3. bespoke - Outside agency developed model for this specific use case\n")

		form = input("\nIn what format would you like to input further responses:\n1. Command line\n2. Text document\n")


		formFL = True
		humanFlag =0
		while formFL == True:
			form = int(form)
			if form == 2:
				included_questions = {}

				for key in self.questionsDict.keys():
					questions = self.questionsDict[key]
					while key == "Bias" and humanFlag not in ["1","2"]:
						humanFlag = input("Does the training dataset contain information related to individuals or human populations?\n" + "1. Yes\n" + "2. No\n")
						if humanFlag == "1":
							questions = self.questionsDict[key][0]
						elif humanFlag == "2":
							questions = self.questionsDict[key][1]
					q = "\n" + key + "\n"
					for question in questions:
						q = q + "     " + question + "\n"

					q = q + "Include section? (Y/N)\n"

					fl = True

					while(fl):
						y = input(q)

						if y == "Y" or y == "y":
							included_questions[key] = questions
							fl = False
						elif y == "N" or y == "n":
							fl = False
						else:
							print("Invalid input")


				print("Section selection complete. Your file will now be populated.")
				self.populateTXT(included_questions)
				formFL = False

			elif form == 1:

				included_questions = {}
				for key in self.questionsDict.keys():
					q = "\n" + key + "\n"
					print(q)
					temp = {}
					questions = self.questionsDict[key]
					while key == "Bias" and humanFlag not in ["1","2"]:
                                                humanFlag = input("Does the training dataset contain information related to individuals or human populations?\n" + "1. Yes\n" + "2. No\n")
                                                if humanFlag == "1":
                                                        questions = self.questionsDict[key][0]
                                                elif humanFlag == "2":
                                                        questions = self.questionsDict[key][1]

					for queIndex in range(0,len(questions)):
						question = questions[queIndex]
						ans = input(question + "\n")
						while ans.lower() == "help":
							self.examples(self, key, queIndex)
							ans = input(question + "\n")
						
						if len(ans) > 1:
							temp[question] = ans
					if len(temp.keys()) > 0:
						included_questions[key] = temp
				print("Questions completed. Your output file will now be populated.")
				outputForm = input("\nIn what format would you like to output your model card responses:\n1. Markdown (.md)\n2. JSON (.json)\n3. Word (.docx)\n")
				while outputForm not in ["1","2","3"]:
					outputForm = input("\nIn what format would you like to output your model card responses:\n1. Markdown (.md)\n2. JSON (.json)\n3. Word (.docx)\n")

				outputFL = True
				while outputFL == True:
					outputForm = int(outputForm)
					if outputForm == 1:
						self.do_bye(included_questions, 1)
						outputFL = False
					elif outputForm > 1 and outputForm < 4:
						self.do_bye(included_questions, outputForm + 3)
						outputFL = False
					else:
						print("Invalid output form selected.\n")
						outputForm = input("\nIn what format would you like to output your model card responses:\n1. Markdown (.md)\n2. JSON (.json)\n 3. Word (.docx)\n")
				
				formFL = False

			else:
				print("Invalid form choice")
				form = input("\nIn what format would you like to input further responses:\n1. Command line\n2. Word document\n 3. Text document\n")

		self.do_bye(included_questions,form)
		

	def do_bye(self, arg, form):
		'Stop recording, close the tool, and exit:  bye'

		if form == 1:

			self.populateMD(arg)

		try:
			with open('ModelCard.md', 'r') as f:
				text = f.read()
				html = markdown.markdown(text)

			with open('ModelCard.html', 'w') as f:
				f.write(html)
			f.close()
		except:
			print("Unable to create HTML file")
		print('Thank you for using the Model Card Generator. \n Type \'exit\' to leave the shell')
		return True

	def examples(self,questionsDict, section, questionIndex):


		print("*****************************")
		print("\n")

		print("More information:\n")
		print(self.informationDict[section])

		print("\n")	
		print("Question: " + self.questionsDict[section][questionIndex])
		print("Example Answer:\n")
		print(self.exampleDict[section][questionIndex])
		print("*****************************")


	"""
	def populateWORD(self,arg):	

		try:
			from docx import Document
			document = Document()
		except:
			print("Missing prerequisite packages. Saving information to ModelCardInputs.txt")

		populateMD(self,arg)

	"""
	def populateTXT(self,arg):	

		file = open("ModelCardInputs.txt","w")

		names = ""
		agents = ""
		for name in self.name:
			if names != "":
				names = names + "+" + str(name)
			else:
				names = str(name)
		file.write(str(names))
		file.write("\n")
		file.write(str(self.owner))
		file.write("\n")
		for agent in self.agency:
			if agents != "":
				agents = agents + "+" + str(agent)
			else:
				agents = str(agent)
		file.write(str(agents))
		file.write("\n")
		file.write(str(self.model))
		file.write("\n")

		file.write("Welcome to the model card generator input document. You may answer your selected questions below. Answers should be written in the sections delineated by '################' only. When finished, run the generator once more and run the command 'input'.\n")


		for section in arg.keys():
			file.write("*" + section + "*\n")
			file.write(self.informationDict[section])

			for index in range(0, len(arg[section])):
				file.write("+" + arg[section][index] + "+\n")
				file.write("Example Answer:\n")
				file.write(self.exampleDict[section][index])
				file.write("\nEnter your response between the pound signs (#):")
				file.write("\n#")
				file.write("\n")
				file.write("#\n")
		
			file.write("")
			file.write("")
		file.close()				
			
	def readInputTXT(self):
	
		if os.path.isfile("ModelCardInputs.txt"):

			file = open("ModelCardInputs.txt","r")
			data = file.read()
			file.close()

			vars = data.split("\n")
			self.name = vars[0].split("+")
			self.owner = vars[1]
			self.agency = vars[2].split("+")
			self.model = vars[3]

			included_questions = {}
			temp = {}

			currentSection = None
			currentQuestion = None

			sections = data.split("*")
			for s in range(0,len(sections)):
				if s%2 == 0 and s!=0:
					questions = sections[s].split("+")
					for q in range(0,len(questions)):
						if q%2==0 and q!=0:
							answers = questions[q].split("#")
							for a in range(0,len(answers)):
								if a%2!=0 and a!= 0 and currentQuestion != None:
									temp[currentQuestion] = answers[a]
						elif q == 0:
							continue
						else:
							currentQuestion = questions[q]
				else:
					if s == 0:
						continue
					elif currentSection != None:
						included_questions[currentSection] = temp
						temp = {}
						currentSection = sections[s]
					else:
						currentSection = sections[s]
			included_questions[currentSection] = temp
			self.populateMD(included_questions)
			print("Markdown file created.")

		else:
			print("Unable to open ModelCardInputs.txt")


		







	"""
	def readInputTXT(self):
		included_questions = {}
		try:
			file = open("ModelCardInputs.txt","r")
		except:
			print("Unable to open ModelCardInputs.txt")

		line = file.readlines()

		self.name = line[0][2:-3].split(",")
		self.owner = line[1][:-1]
		self.agency = line[2][2:-3].split(",")
		self.model = line[3][:-1]


		questions = []
		answers = []
		section = ""

		included_questions = {}


		y = 0
		for l in range(5,len(line)):
			if "*" in line[l]:
				if section == "":
					section = line[l-1]
				else:
					i = 0
					temp = {}
					while i < len(answers):
						answer = ""
						for j in range(answers[i] + 1, answers[i+1]):
							answer += line[j]
						temp[line[answers[i]-1]] = answer.strip()
						i += 2
					included_questions[section] = temp
					section = line[l-1]
					answers = []
			elif "+" in line[l]:
				questions.append(line[l-1])
				questions.append(line[l-1])
			elif "#" in line[l]:
				answers.append(l)
		i = 0
		temp = {}
		while i < len(answers)-1:
			answer = ""
			for j in range(answers[i] + 1, answers[i+1]):
				answer += line[j]
			temp[line[questions[i]]] = answer
			i += 2
		included_questions[section] = temp

		self.populateMD(included_questions)
	"""
	def populateMD(self,arg):
		try:
			f = open('ModelCard.md',"w")
		except:
			print("Unable to create .md document")
		f.write("# " + self.model + " Model Card\n")
		if self.name != None:
			f.write("##Collaborators:\n")
			for name in self.name:
				f.write('* {}\n'.format(name))
		f.write("\n")
		if self.agency != None:
			f.write("##Agency:\n")
			for agency in self.agency:
				f.write('* {}\n'.format(agency))
		if self.owner != None:
			f.write("##Ownership:\n")
			f.write('* {}\n'.format(self.owner))
		for section in arg.keys():
			f.write("##" + section + "\n")
			for question in arg[section]:
				f.write("###" + question + "\n")
				f.write("* "+ arg[section][question] + "\n") 
		f.close()

		print("Model card created. Open ModelCard.md in a text editor to populate with your responses to the included questions.")

	def save_input(self, arg):
		'Save future commands to filename:  RECORD rose.cmd'
		self.file = open(arg, 'w')
	def precmd(self, line):
		if self.file and 'playback' not in line:
		    print(line, file=self.file)
		return line
	def do_exit(selfi, inp):
		print("Good bye!")
		return True
	def close(self):
		if self.file:
		    self.file.close()
		    self.file = None

if __name__ == '__main__':
    ModelCardGenerator().cmdloop()
