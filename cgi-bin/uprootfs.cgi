#!/bin/bash
PATH=/bin:/sbin:/usr/bin:/usr/sbin
UBIFILE=""
UBIMD5FILE=""
BOARDNAME=`awk '{ if( $1=="Hardware" ) print tolower($3)}' /proc/cpuinfo`
NFSDIR="/mnt"
NFSADDR=`eeprom net show nfs`
ISMOUNTED="0"

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

getnfsip() {
    echo "获取NFS服务器地址: ${NFSADDR}<br>"
    checkip ${NFSADDR} 
    if [[ $? -eq 0 ]]; then
        return 0
    else
        echo "NFS服务器IP地址格式错误<br>"
        return 1
    fi
}

trypingnfs() {
    echo "尝试与NFS服务器通信："
    pinglostrate=`ping -q -c 4 ${NFSADDR} | grep "packet loss" | awk '{print $(NF-2)}'`
    if [[ "${pinglostrate}" != "100%" ]];then
        echo "成功<br>"
        return 0
    else
        echo "失败，请检查NFS主机是否正常开启或者NFS地址是否正确<br>"
        return 1
    fi
}

trymountnfs() {
    echo "尝试进行NFS目录挂载："
    mount -t nfs ${NFSADDR}:/zhiyuan ${NFSDIR}
    isnfsmount=`mount | grep "${NFSADDR}"`
    if [[ "${isnfsmount}" != "" ]] ;then
         echo "成功<br>"
         ISMOUNTED="1"
         return 0
    else
         echo "失败，请检查NFS服务器是否正确配置<br>"
         return 1
    fi
}



CheckUpdatedImage() {
	cd ${NFSDIR}

	# Check image file name
	MAX=0
	for i in *.ubi
	do
		CHECK=`echo $i | 
		awk -F[_.] '{ if (tolower($1) == "rootfs" && tolower($3) == "rel") printf 1}'`
		if [[ "${CHECK}" != "1" ]]; then
			continue
		fi
		BOARD=`echo $i | awk -F[_.] '{ printf tolower($2) }'`
		if [[ "${BOARD}" != "${BOARDNAME}" ]]; then
			continue
		fi
		NUM=`echo $i | awk -F[_.] '{ printf $4 }'`
		if [[ "${NUM}" -gt "${MAX}" ]]; then
			MAX=$NUM
			UBIFILE=$i
		fi
	done
	unset MAX

	if [[ "${UBIFILE}" = "rootfs.ubi" ]]; then
		return 1
	fi

	# Check image file size
	IMAGESIZE=`du -k ${UBIFILE} | awk '{printf $1}'`
	PARTSIZE=`cat /proc/partitions | awk '{ if ($4 == "mtdblock1") printf $3}'` 
	if [[ "${IMAGESIZE}" -gt "${PARTSIZE}" ]]; then
		return 1
	fi
	return 0
}

showupdatefile() {
    echo "获取升级包:"
    CheckUpdatedImage
    if [[ $? -eq 0 ]] && [[ "${UBIFILE}" != "" ]];then
        echo "$UBIFILE<br>"
        return 0
    else
        echo "失败，未找到升级包，或者升级包过大<br>"
        return 1
    fi
}

getmd5file() {
    echo "获取升级包md5校验文件:"
    for i in `seq 1 2`
    do 
        case $i in
            1)
                UBIMD5FILE=${UBIFILE}.md5
            ;;
            2)
                UBIMD5FILE=`echo ${UBIFILE} | sed 's/.ubi/.md5/g'`
            ;;
        esac
        if [ -f ${NFSDIR}/${UBIMD5FILE} ] ;then
             echo "${UBIMD5FILE}<br>"
             return 0
        fi
    done
    echo "失败，校验文件不存在<br>"
    return 1
}

checkupdatefilemd5() {
    echo "校验升级包MD5值："
    md5filevalue=`cat ${NFSDIR}/${UBIMD5FILE} | awk '{ print $1 }'`
    md5checkvalue=`md5sum ${NFSDIR}/${UBIFILE} | awk '{ print $1 }'`
    if [[ "${md5filevalue}" = "${md5checkvalue}" ]];then
        echo "成功<br>"
        return 0
    else
        echo "失败,请检查升级包完整性<br>"
        return 1
    fi
}
umountnfs() {
    cd /
    umount ${NFSDIR}
}
areyousure() {
    echo "升级条件测试完毕，可以进行升级。<br>"
    echo "<form action=\"/cgi-bin/douprootfs.cgi\" method=POST>"
          echo "<input type=\"hidden\" name=\"updated\"  value=\"1\"  >"
          echo "<input type=\"submit\" value=\"确认升级\" >"
    echo "</form>"
    return 1
}


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
    getnfsip && trypingnfs && trymountnfs && showupdatefile && getmd5file && checkupdatefilemd5  && areyousure
    if [[ "${ISMOUNTED}" = "1"  ]];then
        umountnfs
    fi
echo "</body>"
echo "</html>"
