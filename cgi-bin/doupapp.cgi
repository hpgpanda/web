#!/bin/bash
PATH=/bin:/sbin:/usr/bin:/usr/sbin
filename=
getfilename() {
    for LOOP in $1
    do
        NAME=`echo $LOOP | sed 's/=/ /g' | awk '{print $1}'`
        TYPE=`echo $LOOP | sed 's/=/ /g' | awk '{print $2}' | sed 's/"/ /g' | awk '{print $1}' | sed 's/ //g' ` 
        case "$NAME" in
            "filename")
                filename="${TYPE}"
#                echo "$filename"
            ;;
        esac
    done
}
savefile() {
    dd of=/tmp/test 
    nameline=`sed -n 2p /tmp/test`
#    echo "$nameline<br>"
    getfilename "${nameline}"
    sed -e '1,4d' -e '$d' /tmp/test  > /tmp/test.1
    rm /tmp/test
    size=`ls -l "/tmp/test.1" | awk '{ print $5 }'`
    size=`expr $size - 2`
    dd if=/tmp/test.1 of="/tmp/${filename}" bs=${size} count=1
    rm /tmp/test.1
}

packeterr() {
        echo "请上传符合格式的升级包：appname.tar, 升级失败"
}

checkfilename() {
    postfix=`echo ${filename} | cut -d. -f2`
    
    if [[ "${postfix}" != "tar" ]] ;then
        packeterr  
        return 1
    fi
}

depacket() {
    tar -xvf "/tmp/${filename}" -C /opt/ > /dev/null
    rm -fr "/tmp/${filename}"
    if [ $? -eq 0 ];then
        return 0
    else
        echo "升级包损坏，升级失败<br>"
        return 1
    fi
}

echo  -e "Content-type: text/html \n\n"
echo "<html>"
echo "<head>"
echo "<title>内核升级</title>"
echo "<meta http-equiv=\"Content-Type\" content=\"text/html; charset=utf-8\" />"
echo "</head>"
echo "<body>"
echo "<center>"
echo "<h3>内核升级</h3>"
echo "</center>"
echo "<hr>"
    savefile
    checkfilename
    if [  $? -eq 0 ];then
        depacket
        if [ $? -eq 0 ];then
            echo "升级成功<br>"
        else
            echo "升级失败<br>"
        fi
    fi
echo "</body>"
echo "</html>"
