#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import ply.yacc as yacc

class CPLParser():
	def __init__(self, lexer):
		self.lex = lexer.lexer
		self.tokens = lexer.tokens

	def p_statement_assign(self, t):
		#'statement : BEGIN content_s structure_s END'
		"""statement : BEGIN content_s structure_s END
			     | BEGIN structure_s content_s END"""
		print t[2]
		print t[3]
	
#	def p_statement_assign(self, t):
		#Statement for tests only
#		"""statement : BEGIN content_s END"""
#		print t[2]

	def p_structure_statement(self, t):
		'structure_s : STRUCTURE LBRACKET format_s item_list RBRACKET'
		t[0] = (t[3], t[4])

	def p_format_s(self, t):
		'format_s : FORMAT LBRACKET field_list RBRACKET'
		t[0] = {t[1]: t[3]}

	def p_item_list(self,t):
		'item_list : item_s item_list'
		t[0] = t[2]
		t[0].append(t[1])
	
	def p_item_list2(self,t):
		'item_list : item_s'
		t[0] = [t[1]]

	def p_item_s(self,t):
		"item_s : ITEM col_range_s LBRACKET item_content_list RBRACKET"
		t[0] = {}
		t[0]['col_range'] = t[2]
		t[0]['item_content'] = t[4]

	def p_item_content_list(self,t):
		'item_content_list : item_content_s item_content_list'
		t[0] = t[2]
		t[2].append(t[1])

	def p_item_content_list2(self, t):
		'item_content_list : item_content_s'
		t[0] = [t[1]]

	def p_item_content_s(self, t):
		"item_content_s : ID '.' ID"
		t[0] = (t[1], t[3])

	def p_col_range_s(self,t):
		"col_range_s : '[' NUMBER ']'"
		t[0]=(t[2], t[2])

	def p_col_range_s2(self,t):
		"col_range_s : '[' NUMBER ':' NUMBER ']'"
		t[0]=(t[2], t[4])

	def p_content_statement(self, t):
		'content_s : CONTENT LBRACKET content_list RBRACKET'
		t[0] = t[3]

	def p_content_list (self, t):
		"""content_list : newspaper_s content_list  
				| session_s content_list"""
		t[0] = t[1]
		t[0].update(t[2])

	def p_content_list2 (self, t):
		"""content_list : newspaper_s 
				| session_s"""
		t[0] = t[1]

	def p_newspaper_statement(self, t):
		'newspaper_s : NEWSPAPER LBRACKET field_list RBRACKET'
		t[0] = {t[1]: t[3]}

	def p_session_statement(self, t):
		'session_s : ID LBRACKET field_list RBRACKET'
		t[0] = {t[1]: t[3]}

	def p_field_list (self, t):
		'field_list : field_s field_list'
		t[0] = t[2]
		t[0].update(t[1])

	def p_field_list2 (self, t):
		'field_list : field_s'
		t[0] = t[1]

	def p_field_statement (self, t):
		'field_s : FIELD string_s'
		t[0] = {t[1][:-2] : t[2]}

	def p_field_statement_number (self, t):
		'field_s : FIELD NUMBER'
		t[0] = {t[1][:-2] : t[2]}

	def p_string_statement(self, t):
		"string_s : STRING string_s"
		t[0] = t[1] + '\n' + t[2]

	def p_string_number_statement(self, t):
		"string_s : NUMBER STRING"
		t[0] = str(t[1]) + ' ' + t[2]

	def p_string_def(self, t):
		'string_s : STRING'
		t[0] = t[1]


	def build(self, **kwargs):
		self.parser = yacc.yacc(module=self, **kwargs)

if __name__ == "__main__":
	"""Runs a small test with the parser"""
	import sys
	from cpllexer import CPLLexer

	if len(sys.argv) < 2:
		print "first argument must be the cpl file."
		sys.exit(1)

	# Build the lexer
	cpllexer = CPLLexer()
	cpllexer.build()
	cplparser = CPLParser(cpllexer)
	cplparser.build()
	f=open(sys.argv[1])
	cplparser.parser.parse(f.read())
	f.close()

