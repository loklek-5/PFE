net.dns.setdnsserver("8.8.8.8", 1)
net.dns.resolve("google.com", function(sk, server_ip)
    if (server_ip == nil) then print("DNS fail!") else

        print(server_ip)

        conn = net.createConnection(net.TCP, 0)

        conn:on("receive", function(conn, payload)
            print("Received: " .. payload)
        end)

        conn:on("connection", function(conn, payload)
            print("Connected")
            conn:send("GET /get HTTP/1.1\r\n"
                    .. "Host: google.com\r\n"
                    .. "Connection: keep-alive\r\n"
                    .. "Accept: */*\r\n\r\n")
        end)

        conn:connect(80, server_ip)
    end
end)
