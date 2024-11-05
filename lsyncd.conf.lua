settings {
    logfile = "/var/log/lsyncd.log",
    statusFile = "/var/log/lsyncd.status",
    inotifyMode = "CloseWrite or Create or Delete or Move"
}

sync {
    default.direct,
    source = "/mnt/c-prod",

    init = false,
    delete = false,

    onCreate = "bash notify_django.sh created ^sourcePathname",
    onDelete = "bash notify_django.sh deleted ^sourcePathname",
    onMove = "bash notify_django.sh renamed ^sourcePathname ^targetPathname"
}