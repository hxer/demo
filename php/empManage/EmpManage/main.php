<!DOCTYPE html>
<html>
<head>
<meta http-equiv="content-type" content="text/html;charset=utf-8">
</head>
<?php
    require_once 'AdminServer.class.php';
    require_once 'common.php';
    check_user_legal();
    if(!empty($_REQUEST['id'])){
        $admin_server = new AdminServer();
        $id = $_REQUEST['id'];
        echo "欢迎" . $id. "登陆<br/>";
        $login_time = implode('',$admin_server->get_lasttime());
        echo "上次登录时间:" .$login_time. "<br />";
        $admin_server->update_logintime();
    }
?>
<h1>Main View</h1>
<a href="list_emp.php">管理用户</a><br/>
<a href="add_emp.php">添加用户</a><br/>
<a href="query_emp.php">查询用户</a><br/>

</html>
