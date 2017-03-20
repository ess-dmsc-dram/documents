ChannelFinder Investigation
===========================

This is to document the findings when investigating ChannelFinder as a 
potential service to use for storing and retrieving channel meta data.


Website: http://channelfinder.sourceforge.net/

Source Repos: https://github.com/ChannelFinder

Overview
--------
- [ChannelFinderService]: Server written in Java, unit tests in Python
- [pyCFClient]: Python Client API
- [javaCFClient]: Java Client API
- "[RecSync]" project also in repo tree (Python and C)


First Impressions
-----------------
- Code somewhat stale (~1 year since last update on server)
- Site very outdated (missing and old links)
- Links to old mercurial repository and tarfile of client source
- Full documentation difficult to find or missing
- Some doxygen generated documentation, but doesn't contain instructions and 4+ years old
- When installed, server hosts two PDF files that describe the [API][CFApiDoc] and [Design][CFDesignDoc]
- PDFs can also be found in [server repo](https://github.com/ChannelFinder/ChannelFinderService/tree/master/channelfinder/src/main/webapp)... they are 5 and 7 years old


Installation
------------
- Detailed installation instructions available in readme.md
- Difficult installation for such a simple tool
- Involves manually installing and configuring many third party dependencies
- Many heavy-weight dependencies, such as Glassfish and ElasticSearch, which seems disproportional for a small tool
- Afonso Mukai's [docker image](https://github.com/ess-dmsc/docker-channelfinder) helped a lot to get started


Using REST API
--------------
- Tried different REST clients, can recommend: https://insomnia.rest/
- Using the [API PDF][CFApiDoc] as a reference, tried the following:
- HTTP(S) GET ChannelFinder/resources/channels returns 200 OK (with empty `[]` because no channels set yet)
- HTTP POST ChannelFinder/resources/channels returns 200 OK but response is `[]` just like GET (should create new channel instead)
- HTTPS POST ChannelFinder/resources/channels returns 405 METHOD NOT ALLOWED (even though API doc says to do this)
- PUT appears to get further than POST (even though no mention of it in API), but...
- HTTPS PUT ChannelFinder/resources/channels with XML payload returns 415 UNSUPPORTED MEDIA TYPE (even though docs claim to support XML)
- HTTPS PUT ChannelFinder/resources/channels with JSON payload returns 500 INTERNAL SERVER ERROR and Java Exception:
```
java.lang.ClassNotFoundException: com.fasterxml.jackson.module.jaxb.JaxbAnnotationIntrospector
not found by com.fasterxml.jackson.jaxrs.jackson-jaxrs-json-provider [107]
```
- Subsequent attempts to HTTPS PUT now return 400 BAD REQUEST with:
```
Can not deserialize instance of java.util.ArrayList out of START_OBJECT token at
[Source: org.glassfish.jersey.message.internal.ReaderInterceptorExecutor$UnCloseableInputStream@460e5ff4; line: 1, column: 1]
```
- First attempt after server restart is 500 INTERNAL SERVER ERROR again
- Similar experience with trying "create single channel" requests
- Many responses have wrong `content-type`, and other HTTP headers
- Gave up at this stage... 
- Some problems could be config/dependency related, but many seem to be just inconsistent behaviour and incorrect documentation


Using Python API
----------------
- Make sure to get [pyCFClient] from GitHub, not channelfinderpy from website (old mercurial version)
- Code in pyCFClient/example doesn't work (outdated?)
- Import should be `from channelfinder import ChannelFinderClient, Channel, Property, Tag`
- `InsecureRequestWarning`s on HTTPS request due to missing certificate (probably just a config issue, but should be documented)
- Attempting `addProps` in `example/loadData.py`: `TypeError: <channelfinder.CFDataTypes.Property object at 0x7f3b9caf4810> is not JSON serializable`
- Correct syntax appears to be: `cf.set(properties=[{'name':'prop1','owner':'propOwner'},'prop2','propOwner'])`
- But this returns a 400 BAD REQUEST response
- Similar issue with tags... tag code in `example/demo.py` appears incorrect
- Correct syntax is `cf.set(tag={'name':'example', 'owner':'vioc'})`
- This does work... and `cf.getAllTags()` returns previous set tags
- Channel can be created in a similar way: `cf.set(channel={'name':'myChannel', 'owner':'channelOwner'})`
- And searched with wildcards:
```
>>> cf.find(name='*')
[{u'owner': u'channelOwner', u'tags': [], u'name': u'myChannel', u'properties': []}]
```
- Works better than REST API, but still many bugs and incorrect or old documentation


RecSync
-------
- Seems much fresher, has both client and server
- Replacement for ChannelFinder? Used to populate it? No mention in readme.
- Python server, C client that runs as EPICS support module
- Client automatically informs server of available records
- Server writes client info to screen/log or SQLite DB
- Interaction with ChannelFinder, if any, not specified


Conclusions
-----------
- Rather poor impression overall
- Perhaps a good toolkit, but outdated and incorrect documentation is crippling
- At least some issues appear to be actual bugs rather than just documentation or configuration problems
- Even if issues are overcome, documentation will also need to be updated extensively for future collegues
- Also comes with very heavy dependency tree
- Overall, adopting this toolkit involves inheriting substantial technical debt
- RecSync is seems like the most promising part of this kit:
- Contains solution to pull record data from IOC with a plugin
- Stores record data in lightweight DB, allowing any other service to access in standard way


Actions
-------
These are some recommended actions / questions to pursue moving forward. [RecSync] most promising component and probably warrants further investigation.
- Learn more about how RecSync works
- Can RecSync be run independently from [ChannelFinderService]?
- How, if at all, does RecSync interact with ChannelFinderService?
- Would using just RecSync with our own REST service be viable?
- Find out what `ChannelSeeker` is, and if it relates to `ChannelFinder`


[ChannelFinderService]: https://github.com/ChannelFinder/ChannelFinderService
[pyCFClient]: https://github.com/ChannelFinder/pyCFClient
[javaCFClient]: https://github.com/ChannelFinder/javaCFClient
[RecSync]: https://github.com/ChannelFinder/recsync
[CFApiDoc]: https://github.com/ChannelFinder/ChannelFinderService/blob/master/channelfinder/src/main/webapp/ChannelFinder-API.pdf
[CFDesignDoc]: https://github.com/ChannelFinder/ChannelFinderService/blob/master/channelfinder/src/main/webapp/ChannelFinder-Design.pdf
