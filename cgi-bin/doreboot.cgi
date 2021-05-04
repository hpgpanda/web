#!/bin/bash

PATH=/bin:/sbin:/usr/bin:/usr/sbin

echo  -e "Content-type: text/html \n\n"
echo "<html>"
echo "<head>"
echo "<title>NFS设置</title>"
echo "<meta http-equiv=\"Content-Type\" content=\"text/html; charset=utf-8\" />"
echo "</head>"
echo "<body>"
echo "<center>"
echo "<h3>重启系统</h3>"
echo "</center>"
echo "<hr>"
    echo "<center><br><br>"
    echo "正在重启<br>"
    echo "<center>"
echo "</body>"
echo -e "</html>\n\n"
reboot
