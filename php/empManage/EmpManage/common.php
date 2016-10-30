<?php

function getCookie($key){
    if(!empty($_COOKIE[$key])){
        return $_COOKIE[$key];
    }else{
        return "";
    }
}

function check_user_legal(){
    session_start();
    if(empty($_SESSION['id'])){
        header("Location:login.php?errNo=1");
    }
}
