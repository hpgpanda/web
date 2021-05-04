#!/bin/bash

PATH=/bin:/sbin:/usr/bin:/usr/sbin
i="0"
echo  -e "Content-type: text/html \n\n"
echo "<html>"
echo "<head>"
echo "<title>服务设置</title>"
echo "<meta http-equiv=\"Content-Type\" content=\"text/html; charset=utf-8\" />"
echo "</head>"
echo "<body>"
echo "<center>"
echo "<h3>服务设置</h3>"
echo "</center>"
echo "<hr>"
    
    echo "<center>"
    echo "<form action=\"/cgi-bin/doservicecfg.cgi\" method=POST>"
    echo "<table width=\"75%\">"
        echo "<tr>"
            echo "<td>&nbsp;&nbsp;</td>"
            echo "<td>服务名</td>"
            echo "<td>运行等级</td>"
            echo "<td>当前状态</td>"
        echo "</tr>"
        zyconfig -l | while read line
        do
            i=`expr $i + 1`
            if [[ $i -eq 1 ]];then
                continue
            fi
            service=`echo ${line} | awk '{print $1}'`
            level=`echo ${line} | awk '{print $2}'`
            status=`echo ${line} | awk '{print $3}'`
            echo "<tr>"
            echo "<td><input type=\"checkbox\" name=\"$service\" /></td>"
            echo "<td>"${service}"</td>"
            echo "<td>"${level}"</td>"
            echo "<td>"${status}"</td>"
            echo "</tr>"
        done
        echo "<tr>"
            echo "<td><input type=\"submit\" name=\"add\"/ value=\"设置启动\" ></td>"
            echo "<td><input type=\"submit\" name=\"cal\" value=\"取消启动\"></td>"
            echo "<td><input type=\"submit\" name=\"del\" value=\"删除启动\"></td>"
        echo "</tr>"
        echo "<tr>"
        echo "<td><br></td>"
        echo "</tr>"
        echo "<tr>"
            echo "<td>服务名:</td>"
            echo "<td><input type=\"text\" name=\"servname\"></td>"
            echo "<td>运行级别:</td>"
            echo "<td><input type=\"text\" name=\"level\"></td>"
            echo "<td>(90--99)</td>"
        echo "</tr>"
        echo "<tr>"
            echo "<td>程序路径:</td>"
            echo "<td><input type=\"text\" name=\"path\"></td>"
            echo "<td>程序参数(可选):</td>"
            echo "<td><input type=\"text\" name=\"args\"></td>"
        echo "</tr>"
        echo "<tr>"
            echo "<td><input type=\"submit\" name=\"new\" value="新建" ></td>"
        echo "</tr>"
    echo "</table>"
    echo "</form>"
echo "</center>"
echo "</body>"
echo -e "</html>\n\n"
 
