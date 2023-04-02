Chat GPT HTTP Request Parser
----------------------------
The following parser and tests were written by chat GPT as a experiment in AI
paired coding. I slightly massaged the typing and lint, but the functions,
classes and logic is all from the GPT model.

It had a harder time completing the tests, but it did produce a working
hypothesis test, which is very impressive.

Examples
--------
```python
>>> import gpt_tests
>>> gpt_tests.http_request_strategy.example()
HttpRequest(method='PATCH', uri='users/products/api/items/search?sort=asc', http_version='HTTP/1.1', headers={'Accept-Charset': 'utf-8', 'Accept-Language': 'fr-FR'}, body='-8953')
```

Truly amazing.

This is the series of questions I asked:
- I want to write python functions that completely parse the raw bytes of http requests. I don't want to connect a socket or import any additional modules. I just want to have a function that takes the raw bytes of any http request and returns a fully parsed object. I want the http request data model to be expressed as python data-classes. I want the entire user-agent header field parsed as deep as possible. I want the entire cookies filed parsed. I want all the security fields parsed too. Use separate helper function for each of the complicated header fields
- Good. Now lets expand to include a parser for the authorization header field.
- Good. Now lets expand this to account for the possibility of malicious requests. We want to securely handle requests while raising exceptions that have useful and complete information regarding the failure reasons. I want a robust solution that accounts for all known malicious request variants. I want the exceptions to reflect the exact type of malicious request.
- This is good. Now i want to use the python package called hypothesis to create a strategy for http rest requests.
- I want the hypothesis strategy for the ray http request bytes.
- Can you go deeper into the http features and make a strategy that reaches all the edge cases of http requests?
- This example did not work. please try again.
- That worked, but its too much randomness. I want the uri to look real, and for the rest of the attributes to be more real looking. Can you make it better?
- The uri still looks like random garbage text. I want real uri. I think the path_segments are too random for real internet addresses. Can you improve it?
- That did not work. Can you show me an example of a reasonably complex http rest request?
- Can you make a hypothesis strategy that produces something more like the above http request example?
- That worked much better. Can you show me all the known http headers with some examples of each?
- Good. Can you use those http request header examples for the header_names and header_values?
