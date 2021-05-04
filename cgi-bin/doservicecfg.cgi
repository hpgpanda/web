#!/bin/bash
PATH=/bin:/sbin:/usr/bin:/usr/sbin
cmdtype=
POSTSTRING=
SERVICECHK=
proname=
prolevel=
propath=
proargs=

addcmd() {
    cmd=`echo "${POSTSTRING}" | grep "add"`
    if [ "${cmd}"  != "" ];then 
        cmdtype="add"
    fi
}

delcmd() {
    cmd=`echo "${POSTSTRING}" | grep "del"`
    if [ "${cmd}"  != "" ];then 
        cmdtype="del"
    fi
}

newcmd() {
    cmd=`echo "${POSTSTRING}" | grep "new"`
    if [ "$cmd"  != "" ];then 
        cmdtype="new"
    fi
}

calcmd() {
    cmd=`echo "${POSTSTRING}" | grep "cal"`
    if [ "$cmd"  != "" ];then 
        cmdtype="cal"
    fi
}

checkitem() {
    LINE=`echo ${POSTSTRING} | sed 's/&/ /g'`
    for LOOP in $LINE
    do
        NAME=`echo ${LOOP} | sed 's/=/ /g' | awk '{print $1}'`
        TYPE=`echo ${LOOP} | sed 's/=/ /g' | awk '{print $2}' | sed -e 's/%\(\)/\\x/g' | sed 's/+/ /g'`
        if [[ "${TYPE}" = "on" ]];then
            SERVICECHK="${SERVICECHK}"" ""${NAME}"
        fi
    done
}

getinputvalue() {
    LINE=`echo $POSTSTRING | sed 's/&/ /g'`
    for LOOP in $LINE
    do
        NAME=`echo $LOOP | sed 's/=/ /g' | awk '{print $1}'`
#        TYPE=`echo $LOOP | sed 's/=/ /g' | awk '{print $2}' | sed -e 's/%\(\)/\\x/g' | sed 's/+/ /g'`
        TYPE=`echo $LOOP | sed 's/=/ /g' | awk '{print $2}' | sed 's/+/ /g'` 
        case "$NAME" in
            "servname")
                proname="${TYPE}"
            ;;
            "level")
                prolevel="${TYPE}"
            ;;
            "path")
                propath="${TYPE}"
                propath=`echo "$propath" | sed 's/%2F/\//g'`
            ;;
            "args")
                proargs="${TYPE}"
            ;;
        esac
            
    done

}

checkinputvalue() {
    if [[ "${proname}" = "" ]];then
        echo "程序名错误<br>"
        return 1
    fi

    if [[ -n "${prolevel/9[0-9]/}" ]];then
        echo "运行等级错误,运行等级必须为90～99<br>"
        return 1
    fi

    if [[ "${propath}" = "" ]] || [[ ! -d "${propath}" ]] ;then
        echo "程序路径错误<br>"
        return 1
    fi
    return 0
}

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
POSTSTRING=`cat -`
addcmd && delcmd && newcmd && calcmd
    case "${cmdtype}" in
        "add")
            SERVICECHK=""
            checkitem
            for i in $SERVICECHK
            do
                ./wr /usr/sbin/zyconfig -a $i > /dev/null
                echo "$i 启用成功!<br>"
            done

        ;;
        "del")
            SERVICECHK=""
            checkitem
            for i in $SERVICECHK
            do
                ./wr /usr/sbin/zyconfig -d $i > /dev/null
                echo "$i 删除成功!<br>"
            done
        ;;
        "cal")
            SERVICECHK=""
            checkitem
            for i in $SERVICECHK
            do
                ./wr /usr/sbin/zyconfig -c $i > /dev/null
                echo "$i 取消成功!<br>"
            done
        ;;
        "new")
            getinputvalue
            checkinputvalue
            if [[ $? -eq 0 ]]; then
                ./wr /usr/sbin/zyconfig -n "${proname}" "${prolevel}" "${propath}" "${proargs}" 
                echo "$i 新增成功!<br>"
            fi
        ;;
        esac
echo "</body>"
echo -e "</html>\n\n"
 
