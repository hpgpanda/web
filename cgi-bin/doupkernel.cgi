#!/bin/bash
PATH=/bin:/sbin:/usr/bin:/usr/sbin
filename=
prefix=
postfix=
uImagepath=
deppath=
checkpath=
platform=
STEP=
CURDIR=`pwd`
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
    STEP=0
    return 0
}

packeterr() {
        echo "请上传符合格式的升级包：uImage_${platform}_rel_YYYYMMDD.tar, 升级失败"
}

checkfilename() {
    platform=`cat /proc/cpuinfo | grep 'Hardware' | awk '{print $3}'`
    prefix=`echo ${filename} | cut -d. -f1`
    postfix=`echo ${filename} | cut -d. -f2`
    #must be uImage
    aprefix=`echo ${prefix} | cut -d_ -f1`
#    echo "${aprefix}<br>"
    #must be ${platform}
    bprefix=`echo ${prefix} | cut -d_ -f2`
#    echo "${bprefix}<br>"
    #must be rel
    cprefix=`echo ${prefix} | cut -d_ -f3`
#    echo "${cprefix}<br>"
    #must be date
    dprefix=`echo ${prefix} | cut -d_ -f4`
#    echo "${dprefix}<br>"

    check=`echo "$dprefix" | grep '\<[0-9]\{4\}[0-1][0-9][0-3][0-9]\>'` 
    if [[ "${check}" = "" ]] || [[ "${aprefix}" != "uImage" ]] || [[ "${bprefix}" != "${platform}" ]] || [[ "${cprefix}" != "rel" ]]; then
        packeterr
        return 1
    fi
    
    if [[ "${postfix}" != "tar" ]] ;then
        packeterr  
        return 1
    fi
    return 0
}

depacket() {
    tar -xvf "/tmp/${filename}" -C /tmp/ > /dev/null
    rm -fr "/tmp/${filename}"
    STEP=1
    if [ $? -eq 0 ];then
        return 0
    else
        echo "升级包损坏，升级失败<br>"
        return 1
    fi
}

checkpacket() {
    deppath="/tmp/${prefix}"

#    echo "depacket path ${deppath}"
    files=`ls -l $deppath | grep -v "total" | wc -l` 
    if [ $files -ne 2 ];then
        echo "升级包内应只有两个文件，升级失败<br>" 
        return 1
    fi
    uImagepath="${deppath}/${prefix}"
    if [ ! -f "${uImagepath}" ];then
        echo "升级包中无${prefix}文件，升级失败<br>"
        return 1
    fi

    mv ${uImagepath} "${deppath}/uImage"
    uImagepath="${deppath}/uImage"

    cd ${deppath}
    for checkfile in *
    do
        if [[ "${checkfile}" = "${prefix}" ]];then
            continue
        fi
#        echo "${checkfile}<br><br>"
    done
    cd ${CURDIR}
#    checkfile=`ls -l ${deppath} | grep -v ""| grep -v 'total' | awk '{print $(NF)}'`
    cfprefix=`echo ${checkfile} | cut -d. -f1`
    cfpostfix=`echo ${checkfile} | cut -d. -f2`
#    timestamp=`echo ${prefix} | cut -d_ -f4`
#    echo "${timestamp}<br>"
#    echo "${prefix}<br>"
#    echo "${cfprefix}<br>"
    if [ "${cfprefix}" != "${prefix}" ];then
          echo "校验文件名与升级包名不匹配，升级失败<br>"
          return 1
    fi
    if [[ "${cfpostfix}" = "md5" ]] || [[ "${cfpostfix}" = "sha" ]] || [[ "${cfpostfix}" = "md2" ]];then
        checkpath="${deppath}/${checkfile}"
        return 0
    else
        echo "升级包中未包含.md5或.sha或.md2内核校验文件<br>"
        return 1
    fi
}

doupkernel() {
    /usr/sbin/upkernel -k ${uImagepath} -c ${checkpath}
    if [ $? -eq 0 ];then
         echo "升级成功,请重启系统.<br>"
    else
         echo "升级失败<br>"
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
    savefile  &&  checkfilename && depacket && checkpacket  && doupkernel
    
    if [[ ${STEP} -eq 0 ]] ;then
        rm -fr "/tmp/${filename}"
    elif [[ ${STEP} -eq 1 ]];then
        rm -fr "${deppath}"
    fi

echo "</body>"
echo "</html>"
