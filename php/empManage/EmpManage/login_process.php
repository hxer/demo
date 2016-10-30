<?php

require_once 'AdminServer.class.php';

if(!empty($_POST['cookie'])){
    if(!empty($_POST['username'])){
        $username = $_POST['username'];
        setcookie("username", "$username", time()+300);
    }
    if(!empty($_POST['password'])){
        $password = $_POST['password'];
        setcookie("password", "$password", time()+300);
    }
}else{
    if(!empty($_POST['username'])){
        $username = $_POST['username'];
    }
    if(!empty($_POST['password'])){
        $password = $_POST['password'];
    }
}

$admin_server = new AdminServer();

if($id=$admin_server->check_user($username, $password)){
    //legal
    session_start();
    $_SESSION['id'] = $id;
    header("Location:main.php?id=$id");
    exit();
}else{
    //illegal
    header("Location:login.php?errNo=2");
    exit();
}
