<html>
<!- Guangzhou Zhiyuan  Pengguowen linux@zlgmcu.com ->
<head>
<title>更改密码</title>
<meta http-equiv=Content-Type content=text/html; charset=utf-8 />
<meta http-equiv="Pragma" content="no-cache">
<script type="text/javascript">
    function chkpassword()
    {
        if (password.newpw.value == password.again.value) {
            return true;    
        }
        alert("两次输入密码不相同！");
        return false;
    }
</script>
</head>
<body>
<center>
<h3>更改用户密码</h3>
</center>
<hr>
<center>
<br>
<br>
<form name="password" action=/goform/SetPassword onsubmit="return chkpassword();"  method=POST>
<table>
<tr>
	<td>旧密码:</td>
<td>
	<input type=password name=oldpw size=40 >
</td>
</tr>
<tr>
	<td>新密码:</td>
<td>
	<input type=password name=newpw size=40 >
</td>
</tr>
<tr>
	<td>确认密码:</td>
<td>
	<input type=password name=again size=40 >
</td>
</tr>
<tr>
    <td></td>
      <td ALIGN="CENTER"> 
        <input type=hidden name=user value="admin">
        <input type=submit name=ok value="确定" >
        <input type=submit name=ok value="取消"></td>
</tr>
</table>

</form>

</center>
</body>
</html>
