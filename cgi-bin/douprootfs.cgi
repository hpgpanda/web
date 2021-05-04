#!/bin/bash
updated=
POSTSTRING=
getinputvalue() {
    LINE=`echo $POSTSTRING | sed 's/&/ /g'`
    for LOOP in $LINE
    do
        NAME=`echo $LOOP | sed 's/=/ /g' | awk '{print $1}'`
        TYPE=`echo $LOOP | sed 's/=/ /g' | awk '{print $2}' | sed 's/+/ /g' | sed 's/%2F/\//g' | sed 's/%3A/:/g' ` 
        case "$NAME" in
            "updated")
                updated="${TYPE}"
            ;;
        esac
            
    done

}


POSTSTRING=`cat -`
echo  -e "Content-type: text/html \n\n"
echo "<html>"
echo "<head>"
echo "<title>SSH 文件系统更新</title>"
echo "<meta http-equiv=\"Content-Type\" content=\"text/html; charset=utf-8\" />"
echo "</head>"
echo "<body>"
echo "<center>"
echo "<h3>文件系统更新</h3>"
echo "</center>"
echo "<hr>"
    getinputvalue
#    echo "${updated}<br>"
    if [[ "${updated}" = "1" ]];then
        eeprom flag set 1
        echo "设置完成，请重启系统进行升级<br>"
    fi
echo "</body>"
echo "</html>"
