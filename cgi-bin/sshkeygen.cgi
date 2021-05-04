#!/bin/bash
PATH=/bin:/sbin:/usr/bin:/usr/sbin

echo  -e "Content-type: text/html \n\n"
echo "<html>"
echo "<head>"
echo "<title>SSH 密钥更新</title>"
echo "<meta http-equiv=\"Content-Type\" content=\"text/html; charset=utf-8\" />"
echo "</head>"
echo "<body>"
echo "<center>"
echo "<h3>SSH密钥更新</h3>"
echo "</center>"
echo "<hr>"
    if [ ! -f /usr/bin/ssh-keygen ];then
        echo "更新失败, /usr/bin/ssh-keygen丢失\n\n"
    else
        echo -e "本页面可能需要几分钟才能完成，请耐心等待。\n\n<br>"
        echo -e "Generating RSA1 Key...\n\n<br>"
	    echo 'y' | ./wr /usr/bin/ssh-keygen -t rsa1 -f /etc/ssh_host_key -C '' -N '' > /dev/null
        echo -e "Generating RSA Key...\n\n<br>"
        echo 'y' | ./wr /usr/bin/ssh-keygen -t rsa -f /etc/ssh_host_rsa_key -C '' -N '' > /dev/null
        echo -e "Generating DSA Key...\n\n<br>"
        echo 'y' | ./wr /usr/bin/ssh-keygen -t dsa -f /etc/ssh_host_dsa_key -C '' -N '' > /dev/null
        echo -e "Generating ECDSA Key...\n\n<br>"
	    echo 'y' | ./wr /usr/bin/ssh-keygen -t ecdsa -f /etc/ssh_host_ecdsa_key -C '' -N '' > /dev/null
        echo -e "Done\n\n"
    fi
echo "</body>"
echo "</html>"
