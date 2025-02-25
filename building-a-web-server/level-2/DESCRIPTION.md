In this challenge, you’ll begin your journey into networking by creating a socket using the [socket](https://man7.org/linux/man-pages/man2/socket.2.html) syscall.
A socket is the basic building block for network communication; it serves as an endpoint for sending and receiving data.
When you invoke [socket](https://man7.org/linux/man-pages/man2/socket.2.html), you provide three key arguments: the domain (for example, `AF_INET` for IPv4), the type (such as `SOCK_STREAM` for TCP), and the protocol (usually set to `0` to choose the default).
Mastering this syscall is important because it lays the foundation for all subsequent network interactions.
