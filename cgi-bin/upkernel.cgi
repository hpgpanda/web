#!/bin/bash
PATH=/bin:/sbin:/usr/bin:/usr/sbin

echo  -e "Content-type: text/html \n\n"
echo "<html>"
echo "<head>"
echo "<title>内核升级</title>"
echo "<meta http-equiv=\"Content-Type\" content=\"text/html; charset=utf-8\" />"
#echo "
#<script type=\"text/javascript\">
#    function getFileSize()
#    {
#        var s=document.file.kpacket.value;
#        var img=new Image();
#        img.src=s;
#        alert("filesize="+img.fileSize+"byte");
#        return false;
#    }
#</script>"
echo "</head>"
echo "<body>"
echo "<center>"
echo "<h3>内核升级</h3>"
echo "</center>"
echo "<hr>"
    echo "<center>"
    echo "<br><br>"
    echo "<form name=\"file\" action=\"/cgi-bin/doupkernel.cgi\" enctype=multipart/form-data  method=POST>"
        echo "<table>"
            echo "<tr>"
                echo "<td>请选择文件:</td>"
                echo "<td><input type=\"file\" name=\"kpacket\" onchange=\"getFileSize()\" ></td>"
                echo "<td><input type=\"submit\" value="上载"></td>"
            echo "</tr>"

        echo "</table>"
    echo "</form>"
                echo "<br><br>"
                platform=`cat /proc/cpuinfo | grep 'Hardware' | awk '{print $3}'`
                echo "请遵循升级包标准格式：uImage_${platform}_rel_YYYYMMDD.tar"
    echo "</center>"
echo "</body>"
echo "</html>"
