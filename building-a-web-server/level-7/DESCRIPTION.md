In this challenge, your server evolves to handle dynamic content based on HTTP GET requests.
You will first use the `read` syscall to receive the incoming HTTP request from the client socket.
By examining the request line--particularly, in this case, the URL path--you can determine what the client is asking for.
Next, use the `open` syscall to open the requested file and `read` to read its contents.
Send the file contents back to the client using the `write` syscall.
This marks a significant step toward interactivity, as your server begins tailoring its output rather than simply echoing a static message.
