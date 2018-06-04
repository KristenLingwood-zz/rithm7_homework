How The Web Works Exercise
Answer the following questions. Write out your answers in atext or markdown file.

1.  What is HTTP?
    hyper text transfer protocol-- procedure/rules for client and server to communicate. Client generates and asks question, and the servers answers and sends response back.
    request: browser asking server
    response: server replies to browser
    header:
2.  What is a URL?
    address for anything on the web. Has different components: protocol, domain name, port, path, parameters
3.  What is TCP?
    transmission control protocol-- governs how data is split up and sent (as packets), makes sure data is complete and correct before being delivered. TCP is on both client and server sides.
4.  What is IP?
    internet protocol -- assigns a number/label to each machine connected to the internet. IP address is unique label for device.
5.  What is DNS?
    Domain name system-- naming system, interpretation/shortcut for IP addresses. Holds IP address info. Computer using DNS to look up IP address.
6.  What is idempotent?
    always produces the same output regardless of what operations are done. Multiple requests give same result
7.  What is a query string?
    part of the url structure used to search/obtain variables
8.  What is a path or route?
    the directory structure within the website/domain
9.  List four HTTP Verbs and their use cases.
    get-- request info or action from server
    post-- add new data to server
    put-- update existing data on server
    delete-- remove data from server
10. What is a client?
    hardware or software that makes requests from server, like a web browser. Usually the user side.
11. What is a server?
    the host of the data being queried, example: responds to client requests and sends info (data packets) to populate websites
12. What is an HTTP request?
    User/client/web browser generates question/request and sends it to server
13. What is an HTTP response?
    Server answers question/fulfills request and sends the info back to client.
14. What is an HTTP header? Give a couple examples of request and response headers you have seen.
    Address label of sorts for the data transmission between client and server.
15. What is REST?
16. What is JSON?
    javascript object notation-- data transfer format, works really well with javascript
17. What happens when you type in "Hello World" in google.com and press enter?
18. What does it mean when we say the web is "stateless"?
19. What is curl?
    terminal command to make request directly to server
20. Make a GET request to the icanhazdadjoke API with curl to find all jokes involving the word "pirate." (your answer should be the curl command required).
    curl https://icanhazdadjoke.com/search\?term\=pirate
