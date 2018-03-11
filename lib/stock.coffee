require 'coffeescript/register'

url = require 'url'
fs = require 'fs'
request = require 'request'

config = require '../config/config'

proxy = 
	jar: true
	headers: 
		Accept: '*/*',
		"User-Agent": 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36'

http = request.defaults proxy 

visitStockSite = ->
	new Promise (resolve, reject)=>
		if http.authed
			resolve()
		http.get config.stockAPI.site, (err,res,data)=>
			if err
				reject err
			else 
				http.authed = true
				resolve()

readStockCodeFile = ->
	new Promise (resolve)=>
		fs.readFile config.stockDataFile, (err,data)=>
			unless err
				codeList = data.toString().split "\n"
				if codeList[0] is '' then codeList.shift()
				resolve codeList

getStockStatus = (code)->
	new Promise (resolve, reject)=>
		code = encodeURIComponent code
		link = config.stockAPI.info.replace /\{code\}/, code

		http.get link, (err,res,data) ->
			if res.statusCode is 400
				http.authed = false
			if err
				console.log err
			else
				data = JSON.parse data
				resolve data

exports.fetchStockStatus = (code, callback)->
	await visitStockSite()
	data = await getStockStatus code
	result = {}
	if data.error_code 
		console.log "#{code} no exsiting, and removing ..."
		exports.removeStock code
	else
		for key, value of config.stockTermMap
			result[key] = data[code][key]
		callback result

exports.addStock = (code)->
	codeList = await readStockCodeFile()
	if code not in codeList 
		str = codeList.join "\n"
		str += "\n#{code}"
		fs.writeFile config.stockDataFile, str,(err)->
			unless err then console.log "Added #{code} into stock list!"
	else
		console.log "#{code} already in stock list"

exports.removeStock = (code)->
	codeList = await readStockCodeFile()
	if code not in codeList
		console.log "#{code} is not in stock list"
	else
		codeList = (item for item in codeList when item isnt code)
		str = codeList.join "\n"
		fs.writeFile config.stockDataFile, str, (err)->
			unless err then console.log "Removed #{code} from stock list!"


exports.getStockList = (callback)->
	codeList = await readStockCodeFile()
	unless codeList.length
		console.log 'There is NO any stock in list,please add some firstly.'
	else
		callback codeList
