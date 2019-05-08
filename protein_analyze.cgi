#!/usr/local/bin/python3

import cgi 
import jinja2
import mysql.connector 
import re

def main(): 

	templateLoader = jinja2.FileSystemLoader( searchpath="./templates" )
	env = jinja2.Environment(loader=templateLoader)
	template = env.get_template('final_template.html')
	form = cgi.FieldStorage()
	term = form.getvalue('uniquename')
   	#print("Content-type: text/plain\n")
	conn = mysql.connector.connect(user='hthoma25', password='MHC2#janeway',
								host='localhost', database='hthoma25_chado')
	
	
	cursor = conn.cursor()
	
	qry = ("SELECT residues FROM feature WHERE uniquename = %s")
    
    
	cursor.execute(qry,(term,))
	
	protein_list=list()
	for residues in cursor:
		protein_list.append(residues)
	
# A Dictionary for converting amino acid residue to its respective molecular weight in Daltons
	mw = {'A':89, 'R':174, 'N':132, 'D':133, 'B':133, 'C':121, 'Q':146, 
	  'E':147, 'Z':147, 'G':75, 'H':155, 'I':131, 'L':131, 'K':146,
	  'M':149, 'F':165, 'P':155, 'S':105, 'T':119, 'W':204, 'Y':181, 'V':117}
	  
# A Dictionary for converting amino acid residue to its respective charge at pH=7.0	  
	charge = {'A':0, 'R':1, 'N':0, 'D':-1, 'B':0, 'C':0, 'Q':0, 
	  	  'E':-1, 'Z':0, 'G':0, 'H':1, 'I':0, 'L':0, 'K':1,
	      'M':0, 'F':0, 'P':0, 'S':0, 'T':0, 'W':0, 'Y':0, 'V':0}

#A Dictionary for converting amino acid residue respectively as hydrophobes or hydrophiles 	      
	hydrophilic_hydrophobic = {'A':'h', 'R':'H', 'N':'H', 'D':'H', 'B':'H', 'C':'H',
						   'Q':'H', 'E':'H', 'Z':'H', 'G':'H', 'H':'H', 'I':'h',
						   'L':'h', 'K':'H', 'M':'h', 'F':'h', 'P':'h', 'S':'H',
						   'T':'H',	'W':'h', 'Y':'H', 'V':'h'}
						   
#The protein sequence to be analyzed 


	protein = protein_list

	protein_match=""
	protein_use = str(protein)

	match = re.search('.([A-Z]+).',protein_use)
	if match: 
		protein_match= str(protein_match) + str(match.group(1))

#Definition to get molecular weight of the input protein seq. 
	def get_molecular_weight(protein_match):
		weight = sum(mw[aa] for aa in protein_match)
		return(weight)
	
#Definition to get overall protein charge from the input protein seq. 
	def get_charge(protein_match):
		protein_charge = sum(charge[aa] for aa in protein_match)
		return(protein_charge)


	structure = "" #Empty str with which to append with for loop 

#For loop to covert amino acid residue as hydrophobe or hydrophile and append structure
	for aa in protein_match:
		phobic_philic = hydrophilic_hydrophobic.get(aa)
		structure = structure + phobic_philic



	protein_length = ('The Protein Sequence Length is:\n' +str(len(protein_match)))

	protein_mol_weight = ('Molecular Weight of Protein is:\n' +str(get_molecular_weight(protein_match)) + 'Daltons')

	protein_net_charge = ('The Protein Charge at Physiological pH is:\n' +str(get_charge(protein_match)))

	protein_seq_structure = ('The Sequence of Hydrophilic and Hydrophobic Residues is:\n' +structure)

	#print(protein_length)
	#print(protein_mol_weight)
	#print(protein_net_charge)
	#print(protein_seq_structure)
	
	print("Content-Type: text/html\n\n")
	print(template.render(protein_match=protein_match, protein_length=protein_length, protein_mol_weight=protein_mol_weight, protein_net_charge=protein_net_charge, protein_seq_structure=protein_seq_structure))
	
	cursor.close()
	conn.close()
	
if __name__ == '__main__':
    main()



	