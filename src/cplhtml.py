#!/usr/bin/env python
# -*- coding: UTF-8 -*-

class CPLHTML():



	def __init__(self, dictionary):
		self.dictionary = dictionary

	def getHeader(self, d):
		s = '<div id="header"><div id="logo"> <h1><a>' + d['content']['newspaper']['title']
		if d['content']['newspaper'].has_key("date"):
			s += '</a><p>' + d['content']['newspaper']['date'] + '</p>'
		s += '</div></h1><div id="separador"></div></div>'
		return s

	def getNews(self, d, news):
		result = []
		for n in news:
			result.append("<p>")
			if n[1] == 'title':
				result.append('<H2>%s</H2>' % d['content'][n[0]][n[1]])
			elif n[1] == 'image':
				result.append('<div id="figura"><img src="%s"></img></div>' % d['content'][n[0]][n[1]])
			elif n[1] == 'source':
				result.append('<B>Fonte: </B> <a href="%s" target="_blank">%s</a>' % (d['content'][n[0]][n[1]], d['content'][n[0]][n[1]]))
			elif n[1] == 'author':
				result.append('<B>Autor: </B> %s' % d['content'][n[0]][n[1]])
			elif n[1] == 'date':
				result.append('<B>Data: </B> %s' % d['content'][n[0]][n[1]])
			else:
				result.append(d['content'][n[0]][n[1]])
			result.append("</p>")
		return "\n".join(result)

	def getTable(self, d):
		num_cols = d["structure"]["format"]["col"]
		current_col = 0
		table = []
		table.append('<TABLE cellSpacing=0 cellPadding=8 width="1024" border=1>')

		table.append("<TR>")
		#add the news 
		#rethink the way we arrange columns
		for news in d["structure"]["items"]:
			start_col = news["col_range"][0]-1 #here cols starts in 0
			end_col = news["col_range"][1]-1
			#fix col range
			if end_col > num_cols:
				end_en = num_cols
			if start_col > end_col:
				start_col = num_cols
			if end_col < start_col:
				end_col = start_col
			cols = end_col - start_col + 1
			if start_col < current_col:
				if current_col < num_cols:
					table.append("<td colspan='" + str(num_cols - current_col) + "'></td>")
				#add new line
				table.append("</TR>")
				table.append("<TR>")
				current_col = 0

			if current_col != start_col:
				table.append('<td colspan="' + str(start_col - current_col) + '"></td>')
			table.append('<td colspan="' + str(cols) + '">')
			table.append(self.getNews(d, news['item_content']))
			table.append('</td>')
			current_col += cols

		table.append('</TABLE>')

		return "\n".join(table)

	def generateHTML(self):
		d = self.dictionary
		model = [
			'<HTML>',
			'<HEAD> <meta http-equiv="content-type" content="text/html; charset=utf-8" />'
			'<TITLE>' + d['content']['newspaper']['title'] + '</TITLE>',
			'<link rel="stylesheet" type="text/css" href="style/style.css" media="screen" />',
			'<script type= "text/javascript"> </script>',
			'</HEAD>'
			'<BODY>',
			self.getHeader(d),
			self.getTable(d),
			'</BODY>',
			'</HTML>',
			]
		return "\n".join(model)

if __name__ == "__main__":
	"""Runs a small test with the htmlgenerator"""
	import sys
	from cpllexer import CPLLexer
	from cplparser import CPLParser

	if len(sys.argv) < 2:
		print "first argument must be the cpl file."
		sys.exit(1)

	f=open(sys.argv[1])
	cpl_file = f.read()
	f.close()

	# Build the lexer
	cpllexer = CPLLexer()
	cpllexer.build()
	cplparser = CPLParser(cpllexer)
	cplparser.build()
	d = cplparser.parser.parse(cpl_file)
	if not d:
		print "Parsing failed!"
	else:
		cplhtml = CPLHTML(d)
		print cplhtml.generateHTML()

