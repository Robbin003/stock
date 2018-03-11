#!/usr/bin/env coffee

require 'coffeescript/register'

program = require 'commander'

terminate = require './lib/terminate'
config = require './config/config'
pkg = require './package'
stock = require './lib/stock'

checkCodeInput = (code)->
	code = code.toUpperCase code
	unless /^((SH|SZ)\d{6})|\d{5}$/.test code
		console.log "Wrong code."
	else
		return true

program
	.version pkg.version
	.usage '[command]'

program 
	.command 'show <code>'
	.description 'show stock status by code'
	.option '-n, --nocolor', 'do not mark the stock status red or green'
	.option '-i, --interval <interval>', 'set the stock check interval'
	.action (code,options) =>
		code = code.toUpperCase code
		if checkCodeInput code
			interval = config.stockCheckInterval
			if options.interval then interval = options.interval
			showStockStatus = ->
				terminate.showStockHeads()
				terminate.showStockStatus code, options.nocolor
			setInterval showStockStatus, interval
program 
	.command 'list'
	.description 'show the stock status on list'
	.option '-n, --nocolor', 'do not mark the stock status red or green'
	.option '-i, --interval <interval>', 'set the stock check interval'
	.action (options)=>
		interval = config.stockCheckInterval
		if options.interval then interval = options.interval

		showStockListStatus = ->
			terminate.showStockHeads()
			stock.getStockList (data)->
				for code in data
					terminate.showStockStatus code, options.nocolor
		setInterval showStockListStatus, interval


program 
	.command 'add <code>'
	.description 'add stock to stock list'
	.action (code)=>
		code = code.toUpperCase code
		if checkCodeInput code
			stock.addStock code

program 
	.command 'remove <code>'
	.description 'remove stock from stock list'
	.action (code)=>
		code = code.toUpperCase code
		if checkCodeInput code
			stock.removeStock code


program.parse process.argv

# display help by default
if !process.argv.slice(2).length
	program.outputHelp()
