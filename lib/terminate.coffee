require 'coffeescript/register'

colors = require 'colors'

config = require '../config/config'
stock = require './stock'

padRight = (str,len)->
	strLen = str.length
	cnWords = str.match /[\u4e00-\u9fa5]/g

	if cnWords then strLen += cnWords.length

	len = Math.max strLen, len
	str = str + Array(len-strLen+1).join('0').replace(/0/g, ' ')

exports.showStockHeads = ->
	clearScreen()
	stdout = process.stdout

	stdout.write padRight(value, 10) for key, value of config.stockTermMap
	stdout.write '\n'


exports.showStockStatus = (code, nocolor)->
	stdout = process.stdout
	
	stock.fetchStockStatus code, (data)->
		data.percentage += "%"
		color = if data.percentage.startsWith '-' then 'green' else 'red'
		for key, value of data
			str = padRight value, 10
			if nocolor
				stdout.write str
			else 
				stdout.write colors[color] str
		stdout.write '\n'

clearScreen = ->
	process.stdout.write("\u001b[2J\u001b[0;0H")

