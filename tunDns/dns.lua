sk=net.createConnection(net.UDP, 0)
sk:dns("a.pch",function(con,ip) 
if (ip == nil) then print("DNS fail!") else
        print(ip)
        conn = net.createConnection(net.TCP, 0)
        conn:on("receive", function(conn, payload)
            print("Received: " .. payload)
        end)
        conn:on("connection", function(conn, payload)
            print("Connected")
            conn:send("GET /get HTTP/1.1\r\n"
                    .. "Host: a.pch\r\n"
                    .. "Connection: keep-alive\r\n"
                    .. "Accept: */*\r\n\r\n")
        end)

        conn:connect(8080, ip)
    end
    end)