settings {
    logfile = "/var/log/lsyncd.log",
    statusFile = "/var/log/lsyncd.status",
    inotifyMode = "CloseWrite or Create or Delete or Move"
}

sync {
    default.rsync,
    source = "/mnt/c-prod",
    target = "/mnt/c-prod-virtual",
    delay = 5,

    rsync = {
        archive = true,
        delete = false
    },

    onEvent = function(event)
        if event.etype == "CreateDir" or event.etype == "DeleteDir" or event.etype == "RenameDir" then
            local http = require("socket.http")
            local ltn12 = require("ltn12")
            local json = require("cjson")

            local data = json.encode({
                path = event.path,
                type = (event.etype == "CreateDir" and "created")
                       or (event.etype == "DeleteDir" and "deleted")
                       or (event.etype == "RenameDir" and "renamed"),
                old_path = event.oldpath
            })

            local response_body = {}
            http.request{
                url = "http://localhost:8000/event-update/",
                method = "POST",
                headers = {
                    ["Content-Type"] = "application/json",
                    ["Content-Length"] = tostring(#data)
                },
                source = ltn12.source.string(data),
                sink = ltn12.sink.table(response_body)
            }

            print("Directory event sent to Django API: " .. data)
        end
    end
}