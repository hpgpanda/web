#!/bin/bash

PATH=/bin:/sbin:/usr/bin:/usr/sbin
POSTSTRING=
nfsip=
getinputvalue() {
    LINE=`echo $POSTSTRING | sed 's/&/ /g'`
    for LOOP in $LINE
    do
        NAME=`echo $LOOP | sed 's/=/ /g' | awk '{print $1}'`
        TYPE=`echo $LOOP | sed 's/=/ /g' | awk '{print $2}' | sed 's/+/ /g' | sed 's/%2F/\//g' | sed 's/%3A/:/g' ` 
        case "$NAME" in
            "nfsip")
                nfsip="${TYPE}"
            ;;
        esac
            
    done

}

checkip() {
    if [[ "$1" = "" ]];then
        return 1
    fi
    if [[ "$1" = "0.0.0.0" ]];then
        return 1
    fi
    a=`echo "$1" | awk -F. '{print $1}'`
    b=`echo "$1" | awk -F. '{print $2}'`
    c=`echo "$1" | awk -F. '{print $3}'`
    d=`echo "$1" | awk -F. '{print $4}'`
    if [ "$a" = "" ] || [ "$b" = "" ] || [ "$c" = "" ] || [ "$d" = "" ];then
        return 1
    fi
    for loop in $a $b $c $d
    do
        if [ ${loop} -ge 255 ] || [ ${loop} -le 0 ]; then
            return 1
        fi
    done
    return 0
}

seteeprom() {
    eeprom net set nfs "${nfsip}"
    if [ $? -ne 0 ]; then
        echo "设置失败<br>"
    else
        echo "保存成功<br>"
    fi
}

POSTSTRING=`cat -`
echo  -e "Content-type: text/html \n\n"
echo "<html>"
echo "<head>"
echo "<title>NFS设置</title>"
echo "<meta http-equiv=\"Content-Type\" content=\"text/html; charset=utf-8\" />"
echo "</head>"
echo "<body>"
echo "<center>"
echo "<h3>NFS服务器设置</h3>"
echo "</center>"
echo "<hr>"
    getinputvalue  
    checkip "${nfsip}"
    if [[ $? -eq 1 ]];then
        echo "NFS ip 地址非法<br>"
    else
        seteeprom
    fi
echo "</body>"
echo "</html>"
