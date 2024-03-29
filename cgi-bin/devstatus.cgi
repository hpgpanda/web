#!/bin/bash
PATH=/bin:/sbin:/usr/bin:/usr/sbin
getbdname() {
    cat /proc/cpuinfo | grep 'Hardware' | cut -d: -f2
}

getcpuinfo() {
    cat /proc/cpuinfo  | grep 'Processor' | cut -d: -f2
}

getbogomips() {
    cat /proc/cpuinfo | grep 'BogoMIPS' | cut -d: -f2
    echo "BogoMIPS"
}

getkernelinfo() {
    uname -r
}

getfsinfo() {
    cat /etc/release
}

gethwinfo() {
    cat /proc/cpuinfo | grep 'Revision' | cut -d: -f2
}

gethwserise() {
    cat /proc/cpuinfo | grep 'Serial' | cut -d: -f2
}

getipaddr() {
    ifconfig  | grep 'inet addr:'| grep -v '127.0.0.1' | cut -d: -f2 | awk '{ print $1}'
}

getnetmask() {
    ifconfig | grep 'Mask:'| grep -v '255.0.0.0' | cut -d: -f4 
}

getgateway() {
    route | grep default.*UG.*$eth | awk '{print $2}'
}

getsystime() {
    date
}
getsysstat() {
    mode=`eeprom flag get 0`
    if [[ ${mode} -eq 0 ]];then
        echo "正常内核"
    else
        echo "备份内核"
    fi
}
echo  -e "Content-type: text/html \n\n"
echo "<html>"
echo "<head>"
echo "<title>设备状态</title>"
echo "<meta http-equiv=\"Content-Type\" content=\"text/html; charset=utf-8\" />"
echo "</head>"
echo "<body>"
    echo "<center>"
        echo "<h3>设备状态信息</h3>"
    echo "</center>"
    echo "<hr>"
    echo "<table>"
        echo "<tr>"
            echo "<td>"
                echo "工控机型号"
            echo "</td>"
            echo "<td>"
                getbdname
            echo "</td>"
        echo "</tr>"
        echo "<tr>"
            echo "<td>"
                echo "CPU信息"
            echo "</td>"
            echo "<td>"
                getcpuinfo
            echo "</td>"
        echo "</tr>"
        echo "<tr>"
            echo "<td>"
                echo "CPU Speed"
            echo "</td>"
            echo "<td>"
                getbogomips
            echo "</td>"
        echo "</tr>"
        echo "<tr>"
            echo "<td>"
                echo "内核信息"
            echo "</td>"
            echo "<td>"
                getkernelinfo
            echo "</td>"
        echo "</tr>"
        echo "<tr>"
            echo "<td>"
                echo "文件系统版本"
            echo "</td>"
            echo "<td>"
                getfsinfo
            echo "</td>"
        echo "</tr>"
        echo "<tr>"
            echo "<td>"
                echo "硬件版本信息"
            echo "</td>"
            echo "<td>"
                gethwinfo
            echo "</td>"
        echo "</tr>"
        echo "<tr>"
            echo "<td>"
                echo "硬件序列号"
            echo "</td>"
            echo "<td>"
                gethwserise
            echo "</td>"
        echo "</tr>"
        echo "<tr>"
            echo "<td>"
                echo "IP地址"
            echo "</td>"
            echo "<td>"
                getipaddr
            echo "</td>"
        echo "</tr>"
        echo "<tr>"
            echo "<td>"
                echo "子网掩码"
            echo "</td>"
            echo "<td>"
                getnetmask
            echo "</td>"
        echo "</tr>"
        echo "<tr>"
            echo "<td>"
                echo "网关地址"
            echo "</td>"
            echo "<td>"
                getgateway
            echo "</td>"
        echo "</tr>"
        echo "<tr>"
            echo "<td>"
                echo "系统时间"
            echo "</td>"
            echo "<td>"
                getsystime
            echo "</td>"
        echo "</tr>"
        echo "<tr>"
            echo "<td>"
                echo "系统状态"
            echo "</td>"
            echo "<td>"
                getsysstat
            echo "</td>"
        echo "</tr>"
 
    echo "</table>"
echo "</body>"
echo -e "</html>\n\n"

