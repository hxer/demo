<!DOCTYPE html>
<html>
<head>
<meta http-equiv="content-type" content="text/html;charset=utf-8">
<title>emp_system</title>
</dead>
<?php require_once 'common.php'; ?>
<h1>emp login</h1>
<form action="login_process.php" method="post">
<table>
<tr><td>用户名</td><td><input type="text" name="username" value="<?php echo getCookie("username");?>"/></td></tr>
<tr><td>密码</td><td><input type="text" name="password" /></td></tr>
</table>
save cookie<input type="checkbox" name="cookie"/><br/>
<input type=submit value="登陆"/><br/>

</form>

<?php
    if(!empty($_GET['errNo'])){
        $errNo=$_GET['errNo'];
        echo "<br/><font color='red'>输入的密码或用户名错误，错误信息</font>" . $errNo;
    }
?>
</html>
